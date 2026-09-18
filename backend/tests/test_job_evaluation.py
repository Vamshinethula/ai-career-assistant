import unittest

from evaluation.evaluate_jobs import evaluate


class JobEvaluationTests(unittest.TestCase):
    def test_synthetic_keyword_contract_has_no_regressions(self):
        report = evaluate()
        contract = report['keyword_contract']
        self.assertGreater(contract['cases'], 0)
        self.assertEqual(contract['failures'], [])
        self.assertEqual(contract['passed'], contract['cases'])
