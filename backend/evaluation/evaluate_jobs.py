"""Synthetic contract checks and separate required-skill interpretation probes.

Run from backend: python -m evaluation.evaluate_jobs
Exit nonzero on keyword-contract regressions. Semantic gaps are reported, not
silently redefined as passing required-skill classification.
"""
import json
from pathlib import Path

from app.services.job_comparison import compare_job_description


def evaluate() -> dict:
    cases = json.loads(Path(__file__).with_name('job_cases.json').read_text(encoding='utf-8'))
    failures = []
    context_results = []
    true_positives = false_positives = false_negatives = 0
    for case in cases:
        actual = compare_job_description(case['resume'], case['job'])
        if (actual['job_skills'] != case['expected_job_skills']
                or actual['skill_overlap_percent'] != case['expected_score']):
            failures.append({'id': case['id'], 'actual': actual,
                             'expected_job_skills': case['expected_job_skills'],
                             'expected_score': case['expected_score']})
        if 'required_skills' not in case:
            continue
        expected = set(case['required_skills'])
        predicted = set(actual['job_skills'])
        true_positives += len(predicted & expected)
        false_positives += len(predicted - expected)
        false_negatives += len(expected - predicted)
        context_results.append({
            'id': case['id'],
            'extra_if_interpreted_as_required': sorted(predicted - expected),
            'missing_required': sorted(expected - predicted),
        })
    mismatches = [row for row in context_results
                  if row['extra_if_interpreted_as_required'] or row['missing_required']]
    predicted_count = true_positives + false_positives
    expected_count = true_positives + false_negatives
    return {
        'dataset': 'synthetic development examples, not held-out hiring data',
        'keyword_contract': {'cases': len(cases), 'passed': len(cases) - len(failures),
                             'failures': failures},
        'required_only_interpretation_probe': {
            'cases': len(context_results), 'exact_matches': len(context_results) - len(mismatches),
            'true_positives': true_positives, 'false_positives': false_positives,
            'false_negatives': false_negatives,
            'precision': true_positives / predicted_count if predicted_count else None,
            'recall': true_positives / expected_count if expected_count else None,
            'mismatches': mismatches,
        },
    }


if __name__ == '__main__':
    report = evaluate()
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if report['keyword_contract']['failures'] else 0)
