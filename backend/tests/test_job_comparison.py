import unittest

import fitz
import test_resume_flow
from sqlalchemy.orm import Session

from app import models
from app.services.job_comparison import compare_job_description


class JobComparisonServiceTests(unittest.TestCase):
    def test_cross_line_alias_keeps_score_and_uses_uncertain_evidence(self):
        result = compare_job_description('JavaScript', 'Required: Java\nScript')
        self.assertEqual(result['job_skills'], ['JavaScript'])
        self.assertEqual(result['skill_overlap_percent'], 100.0)
        self.assertEqual(result['requirements'], [{'skill': 'JavaScript', 'category': 'uncertain',
            'evidence': [{'text': 'Required: Java\nScript', 'category': 'uncertain'}]}])

    def test_aliases_duplicates_and_denominator(self):
        result = compare_job_description('Python Fast API Git', 'Python python FastAPI Docker')
        self.assertEqual(result['job_skills'], ['Docker', 'FastAPI', 'Python'])
        self.assertEqual(result['matched_skills'], ['FastAPI', 'Python'])
        self.assertEqual(result['not_detected_skills'], ['Docker'])
        self.assertEqual(result['skill_overlap_percent'], 66.7)

    def test_empty_evidence_and_zero_overlap_are_different(self):
        for text in (None, '', '  '):
            result = compare_job_description(text, 'Python')
            self.assertFalse(result['text_available'])
            self.assertIsNone(result['skill_overlap_percent'])
        self.assertIsNone(compare_job_description('Python', 'Team player')['skill_overlap_percent'])
        self.assertEqual(compare_job_description('Java', 'Python')['skill_overlap_percent'], 0.0)
        self.assertEqual(compare_job_description('Python', 'Python')['skill_overlap_percent'], 100.0)

    def test_spaced_javascript_does_not_invent_java(self):
        result = compare_job_description('JavaScript', 'Java Script and Java')
        self.assertEqual(result['matched_skills'], ['JavaScript'])
        self.assertEqual(result['not_detected_skills'], ['Java'])
        self.assertEqual(result['skill_overlap_percent'], 50.0)


class JobComparisonApiTests(unittest.IsolatedAsyncioTestCase):
    setUp = test_resume_flow.ResumeFlowTests.setUp
    request = test_resume_flow.ResumeFlowTests.request
    register_and_login = test_resume_flow.ResumeFlowTests.register_and_login

    async def seed(self):
        token, _ = await self.register_and_login('compare@example.com')
        with fitz.open() as document:
            document.new_page().insert_text((72, 72), 'Python FastAPI SQL Git Docker')
            pdf = document.tobytes()
        status, resume = await self.request('POST', '/resumes/upload', token, pdf=pdf)
        self.assertEqual(status, 201)
        return token, resume['id']

    async def test_comparison_and_ownership(self):
        token, resume_id = await self.seed()
        path = f'/resumes/{resume_id}/compare-job'
        payload = {'job_description': 'Python Docker Kubernetes'}
        status, result = await self.request('POST', path, token, payload=payload)
        self.assertEqual(status, 200)
        self.assertEqual(result['method'], 'keyword_overlap')
        self.assertEqual(result['matched_skills'], ['Docker', 'Python'])
        self.assertEqual(result['not_detected_skills'], ['Kubernetes'])
        self.assertEqual(result['skill_overlap_percent'], 66.7)
        self.assertNotIn('job_description', result)
        self.assertEqual([row['skill'] for row in result['requirements']], result['job_skills'])
        other, _ = await self.register_and_login('other-compare@example.com')
        self.assertEqual((await self.request('POST', path, other, payload=payload))[0], 404)
        self.assertEqual((await self.request('POST', path, payload=payload))[0], 401)
        self.assertEqual((await self.request('POST', '/resumes/99999/compare-job', token, payload=payload))[0], 404)
        with Session(self.engine) as db:
            self.assertEqual(db.get(models.Resume, resume_id).resume_text, 'Python FastAPI SQL Git Docker')

    async def test_validation_and_length_boundary(self):
        token, resume_id = await self.seed()
        path = f'/resumes/{resume_id}/compare-job'
        for payload in ({}, {'job_description': ''}, {'job_description': ' \n '},
                        {'job_description': 'x' * 10001}, {'job_description': None}):
            self.assertEqual((await self.request('POST', path, token, payload=payload))[0], 422)
        status, result = await self.request('POST', path, token, payload={'job_description': 'x' * 10000})
        self.assertEqual(status, 200)
        self.assertEqual(result['job_skills'], [])
        self.assertIsNone(result['skill_overlap_percent'])

    async def test_no_readable_resume_text(self):
        token, resume_id = await self.seed()
        with Session(self.engine) as db:
            db.get(models.Resume, resume_id).resume_text = None
            db.commit()
        status, result = await self.request('POST', f'/resumes/{resume_id}/compare-job', token,
                                            payload={'job_description': 'Python'})
        self.assertEqual(status, 200)
        self.assertFalse(result['text_available'])
        self.assertIsNone(result['skill_overlap_percent'])
        self.assertEqual(result['requirements'][0]['category'], 'uncertain')

    async def test_explicit_and_conflicting_labels_preserve_score(self):
        token, resume_id = await self.seed()
        description = 'Python is required. Docker is optional. Java is not required. SQL is required. SQL is optional.'
        status, result = await self.request('POST', f'/resumes/{resume_id}/compare-job', token,
                                            payload={'job_description': description})
        self.assertEqual(status, 200)
        self.assertEqual(result['skill_overlap_percent'], 75.0)
        rows = {row['skill']: row for row in result['requirements']}
        self.assertEqual({skill: row['category'] for skill, row in rows.items()},
                         {'Python': 'required', 'Docker': 'optional', 'Java': 'not_required', 'SQL': 'uncertain'})
        self.assertEqual([item['text'] for item in rows['SQL']['evidence']],
                         ['SQL is required.', 'SQL is optional.'])
        self.assertTrue(all(item['text'] in description for row in rows.values() for item in row['evidence']))
