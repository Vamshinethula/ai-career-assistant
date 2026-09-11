import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fitz
from fastapi import HTTPException, UploadFile
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.datastructures import Headers

from app import models
from app.database import Base
from app.routers import resumes


class ResumeUploadTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.upload_path = Path(self.directory.name)
        self.directory_patch = patch.object(resumes, 'UPLOAD_DIRECTORY', self.upload_path)
        self.directory_patch.start()
        self.addCleanup(self.directory_patch.stop)
        self.engine = create_engine('sqlite://')
        self.addCleanup(self.engine.dispose)
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)
        self.addCleanup(self.db.close)
        self.user = models.User(full_name='Test User', email='test@example.com',
                                hashed_password='unused-test-value')
        self.db.add(self.user)
        self.db.commit()

    def upload(self, content, filename='resume.pdf'):
        upload = UploadFile(file=io.BytesIO(content), filename=filename,
                            headers=Headers({'content-type': 'application/pdf'}))
        return resumes.upload_resume(upload, self.db, self.user)

    def pdf(self):
        with fitz.open() as document:
            document.new_page().insert_text((72, 72), 'Python FastAPI test resume')
            return document.tobytes()

    def assert_no_artifacts(self):
        self.assertEqual(self.db.query(models.Resume).count(), 0)
        self.assertEqual(list(self.upload_path.iterdir()), [])

    def test_valid_pdf_saves_text_file_and_owner(self):
        result = self.upload(self.pdf())
        self.db.expire_all()
        row = self.db.get(models.Resume, result.id)
        self.assertEqual(row.user_id, self.user.id)
        self.assertEqual(row.resume_text, 'Python FastAPI test resume')
        self.assertTrue(Path(row.file_path).is_file())
        self.assertEqual(result.original_filename, 'resume.pdf')

    def test_corrupt_pdf_leaves_no_artifacts(self):
        with self.assertRaises(HTTPException) as raised:
            self.upload(b'This is not a PDF')
        self.assertEqual(raised.exception.status_code, 500)
        self.assert_no_artifacts()

    def test_commit_failure_leaves_no_artifacts(self):
        with patch.object(self.db, 'commit', side_effect=SQLAlchemyError('test failure')):
            with self.assertRaises(HTTPException) as raised:
                self.upload(self.pdf())
        self.assertEqual(raised.exception.status_code, 500)
        self.assert_no_artifacts()

    def test_parser_failure_leaves_no_database_row(self):
        with patch.object(resumes, 'extract_text_from_pdf', side_effect=RuntimeError('test parser failure')):
            with self.assertRaises(HTTPException):
                self.upload(self.pdf())
        self.assert_no_artifacts()

    def test_partial_write_leaves_no_artifacts(self):
        def fail_copy(source, destination):
            destination.write(b'partial')
            raise OSError('simulated disk failure')
        with patch.object(resumes.shutil, 'copyfileobj', side_effect=fail_copy):
            with self.assertRaises(HTTPException) as raised:
                self.upload(self.pdf())
        self.assertEqual(raised.exception.status_code, 500)
        self.assert_no_artifacts()

    def test_non_pdf_rejected_without_artifacts(self):
        with self.assertRaises(HTTPException) as raised:
            self.upload(b'not a PDF', 'resume.docx')
        self.assertEqual(raised.exception.status_code, 400)
        self.assert_no_artifacts()


if __name__ == '__main__':
    unittest.main()
