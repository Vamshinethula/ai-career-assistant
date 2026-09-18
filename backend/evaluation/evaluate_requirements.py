"""Synthetic conservative-policy evaluation, not independent accuracy evidence."""
import json
from pathlib import Path

from app.services.job_requirements import classify_job_requirements


def evaluate() -> dict:
    cases = json.loads(Path(__file__).with_name('requirement_cases.json').read_text(encoding='utf-8'))
    report = {}
    for group in ('development', 'review'):
        selected = [case for case in cases if case['group'] == group]
        mismatches = []
        assigned = uncertain = 0
        for case in selected:
            actual = {row['skill']: row['category'] for row in classify_job_requirements(case['text'])}
            assigned += sum(category != 'uncertain' for category in actual.values())
            uncertain += sum(category == 'uncertain' for category in actual.values())
            if actual != case['expected']:
                mismatches.append({'id': case['id'], 'expected': case['expected'], 'actual': actual})
        report[group] = {'cases': len(selected), 'exact_policy_matches': len(selected) - len(mismatches),
                         'classified_skills': assigned, 'uncertain_skills': uncertain,
                         'mismatches': mismatches}
    return report


if __name__ == '__main__':
    report = evaluate()
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if any(group['mismatches'] for group in report.values()) else 0)
