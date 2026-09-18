# Explicit requirement classification: first service checkpoint

Status: integrated into the HTTP comparison response and dashboard, verified
locally on 2026-09-18. Existing keyword extraction and scores are unchanged.

## Contract

Input: job-description text. Output: one record per detected catalog skill with
`skill`, `category`, and `evidence` (original trimmed fragments and their labels).
No external model, cost, dependency, database writes or persistence.

| Category | Meaning |
| --- | --- |
| required | An explicit supported phrase says the skill is required or not optional |
| optional | An explicit supported phrase says optional or preferred |
| not_required | An explicit supported phrase says not required or no experience required |
| uncertain | No supported cue, unresolved syntax, or conflicting/uncertain occurrences |

`not_required` means absence of a requirement, not a prohibited skill. This name
is deliberately narrower than generic negation. None of the labels certify
proficiency or candidate suitability.

Supported forms: `Required: Python and SQL`, `Preferred skills: Git`,
`Docker is optional`, `Java is not required`, `Python is not optional`, and
`No experience with Docker is required`. Lists must contain known aliases,
commas, ampersands or `and`; other words make the fragment uncertain.

Fragments split at newlines, semicolons and sentence punctuation followed by
whitespace. Periods inside Node.js and React.js are preserved. The service does
not infer heading scope across lines. Contradictory statements or an explicit
statement plus an unclassified mention yield uncertain, preserving all evidence.
Identical fragments are deduplicated. Unknown catalog terms are not emitted.

## Evaluation

From backend:

```text
python -m evaluation.evaluate_requirements
python -m unittest discover -s tests -p test_job_requirements.py -q
```

Results on 2026-09-18: development 12/12 and review 10/10 exact policy matches.
Across both groups, 16 skill records are classified and 16 remain uncertain.
Five classifier unit tests pass, including preserved conflict evidence,
deduplication, canonical aliases and empty input. With API integration and
cross-line alias regressions, the full backend suite has 74 passing tests.

These are authored policy-conformance examples. The review group is separate
from earlier job-comparison fixtures but was created by the same author in this
checkpoint; it is not independent, blinded or real-world accuracy evidence.
An expected uncertain label counts as policy-conformant, not as a solved semantic
classification. Report abstentions alongside exact matches to avoid hiding this.

## Integration and remaining limits

Compound clauses, alternatives (`Python or Java`), cross-line lists, unknown
skills and phrases such as `not only Python but also SQL` remain uncertain.
Catalog ambiguity can still detect ordinary-word React; conservative phrase
rules reduce some misuse but do not solve word sense. Evidence should be shown
for user review. No numerical confidence estimate is provided.

The comparison response includes a required `requirements` list with typed
categories and source evidence. It covers exactly the scoring catalog skills.
When whole-text extraction joins an alias across lines but fragment classification
cannot explain it, the integration returns uncertain with the original input as
evidence rather than changing the score or inventing an explanation. Evidence
may therefore contain the entire submitted text; it remains transient.

The dashboard shows labels and expandable plain-text source snippets even when
resume text is unavailable. The client rejects missing/malformed labels, unknown
categories, inconsistent aggregate labels and evidence absent from submitted text.
Browser tests verify all categories, conflicting evidence, keyboard disclosure,
mobile layout, reset and literal HTML-like text. Ownership tests still pass.
Backend and frontend should be updated together; old responses without the new
field receive a readable unexpected-label error. No database migration is needed.

Users can now select **Your label for [skill]** after reading the source evidence.
The automatic label remains visible, and a separate **Your choice** identifies
the user's interpretation. **Reset label** or **Use automatic label** removes
the choice. All categories, including uncertain, can be selected for any detected
skill. This is transient frontend state: no API submission, database write,
training signal or score change. Editing, comparing again, closing/switching
resumes, refreshing or logging out clears choices. Browser checks verify keyboard
selection, reset, unchanged score, original labels, mobile layout and lifecycle.

Before expanding rules, collect additional
independently labelled examples and measure false definitive labels as well as
uncertain coverage. Do not quietly classify every unspecified skill as required.
