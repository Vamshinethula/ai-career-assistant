"""Run from backend: python -m evaluation.evaluate_skills.

Synthetic development cases, not a held-out or real-world accuracy benchmark.
Expected labels describe skill mentions, including explicitly negated mentions.
"""

import json
from pathlib import Path

from app.services.skill_extractor import extract_skills


def evaluate() -> dict:
    cases = json.loads(Path(__file__).with_name('skill_cases.json').read_text(encoding='utf-8'))
    report = {}
    for group in ('supported', 'limitation'):
        results = []
        true_positives = false_positives = false_negatives = 0
        for case in cases:
            if case['group'] != group:
                continue
            expected = set(case['expected'])
            actual = set(extract_skills(case['text']))
            true_positives += len(actual & expected)
            false_positives += len(actual - expected)
            false_negatives += len(expected - actual)
            results.append({'id': case['id'], 'extra': sorted(actual - expected),
                            'missing': sorted(expected - actual)})
        predicted = true_positives + false_positives
        relevant = true_positives + false_negatives
        report[group] = {
            'cases': len(results),
            'exact_matches': sum(not row['extra'] and not row['missing'] for row in results),
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'precision': true_positives / predicted if predicted else None,
            'recall': true_positives / relevant if relevant else None,
            'mismatches': [row for row in results if row['extra'] or row['missing']],
        }
    return report


if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
