# Browser workflow check

From the project root on Windows, with Node 24+, installed Google Chrome,
frontend dependencies and the backend virtual environment:

```powershell
node backend/tests/browser_smoke.mjs
```

If Node is not on the terminal PATH:

```powershell
& 'C:\Program Files\nodejs\node.exe' backend/tests/browser_smoke.mjs
```

Set `CAREER_TEST_CHROME` to a different Chrome executable path if necessary.
Ports 8001 and 9223 must be free. The script reuses an existing frontend on
127.0.0.1:5173 or starts this project's Vite server there. That existing server
must serve this project. Existing servers are not stopped.

The test launches the actual FastAPI application with an in-memory database
configured and migrated before application import, temporary upload storage, and a synthetic
PDF. A separate headless Chrome profile redirects its API requests from port
8000 to the isolated server on 8001 using Chrome's debugging protocol. The
normal backend and browser session are untouched. Actual application CORS rules
remain in place. Only processes started by the script and its uniquely created
temporary directory are cleaned up. Do not interrupt cleanup unnecessarily.

The test uses real React forms, JWT authentication, multipart upload and PDF
parsing. It checks registration/login, dashboard profile, list refresh, extracted
text, skills, role percentages/counts, blocked-request error and retry, logout,
and horizontal overflow at a 390-pixel viewport. Success prints one PASS line
and exits 0. Failures exit nonzero; a timeout identifies the stalled step.

This is an automated browser smoke test, not a comprehensive visual,
accessibility, performance or security audit. It redirects requests through a
debugger and does not validate deployment networking. It requires no new npm or
Python package. The password implementation now uses bcrypt directly; the
Passlib metadata warning was resolved on 2026-09-15. Registration rejects
passwords over 72 UTF-8 bytes, and this browser test checks that feedback before
registering with a valid password. Child-process logs are suppressed; use the
API test suite to inspect backend warnings directly.

Keyboard checkpoint: real Tab/Enter events verify the first-focus skip link is visible, activates workspace focus, and leads to the registration input. This does not replace screen-reader or comprehensive accessibility testing.

Demo checkpoint: set CAREER_TEST_DEMO=true before running the script to start
an isolated Vite demo server on port 5174 (which must be free). The test backend
allows that exact origin; it does not modify the normal backend configuration.
Checks assert the synthetic-data/reset notice before and after login, then run
the complete workflow and mobile check. Without this setting, the normal test
asserts that the demo notice is absent. Clear the variable afterward.

Skill review checkpoint: Space opens the role disclosure, Space toggles the
focused checkbox, reviewed counts update without changing role scores, and
reopening role overlaps resets the checklist. A fully matched profile shows
evidence-review guidance without checkboxes. The expanded checklist is included
in the mobile overflow check. Both normal and demo modes pass these checks.

Job comparison checkpoint: synthetic pasted text returns 66.7% and Kubernetes
not detected; whitespace is rejected, uncatalogued text has no score, editing
clears stale results, blocked requests show feedback and can be retried, and
closing/reopening clears pasted text/results. The form is included in the mobile
overflow check. API tests separately cover length limits and ownership.

Requirement labels: verify required, optional/preferred, explicitly not-required
and uncertain labels while overlap stays 75% for the synthetic four-skill case.
Space expands conflicting SQL source statements. Closing clears labels/evidence;
HTML-like input displays literally without creating an image or executing code.
Both normal and demo browser modes pass these checks.

User-label review: native select keyboard interaction changes an uncertain SQL
label to the user's Required choice while the automatic label and 75% score
stay visible. Reset clears it; repeat comparison, editing and closing also clear
temporary choices. Mobile layout is checked with a choice displayed.

Export checkpoint: force a temporary Blob-URL failure to verify readable feedback,
then allow a real Chrome download into the isolated test directory. Read and parse
the JSON file to verify score, automatic/user label provenance, source evidence
and absence of token/resume-text fields. Cleanup removes the synthetic download.
Closing results removes the export button. Normal/demo modes pass.

Reviewed scoring: confirming SQL shows 100% for 1 of 1 with 3 unreviewed terms, while original overlap remains 75%. Reset removes reviewed score. Downloaded v2 summary has null reviewed score when no Required choice remains.

Saved comparisons: tests save failure/retry, re-login/reopen with original labels, deletion cancellation, blocked deletion request/retry, and removal persisting after refresh. Both normal and CAREER_TEST_DEMO=true runs pass on 2026-09-18.

Pagination verification (2026-09-18): seed eleven synthetic snapshots, refresh, visit Older, verify final-page disabled control, return Newer. Both browser modes pass.

Title search checks: case-insensitive matching, a single matching row, no-match message, and Clear search restoring history. Both normal/demo modes pass on 2026-09-18.
