"""Full HTTP/API workflow using synthetic data; does not exercise browser UI."""

import json
import test_environment  # Configure a test key before importing authentication.
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fitz
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app import models
from app.database import Base
from app.dependencies import get_db
from app.routers import auth, resumes, users


class ResumeFlowTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.storage = Path(self.directory.name)
        storage_patch = patch.object(resumes, 'UPLOAD_DIRECTORY', self.storage)
        storage_patch.start()
        self.addCleanup(storage_patch.stop)
        self.engine = create_engine('sqlite://', poolclass=StaticPool,
                                    connect_args={'check_same_thread': False})
        self.addCleanup(self.engine.dispose)
        Base.metadata.create_all(self.engine)
        self.app = FastAPI()
        for router in (auth.router, users.router, resumes.router):
            self.app.include_router(router)

        def test_db():
            with Session(self.engine) as db:
                yield db

        self.app.dependency_overrides[get_db] = test_db

    async def request(self, method, path, token=None, payload=None, pdf=None):
        path, _, query = path.partition('?')
        headers = []
        body = b''
        if token:
            headers.append((b'authorization', f'Bearer {token}'.encode()))
        if payload is not None:
            body = json.dumps(payload).encode()
            headers.append((b'content-type', b'application/json'))
        if pdf is not None:
            boundary = 'synthetic-resume-boundary'
            body = (f'--{boundary}\r\nContent-Disposition: form-data; name="resume_file"; '
                    'filename="sample.pdf"\r\nContent-Type: application/pdf\r\n\r\n').encode()
            body += pdf + f'\r\n--{boundary}--\r\n'.encode()
            headers.append((b'content-type', f'multipart/form-data; boundary={boundary}'.encode()))
        headers.append((b'content-length', str(len(body)).encode()))
        messages = []

        async def receive():
            return {'type': 'http.request', 'body': body, 'more_body': False}

        async def send(message):
            messages.append(message)

        await self.app({'type': 'http', 'asgi': {'version': '3.0'}, 'http_version': '1.1',
                        'method': method, 'scheme': 'http', 'path': path,
                        'raw_path': path.encode(), 'query_string': query.encode(), 'root_path': '',
                        'headers': headers, 'server': ('test', 80), 'client': ('test', 1)},
                       receive, send)
        status = next(m['status'] for m in messages if m['type'] == 'http.response.start')
        response = b''.join(m.get('body', b'') for m in messages if m['type'] == 'http.response.body')
        return status, json.loads(response) if response else None

    async def register_and_login(self, email):
        details = {'full_name': 'Synthetic User', 'email': email, 'password': 'synthetic-test-password'}
        status, user = await self.request('POST', '/auth/register', payload=details)
        self.assertEqual(status, 201)
        self.assertNotIn('password', user)
        status, session = await self.request('POST', '/auth/login', payload=details)
        self.assertEqual(status, 200)
        self.assertEqual(session['token_type'], 'bearer')
        return session['access_token'], user['id']

    async def test_register_to_role_results_and_owner_isolation(self):
        token, user_id = await self.register_and_login('owner@example.com')
        status, profile = await self.request('GET', '/users/me', token)
        self.assertEqual(status, 200)
        self.assertEqual(profile['id'], user_id)
        self.assertEqual(await self.request('GET', '/resumes', token), (200, []))
        text = 'Python FastAPI SQL Git Docker'
        with fitz.open() as document:
            document.new_page().insert_text((72, 72), text)
            pdf = document.tobytes()
        status, uploaded = await self.request('POST', '/resumes/upload', token, pdf=pdf)
        self.assertEqual(status, 201)
        resume_id = uploaded['id']
        status, listing = await self.request('GET', '/resumes', token)
        self.assertEqual(status, 200)
        self.assertEqual([row['id'] for row in listing], [resume_id])
        status, detail = await self.request('GET', f'/resumes/{resume_id}', token)
        self.assertEqual(status, 200)
        self.assertEqual(detail['resume_text'], text)
        status, skills = await self.request('GET', f'/resumes/{resume_id}/skills', token)
        self.assertEqual(status, 200)
        self.assertEqual(skills['skills'], ['Docker', 'FastAPI', 'Git', 'Python', 'SQL'])
        status, matches = await self.request('GET', f'/resumes/{resume_id}/matches', token)
        self.assertEqual(status, 200)
        self.assertEqual(matches['matches'][0]['role_id'], 'python_backend')
        self.assertEqual(matches['matches'][0]['skill_overlap_percent'], 100.0)
        with Session(self.engine) as db:
            row = db.get(models.Resume, resume_id)
            self.assertEqual(row.user_id, user_id)
            self.assertEqual(Path(row.file_path).read_bytes(), pdf)
        other_token, _ = await self.register_and_login('other@example.com')
        self.assertEqual(await self.request('GET', '/resumes', other_token), (200, []))
        for suffix in ('', '/skills', '/matches'):
            path = f'/resumes/{resume_id}{suffix}'
            self.assertEqual((await self.request('GET', path, other_token))[0], 404)
            self.assertEqual((await self.request('GET', path))[0], 401)

    async def test_legacy_login_and_registration_limit(self):
        fixture = json.loads(Path(__file__).with_name('fixtures').joinpath('legacy_bcrypt.json').read_text())[2]
        with Session(self.engine) as db:
            db.add(models.User(full_name='Legacy Test', email='legacy@example.com', hashed_password=fixture['hash']))
            db.commit()
        status, _ = await self.request('POST', '/auth/login', payload={
            'email': 'legacy@example.com', 'password': fixture['password']})
        self.assertEqual(status, 200)
        for password in ('a' * 73, '\u00e9' * 37, 'abc\x00def', ''):
            status, _ = await self.request('POST', '/auth/register', payload={
                'full_name': 'Test', 'email': 'new@example.com', 'password': password})
            self.assertEqual(status, 422)
        with Session(self.engine) as db:
            self.assertEqual(db.query(models.User).count(), 1)

    async def test_bad_login_and_corrupt_upload(self):
        token, _ = await self.register_and_login('failure@example.com')
        status, _ = await self.request('POST', '/auth/login', payload={
            'email': 'failure@example.com', 'password': 'wrong-password'})
        self.assertEqual(status, 401)
        self.assertEqual((await self.request('POST', '/resumes/upload', pdf=b'invalid'))[0], 401)
        status, _ = await self.request('POST', '/resumes/upload', token, pdf=b'invalid')
        self.assertEqual(status, 400)
        self.assertEqual(await self.request('GET', '/resumes', token), (200, []))
        self.assertEqual(list(self.storage.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
