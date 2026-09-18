import unittest
from pathlib import Path
import test_job_comparison
import test_resume_flow
from sqlalchemy.orm import Session
from app import models


class SavedComparisonTests(unittest.IsolatedAsyncioTestCase):
    setUp = test_resume_flow.ResumeFlowTests.setUp
    request = test_resume_flow.ResumeFlowTests.request
    register_and_login = test_resume_flow.ResumeFlowTests.register_and_login
    seed = test_job_comparison.JobComparisonApiTests.seed

    async def test_rename_only_changes_title_and_checks_owner(self):
        token, resume_id = await self.seed()
        path = f'/resumes/{resume_id}/comparisons'
        _, original = await self.request('POST', path, token, payload={'title': 'Original', 'job_description': 'Python required'})
        target = f"{path}/{original['id']}"
        other, _ = await self.register_and_login('rename-other@example.com')
        self.assertEqual((await self.request('PATCH', target, other, payload={'title': 'No'}))[0], 404)
        self.assertEqual((await self.request('PATCH', target, payload={'title': 'No'}))[0], 401)
        for title in (' ', 'x' * 121):
            self.assertEqual((await self.request('PATCH', target, token, payload={'title': title}))[0], 422)
        status, renamed = await self.request('PATCH', target, token, payload={'title': ' Updated '})
        self.assertEqual(status, 200)
        self.assertEqual(renamed, {**original, 'title': 'Updated'})
        self.assertEqual(await self.request('GET', target, token), (200, renamed))

    async def test_title_search_literal_matches_pagination_and_ownership(self):
        token, resume_id = await self.seed()
        path = f'/resumes/{resume_id}/comparisons'
        for title in ('Backend Python', 'BACKEND API', '100% role', 'data_role', 'Unrelated'):
            await self.request('POST', path, token, payload={'title': title, 'job_description': 'Python required'})
        async def titles(query):
            status, rows = await self.request('GET', f'{path}?{query}', token)
            self.assertEqual(status, 200)
            return [row['title'] for row in rows]
        self.assertEqual(await titles('search=%20backend%20'), ['BACKEND API', 'Backend Python'])
        self.assertEqual(await titles('search=backend&offset=1&limit=1'), ['Backend Python'])
        self.assertEqual(await titles('search=%25'), ['100% role'])
        self.assertEqual(await titles('search=_'), ['data_role'])
        self.assertEqual(await titles('search=missing'), [])
        self.assertEqual(len(await titles('search=%20')), 5)
        self.assertEqual((await self.request('GET', f'{path}?search=' + 'x' * 121, token))[0], 422)
        other, _ = await self.register_and_login('search-other@example.com')
        self.assertEqual((await self.request('GET', f'{path}?search=backend', other))[0], 404)
        self.assertEqual((await self.request('GET', f'{path}?search=backend'))[0], 401)

    async def test_history_pagination_limits_order_and_ownership(self):
        token, resume_id = await self.seed()
        path = f'/resumes/{resume_id}/comparisons'
        ids = []
        for index in range(23):
            status, saved = await self.request('POST', path, token, payload={
                'title': f'Role {index}', 'job_description': 'Python required'})
            self.assertEqual(status, 201)
            ids.append(saved['id'])
        self.assertEqual(len((await self.request('GET', path, token))[1]), 20)
        collected = []
        for offset in (0, 10, 20):
            status, rows = await self.request('GET', f'{path}?offset={offset}&limit=10', token)
            self.assertEqual(status, 200)
            collected.extend(row['id'] for row in rows)
        self.assertEqual(collected, ids[::-1])
        self.assertEqual(await self.request('GET', f'{path}?offset=30&limit=10', token), (200, []))
        for query in ('offset=-1', 'limit=0', 'limit=101', 'offset=invalid'):
            self.assertEqual((await self.request('GET', f'{path}?{query}', token))[0], 422)
        other, _ = await self.register_and_login('page-other@example.com')
        self.assertEqual((await self.request('GET', f'{path}?offset=10&limit=10', other))[0], 404)
        self.assertEqual((await self.request('GET', f'{path}?offset=10&limit=10'))[0], 401)

    async def test_delete_owner_only_preserves_resume_pdf_and_other_snapshots(self):
        token, resume_id = await self.seed()
        path = f'/resumes/{resume_id}/comparisons'
        payload = {'title': 'Delete test', 'job_description': 'Python required'}
        _, saved = await self.request('POST', path, token, payload=payload)
        _, retained = await self.request('POST', path, token, payload=payload)
        target = f"{path}/{saved['id']}"
        with Session(self.engine) as db:
            resume = db.get(models.Resume, resume_id)
            pdf_path = Path(resume.file_path)
            original_pdf = pdf_path.read_bytes()
            original_text = resume.resume_text
        other, _ = await self.register_and_login('delete-other@example.com')
        self.assertEqual((await self.request('DELETE', target))[0], 401)
        self.assertEqual((await self.request('DELETE', target, other))[0], 404)
        self.assertEqual((await self.request('GET', target, token))[0], 200)
        self.assertEqual(await self.request('DELETE', target, token), (204, None))
        self.assertEqual((await self.request('DELETE', target, token))[0], 404)
        self.assertEqual((await self.request('GET', target, token))[0], 404)
        _, listing = await self.request('GET', path, token)
        self.assertEqual([row['id'] for row in listing], [retained['id']])
        with Session(self.engine) as db:
            self.assertEqual(db.get(models.Resume, resume_id).resume_text, original_text)
        self.assertEqual(pdf_path.read_bytes(), original_pdf)

    async def test_save_relogin_and_snapshot_isolation(self):
        token, resume_id = await self.seed()
        path = f'/resumes/{resume_id}/comparisons'
        payload = {'title': 'Backend role', 'job_description': 'Python required; Java optional',
                   'label_choices': {'Python': 'required', 'Java': 'optional'}}
        self.assertEqual(await self.request('GET', path, token), (200, []))
        status, saved = await self.request('POST', path, token, payload=payload)
        self.assertEqual(status, 201)
        self.assertEqual(saved['result']['skill_overlap_percent'], 50)
        with Session(self.engine) as db:
            db.get(models.Resume, resume_id).resume_text = 'Java'
            db.commit()
        status, login = await self.request('POST', '/auth/login', payload={
            'email': 'compare@example.com', 'password': 'synthetic-test-password'})
        self.assertEqual(status, 200)
        token = login['access_token']
        status, listing = await self.request('GET', path, token)
        self.assertEqual(status, 200)
        self.assertEqual(listing[0]['id'], saved['id'])
        self.assertNotIn('job_description', listing[0])
        self.assertEqual(await self.request('GET', f"{path}/{saved['id']}", token), (200, saved))
        other, _ = await self.register_and_login('other-saved@example.com')
        for target in (path, f"{path}/{saved['id']}"):
            self.assertEqual((await self.request('GET', target, other))[0], 404)
            self.assertEqual((await self.request('GET', target))[0], 401)
        self.assertEqual((await self.request('POST', path, other, payload=payload))[0], 404)
        self.assertEqual((await self.request('POST', path, payload=payload))[0], 401)

    async def test_invalid_save_does_not_create_rows(self):
        token, resume_id = await self.seed()
        path = f'/resumes/{resume_id}/comparisons'
        base = {'title': 'Role', 'job_description': 'Python required'}
        for change in ({'title': ' '}, {'title': 'x' * 121}, {'job_description': ' '},
                       {'label_choices': {'Unknown': 'required'}}, {'label_choices': {'Python': 'fake'}}):
            self.assertEqual((await self.request('POST', path, token, payload={**base, **change}))[0], 422)
        self.assertEqual(await self.request('GET', path, token), (200, []))
        self.assertEqual((await self.request('GET', f'{path}/999999', token))[0], 404)
