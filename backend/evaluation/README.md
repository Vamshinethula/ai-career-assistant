# Skill extraction evaluation

Run from `backend/`:

```powershell
.venv/Scripts/python.exe -m evaluation.evaluate_skills
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

`skill_cases.json` contains 15 synthetic, manually labeled development examples.
Labels describe skill mentions, not demonstrated proficiency. A negated mention
still counts under this contract. No personal resumes or external APIs are used.

- `supported`: 13 cases covering common stacks, aliases, PDF whitespace,
  duplicates, punctuation, boundaries and missing text.
- `limitation`: two probes for ordinary-language ambiguity and catalog coverage.
  These are included in the report even though they fail. They are not asserted
  as desired matcher behavior in the regression tests.

Precision = correct matches / all returned matches. Recall = correct matches /
all expected matches. Counts are summed across examples (micro averages).
Undefined ratios are reported as null. Exact match requires the complete skill
set to equal the expected set for one example.

## Results on 2026-09-11

| Group | Before | After |
| --- | --- | --- |
| Supported exact matches | 12/13 | 13/13 |
| Supported precision | 43/44 (97.7%) | 43/43 (100%) |
| Supported recall | 43/43 (100%) | 43/43 (100%) |
| Limitation exact matches | 0/2 | 0/2 |

Fix: `Java Script` previously returned both Java and JavaScript. Prefer longer
overlapping alias spans, while retaining a separate Java mention elsewhere.

Remaining probes: “I react quickly” incorrectly returns React; Kotlin is missed
because it is outside the catalog. Across all 15 cases after the fix, there are
43 correct matches, one incorrect match and one missed skill (97.7% precision
and recall), with 13/15 exact sets. This small, intentionally constructed set is
not representative of a resume population; these figures do not establish
generalization. It is not held out: the fix was developed against these cases.

Future evaluation should add independently labeled examples before tuning,
broaden writing styles/domains, and retain failures for comparison. Adding a
catalog term alone does not solve ordinary-word ambiguity or proficiency.
