import unittest

from app.services.job_requirements import classify_job_requirements
from evaluation.evaluate_requirements import evaluate


class JobRequirementsTests(unittest.TestCase):
    def test_declared_policy_cases(self):
        for group, result in evaluate().items():
            with self.subTest(group=group):
                self.assertEqual(result['mismatches'], [])

    def test_conflict_retains_both_source_fragments(self):
        rows = classify_job_requirements('Python is required. Python is optional.')
        self.assertEqual(rows, [{'skill': 'Python', 'category': 'uncertain', 'evidence': [
            {'text': 'Python is required.', 'category': 'required'},
            {'text': 'Python is optional.', 'category': 'optional'},
        ]}])

    def test_repeated_fragment_is_not_repeated_evidence(self):
        rows = classify_job_requirements('Git is required. Git is required.')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['category'], 'required')
        self.assertEqual(len(rows[0]['evidence']), 1)

    def test_aliases_remain_canonical_and_evidence_is_original(self):
        rows = classify_job_requirements('  Required: Java Script and Fast API  ')
        self.assertEqual([row['skill'] for row in rows], ['FastAPI', 'JavaScript'])
        self.assertTrue(all(row['evidence'][0]['text'] == 'Required: Java Script and Fast API' for row in rows))

    def test_empty_input_has_no_invented_skills(self):
        self.assertEqual(classify_job_requirements(' \n '), [])
