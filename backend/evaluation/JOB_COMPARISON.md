# Job-description comparison baseline

The [explicit requirement classifier](REQUIREMENTS.md) is now implemented as a
separate experimental service, now included as labels/evidence in the comparison
endpoint and dashboard. It does not affect scores. Historical evaluation results
below describe the mention baseline.

Input: owner-protected stored resume text and 1-10,000 characters of pasted job
description. Output: canonical job skills, shared terms, terms not detected in
the resume, text availability and nullable overlap percentage.

The existing deterministic extractor runs on both texts. The denominator is
the number of unique catalog skills detected in the job description. Duplicate
mentions do not add weight. Score = 100 * shared terms / job terms, rounded to
one decimal. No readable resume text or no job terms yields null, not a score.
Readable text with no shared terms yields zero. Neither input is sent to an
external AI provider; job text/results are not persisted. No new dependencies.

## Synthetic evaluation and checks

Run from backend: `python -m unittest discover -s tests -p test_job_comparison.py -q`.
Six tests cover:

- Python/Fast API against Python/python/FastAPI/Docker -> 66.7%, Docker undetected.
- Missing resume text and unknown job terms -> null; disjoint terms -> 0%; identical terms -> 100%.
- JavaScript against Java Script and Java -> 50%, Java undetected.
- Actual HTTP upload/comparison -> 200 and unchanged saved resume text.
- Other-owner/missing resume -> 404; missing token -> 401.
- Blank/missing/null/10,001-character input -> 422; 10,000 characters accepted.

Browser evidence additionally covers stale-result clearing, network failure and
retry, temporary text reset and mobile layout. These are development examples,
not representative hiring data or an accuracy benchmark.

## Context evaluation checkpoint - 2026-09-18

Run `python -m evaluation.evaluate_jobs` from backend. The versioned synthetic
fixtures are in job_cases.json. The command exits nonzero for keyword-contract
regressions; required-only interpretation gaps are reported separately and do
not imply the existing mention-based contract failed. The backend test suite
also runs the keyword-contract checks.

| Check | Result |
| --- | --- |
| Existing keyword behavior | 16/16 cases pass |
| Required-only interpretation, exact skill sets | 5/12 cases |
| Required-only probe true positives / false positives / false negatives | 12 / 7 / 1 |
| Required-only probe precision / recall | 63.2% / 92.3% |

These metrics ask what happens if someone incorrectly treats every detected
mention as a required skill. They do not measure a required-skill classifier
(none exists), candidate quality, or real-world accuracy. Labels were authored
for these development examples, not independently adjudicated or held out.

Observed gaps: optional/preferred and explicitly non-required terms still count;
ordinary-word React can be a false technical match; required Kotlin is absent
from the catalog. Negated resume experience can still yield 100% keyword overlap.
The job-side required-only metrics do not capture that resume-side context error.

Decision: retain the documented keyword score and add an explicit equal-weight
explanation beside results. Do not remove every skill near 'not': counterexamples
'not optional' and 'not only Python but also SQL' express requirements. No score
improvement is claimed in this checkpoint. Before introducing classification,
define required/optional/negated/uncertain outputs and test a broader independent
set, including cross-sentence scope and contradictory mentions.

## Remaining limits

The extractor matches mentions only. For example, 'Python is not required' still
detects Python, 'react quickly' can detect React, and Kotlin is outside the
current catalog. It does not infer seniority, years of experience, proficiency,
required/optional distinctions or transferable skills. A missing term is not
evidence of a skill deficit. Review original text before acting on the output.

Before semantic/LLM matching, collect representative synthetic cases covering
negation, optional criteria and catalog gaps, define expected structured results,
and assess privacy/cost. This feature is an explainable baseline, not AI advice.
