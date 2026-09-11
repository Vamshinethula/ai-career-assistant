import json
import unittest
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app import models
from app.database import Base
from app.dependencies import get_db
from app.jwt_handler import ALGORITHM, SECRET_KEY
from app.routers.resumes import router


class ResumeListTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://', poolclass=StaticPool,
                                    connect_args={'check_same_thread': False})
        self.addCleanup(self.engine.dispose)
        Base.metadata.create_all(self.engine)
        with Session(self.engine) as db:
            db.add_all([models.User(id=i, full_name=f'User {i}',
                                   email=f'user{i}@example.com', hashed_password='unused')
                        for i in (1, 2, 3)])
            db.add_all([models.Resume(id=i, user_id=owner, original_filename=f'{i}.pdf',
                                     stored_filename=f'{i}.pdf', file_path='unused',
                                     resume_text='private text',
                                     uploaded_at=datetime(2026, 9, 11))
                        for i, owner in [(1, 1), (2, 2), (3, 1)]])
            db.commit()
        self.app = FastAPI()
        self.app.include_router(router)

        def test_db():
            with Session(self.engine) as db:
                yield db

        self.app.dependency_overrides[get_db] = test_db

    async def get(self, user_id=None, invalid=False, path='/resumes'):
        headers = []
        if user_id is not None or invalid:
            token = 'invalid' if invalid else jwt.encode(
                {'sub': str(user_id), 'exp': datetime.now(timezone.utc) + timedelta(minutes=1)},
                SECRET_KEY, algorithm=ALGORITHM)
            headers = [(b'authorization', f'Bearer {token}'.encode())]
        messages = []

        async def receive():
            return {'type': 'http.request', 'body': b'', 'more_body': False}

        async def send(message):
            messages.append(message)

        await self.app({'type': 'http', 'asgi': {'version': '3.0'}, 'http_version': '1.1',
                        'method': 'GET', 'scheme': 'http', 'path': path,
                        'raw_path': path.encode(), 'query_string': b'', 'root_path': '',
                        'headers': headers, 'server': ('test', 80), 'client': ('test', 1)},
                       receive, send)
        status = next(m['status'] for m in messages if m['type'] == 'http.response.start')
        body = b''.join(m.get('body', b'') for m in messages if m['type'] == 'http.response.body')
        return status, json.loads(body)

    async def test_lists_only_authenticated_users_resumes_newest_first(self):
        status, body = await self.get(1)
        self.assertEqual(status, 200)
        self.assertEqual([row['id'] for row in body], [3, 1])
        self.assertTrue(all(row['user_id'] == 1 for row in body))
        self.assertEqual(set(body[0]), {'id', 'original_filename', 'user_id', 'uploaded_at'})
        status, body = await self.get(2)
        self.assertEqual(status, 200)
        self.assertEqual([row['id'] for row in body], [2])

    async def test_user_without_resumes_gets_empty_list(self):
        self.assertEqual(await self.get(3), (200, []))

    async def test_missing_and_invalid_auth_rejected(self):
        self.assertEqual((await self.get())[0], 401)
        self.assertEqual((await self.get(invalid=True))[0], 401)

    async def test_detail_returns_owners_text_without_storage_paths(self):
        status, body = await self.get(1, path='/resumes/1')
        self.assertEqual(status, 200)
        self.assertEqual(body['resume_text'], 'private text')
        self.assertEqual(set(body), {'id', 'original_filename', 'user_id', 'uploaded_at', 'resume_text'})

    async def test_detail_hides_other_users_and_missing_resumes(self):
        foreign = await self.get(1, path='/resumes/2')
        missing = await self.get(1, path='/resumes/999')
        self.assertEqual(foreign, (404, {'detail': 'Resume not found'}))
        self.assertEqual(foreign, missing)

    async def test_detail_requires_authentication(self):
        self.assertEqual((await self.get(path='/resumes/1'))[0], 401)
        self.assertEqual((await self.get(invalid=True, path='/resumes/1'))[0], 401)

    async def test_detail_accepts_empty_or_missing_text(self):
        for value in ('', None):
            with Session(self.engine) as db:
                db.get(models.Resume, 1).resume_text = value
                db.commit()
            status, body = await self.get(1, path='/resumes/1')
            self.assertEqual(status, 200)
            self.assertEqual(body['resume_text'], value)

    async def test_skills_extract_stored_text_without_modifying_it(self):
        with Session(self.engine) as db:
            db.get(models.Resume, 1).resume_text = 'Python, FastAPI and python'
            db.commit()
        status, body = await self.get(1, path='/resumes/1/skills')
        self.assertEqual(status, 200)
        self.assertEqual(body, {'resume_id': 1, 'method': 'rule_based',
                                'text_available': True, 'skills': ['FastAPI', 'Python']})
        with Session(self.engine) as db:
            self.assertEqual(db.get(models.Resume, 1).resume_text, 'Python, FastAPI and python')

    async def test_skills_require_owner_and_authentication(self):
        self.assertEqual((await self.get(path='/resumes/1/skills'))[0], 401)
        self.assertEqual((await self.get(invalid=True, path='/resumes/1/skills'))[0], 401)
        foreign = await self.get(1, path='/resumes/2/skills')
        self.assertEqual(foreign, (404, {'detail': 'Resume not found'}))
        self.assertEqual(foreign, await self.get(1, path='/resumes/999/skills'))

    async def test_skills_distinguish_missing_text_from_no_matches(self):
        for text, available in [(None, False), ('', False), (' \n', False), ('Carpentry', True)]:
            with Session(self.engine) as db:
                db.get(models.Resume, 1).resume_text = text
                db.commit()
            status, body = await self.get(1, path='/resumes/1/skills')
            self.assertEqual(status, 200)
            self.assertEqual(body['text_available'], available)
            self.assertEqual(body['skills'], [])


if __name__ == '__main__':
    unittest.main()
