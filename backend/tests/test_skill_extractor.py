import unittest

from app.services.skill_extractor import extract_skills


class SkillExtractorTests(unittest.TestCase):
    def test_explicit_skills_are_sorted_and_unique(self):
        self.assertEqual(extract_skills('Python, SQL, FastAPI. PYTHON and python.'),
                         ['FastAPI', 'Python', 'SQL'])

    def test_aliases_and_pdf_whitespace(self):
        self.assertEqual(extract_skills('ReactJS, React.js, postgres, Node\nJS, Spring\tBoot'),
                         ['Node.js', 'PostgreSQL', 'React', 'Spring Boot'])

    def test_no_matches_inside_longer_words(self):
        self.assertEqual(extract_skills('JavaScript TypeScript MySQL GitHub reaction'),
                         ['JavaScript', 'MySQL', 'TypeScript'])

    def test_punctuation_names_and_separators(self):
        self.assertEqual(extract_skills('(C++), C#; Python/SQL'),
                         ['C#', 'C++', 'Python', 'SQL'])
        self.assertEqual(extract_skills('C+++ C#developer CPython'), [])

    def test_no_text_and_unknown_skills(self):
        for text in (None, '', ' \n\t ', 'Carpentry and public speaking'):
            with self.subTest(text=text):
                self.assertEqual(extract_skills(text), [])

    def test_mentions_are_not_proficiency_claims(self):
        # Documents the baseline's deliberate limitation: it cannot infer negation.
        self.assertEqual(extract_skills('No experience with Python'), ['Python'])

    def test_long_alias_does_not_also_match_shorter_skill(self):
        self.assertEqual(extract_skills('Java Script and Angular'), ['Angular', 'JavaScript'])
        self.assertEqual(extract_skills('Java services and Java Script interfaces'),
                         ['Java', 'JavaScript'])

    def test_supported_evaluation_cases(self):
        from evaluation.evaluate_skills import evaluate
        report = evaluate()['supported']
        self.assertEqual(report['mismatches'], [])


if __name__ == '__main__':
    unittest.main()
