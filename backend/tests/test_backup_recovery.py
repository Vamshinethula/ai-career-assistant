"""Offline, same-path recovery drill using only disposable synthetic data."""
import shutil
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import fitz
from fastapi import FastAPI
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

import test_resume_flow
from app import models
from app.dependencies import get_db
from app.migrations import migrate_database, require_current_schema
from app.routers import auth, resumes, users


class BackupRecoveryTests(unittest.IsolatedAsyncioTestCase):
    # Reuse the existing HTTP driver rather than introduce another API client.
    request = test_resume_flow.ResumeFlowTests.request
    register_and_login = test_resume_flow.ResumeFlowTests.register_and_login

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.data = self.root / 'data'
        self.storage = self.data / 'uploads'
        self.storage.mkdir(parents=True)
        self.database = self.data / 'career_assistant.db'
        self.engine = self.open_engine()
        self.addCleanup(lambda: self.engine.dispose())
        migrate_database(self.engine)
        storage_patch = patch.object(resumes, 'UPLOAD_DIRECTORY', self.storage)
        storage_patch.start()
        self.addCleanup(storage_patch.stop)
        self.app = FastAPI()
        for router in (auth.router, users.router, resumes.router):
            self.app.include_router(router)

        def test_db():
            with Session(self.engine) as db:
                yield db

        self.app.dependency_overrides[get_db] = test_db

    def open_engine(self):
        return create_engine(URL.create('sqlite', database=str(self.database)),
                             connect_args={'check_same_thread': False})

    async def seed_and_snapshot(self):
        token, _ = await self.register_and_login('recovery@example.com')
        await self.register_and_login('other@example.com')
        with fitz.open() as document:
            document.new_page().insert_text((72, 72), 'Python FastAPI SQL Git Docker')
            self.pdf = document.tobytes()
        status, uploaded = await self.request('POST', '/resumes/upload', token, pdf=self.pdf)
        self.assertEqual(status, 201)
        self.resume_id = uploaded['id']
        status, saved = await self.request('POST', f'/resumes/{self.resume_id}/comparisons', token,
            payload={'title': 'Recovery snapshot', 'job_description': 'Python required',
                     'label_choices': {'Python': 'required'}})
        self.assertEqual(status, 201)
        saved_path = f"/resumes/{self.resume_id}/comparisons/{saved['id']}"
        self.expected = {}
        for path in ('/users/me', '/resumes', f'/resumes/{self.resume_id}',
                     f'/resumes/{self.resume_id}/skills', f'/resumes/{self.resume_id}/matches', saved_path):
            self.expected[path] = await self.request('GET', path, token)
            self.assertEqual(self.expected[path][0], 200)
        # Quiesce writes and close connections before copying the two-part backup.
        self.engine.dispose()
        self.backup = self.root / 'backup'
        self.backup.mkdir()
        with closing(sqlite3.connect(self.database.as_uri() + '?mode=ro', uri=True)) as source:
            with closing(sqlite3.connect(self.backup / self.database.name)) as target:
                source.backup(target)
                self.assertEqual(target.execute('PRAGMA integrity_check').fetchall(), [('ok',)])
        shutil.copytree(self.storage, self.backup / 'uploads')
        # Keep the original intact but unavailable at its former path.
        self.data.rename(self.root / 'original-offline')
        self.data.mkdir()

    def restore(self, include_uploads):
        shutil.copy2(self.backup / self.database.name, self.database)
        if include_uploads:
            shutil.copytree(self.backup / 'uploads', self.storage)
        self.engine = self.open_engine()
        require_current_schema(self.engine)

    async def login(self, email='recovery@example.com', password='synthetic-test-password'):
        return await self.request('POST', '/auth/login', payload={'email': email, 'password': password})

    async def test_complete_snapshot_restores_account_results_and_pdf(self):
        await self.seed_and_snapshot()
        self.restore(include_uploads=True)
        status, session = await self.login()
        self.assertEqual(status, 200)
        token = session['access_token']
        for path, expected in self.expected.items():
            self.assertEqual(await self.request('GET', path, token), expected)
        with Session(self.engine) as db:
            row = db.get(models.Resume, self.resume_id)
            restored_pdf = Path(row.file_path)
            self.assertEqual(restored_pdf.parent, self.storage)
            self.assertEqual(restored_pdf.read_bytes(), self.pdf)
        self.assertEqual((await self.login(password='wrong'))[0], 401)
        status, other = await self.login('other@example.com')
        self.assertEqual(status, 200)
        for suffix in ('', '/skills', '/matches'):
            path = f'/resumes/{self.resume_id}{suffix}'
            self.assertEqual((await self.request('GET', path, other['access_token']))[0], 404)
            self.assertEqual((await self.request('GET', path))[0], 401)

    async def test_database_only_restore_is_not_complete_recovery(self):
        await self.seed_and_snapshot()
        self.restore(include_uploads=False)
        status, session = await self.login()
        self.assertEqual(status, 200)
        path = f'/resumes/{self.resume_id}'
        self.assertEqual(await self.request('GET', path, session['access_token']), self.expected[path])
        with Session(self.engine) as db:
            row = db.get(models.Resume, self.resume_id)
            with self.assertRaises(FileNotFoundError):
                Path(row.file_path).read_bytes()
