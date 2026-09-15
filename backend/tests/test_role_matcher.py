import unittest

from app.services.role_matcher import ROLE_PROFILES, match_roles
from app.services.skill_extractor import SKILL_ALIASES


class RoleMatcherTests(unittest.TestCase):
    def test_partial_overlap_explains_score(self):
        result = next(row for row in match_roles(['Python', 'SQL'])
                      if row['role_id'] == 'python_backend')
        self.assertEqual(result['skill_overlap_percent'], 40.0)
        self.assertEqual(result['matched_skills'], ['Python', 'SQL'])
        self.assertEqual(result['not_detected_skills'], ['Docker', 'FastAPI', 'Git'])

    def test_full_profile_ranks_first(self):
        result = match_roles(['Python', 'FastAPI', 'SQL', 'Git', 'Docker'])
        self.assertEqual(result[0]['role_id'], 'python_backend')
        self.assertEqual(result[0]['skill_overlap_percent'], 100.0)
        self.assertEqual(result[0]['not_detected_skills'], [])
        scores = [row['skill_overlap_percent'] for row in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_duplicates_and_unrelated_skills_do_not_change_scores(self):
        self.assertEqual(match_roles(['Python', 'Python', 'Kubernetes', 'Unknown']),
                         match_roles(['Python']))

    def test_no_overlap_returns_no_matches(self):
        for skills in ([], ['Kubernetes'], ['Unknown']):
            self.assertEqual(match_roles(skills), [])

    def test_equal_scores_have_stable_order(self):
        result = match_roles(['Git'])
        ids = [row['role_id'] for row in result]
        self.assertEqual(ids, sorted(ids))
        self.assertTrue(all(row['skill_overlap_percent'] == 20.0 for row in result))

    def test_catalog_is_unique_and_uses_extractable_skills(self):
        self.assertEqual(len({role['role_id'] for role in ROLE_PROFILES}), len(ROLE_PROFILES))
        for role in ROLE_PROFILES:
            self.assertTrue(role['skills'])
            self.assertEqual(len(role['skills']), len(set(role['skills'])))
            self.assertTrue(set(role['skills']) <= SKILL_ALIASES.keys())


if __name__ == '__main__':
    unittest.main()
