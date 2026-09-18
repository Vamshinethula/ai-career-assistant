# ERRORS_AND_FIXES.md — AI Career Assistant

## 2026-09-18 - Saved timestamp and history-state verification

Initial saved snapshot API test failed because POST returned created_at with Z while SQLite-backed GET omitted timezone. Added UTC normalization to SavedComparisonSummary. The same test and all 77 backend tests now pass; no existing account/resume timestamps modified.

Lint flagged synchronous state resets in the saved-history effect. Moved resets to action handlers and clear errors after successful async loads. Lint and both browser workflows pass without warnings.

## 2026-09-18 - Node test runner sandbox restriction

Initial npm test failed with Error: spawn EPERM as Node attempted to spawn the test worker. Approved execution outside the sandbox passed all three tests without source changes. Lint and both builds also passed. Lesson: Node built-in tests can require the same process permissions as Vite in this environment.

## 2026-09-18 - Browser helper variable scope

New label-review test failed with Error: Browser evaluation failed on a repeated helper call. The helper declared top-level const choice repeatedly in the same Chrome evaluation context. Wrapped the helper body in an immediately invoked function to give each call its own scope. Verified both normal/demo complete workflows pass. Application source did not require a fix. Lesson: repeated debugger evaluations can share lexical state.

## 2026-09-17 - Browser disclosure activation check

New Chrome test failed AssertionError: Keyboard expands skill review; waiting instead produced Timed out: keyboard expands skill review. Synthetic Enter events did not open the native details control in this run. Added explicit focused-summary assertion and used standard Space activation. Both normal/demo browser workflows then passed, including checkbox keyboard toggles and reset checks. No application workaround needed. Root cause is narrowed to the test activation sequence; manual Enter behavior remains unverified. Lesson: verify focus and distinguish supported keyboard paths from synthetic-event assumptions.

## 2026-09-17 - Demo build sandbox restriction

Initial npm run build:demo failed with Error: spawn EPERM while loading Vite configuration. This matches the existing sandbox child-process restriction. Approved execution outside the sandbox passed for demo and normal builds without application fixes. Both browser workflows also passed. Lint passed inside the sandbox.

## 2026-09-17 - Recovery test execution and discovery

Initial test execution failed with PermissionError: [WinError 5] Access is denied under Python's temporary directory; upload tests also returned 500 when temporary storage was inaccessible. Approved execution outside the sandbox passed without application changes. No production-data fix was needed.

The first recovery-test import exposed ResumeFlowTests directly, so unittest also discovered its three tests in the new module (five tests instead of two). Changed to a module import and reused its driver methods through that module. Verified targeted run: exactly 2 tests, OK; full suite: 60 tests, OK. Lesson: distinguish execution restrictions from app failures and avoid exposing imported TestCase classes to discovery.

## 2026-09-10 - Verification environment and bcrypt warning

- Build error: `Error: spawn EPERM` in Vite config loading under the sandbox. Re-ran the same build with approved escalation; build passed. Cause: sandbox child-process restriction, not application source.
- Existing dependency warning during hashing: `(trapped) error reading bcrypt version`, followed by `AttributeError: module 'bcrypt' has no attribute '__about__'`. Passlib expects metadata absent from the installed bcrypt package. Registration and password verification both passed in isolation. Warning remains open for a separate dependency maintenance checkpoint; no dependency fix attempted. Lesson: distinguish a trapped compatibility warning from a failed request.

## 2026-09-10 - Port 5173 already in use

Status: existing server verified; second startup correctly rejected.

User-reported error: Error: Port 5173 is already in use.

Cause: starting a second server with --strictPort while a process already listens on 5173. The existing server returned HTTP 200 and served the newly edited frontend module, confirming it serves this project.

Action: use http://127.0.0.1:5173/ without starting another server. No process was killed. Lesson: one development server is enough; strictPort prevents silently selecting a different port.

---


## 2026-09-10 - Node.js and npm unavailable in the terminal

Status: resolved for this session.

Error: node and npm each returned 'The term ... is not recognized as the name of a cmdlet, function, script file, or operable program.'

Evidence: command lookup failed and common Node.js installation paths were absent. Installed OpenJS.NodeJS.LTS with winget, then added C:\Program Files\nodejs to the current tool process PATH.

Verified result: node --version returned v24.19.0; npm.cmd --version returned 11.17.0; dependency installation, build, and lint succeeded.

Lesson: existing terminals may retain the old PATH after installation. Restart VS Code to inherit the updated PATH, or add the installation path for the current terminal. npm.cmd explicitly selects the Windows command wrapper.

---


Track meaningful technical errors, their root causes, fixes, and lessons.

Do not remove old resolved errors. They prevent repeated mistakes.

---

## E-001 — Postman Cloud Agent Could Not Reach Localhost

**Status:** Resolved

**Context:** Testing local FastAPI API from Postman Web.

**Error:**
`Cloud agent error: cannot send request`

**Root cause:**
Postman Cloud Agent cannot directly send requests to a service running on the local machine at `127.0.0.1`.

**Fix:**
Use Postman Desktop / Desktop Agent.

**Verified result:**
Local API requests subsequently succeeded.

**Lesson:**
Localhost services require a client running with access to the local computer/network.

---

## E-002 — Resume Upload Returned 401

**Status:** Resolved

**Endpoint:**
`POST /resumes/upload`

**Response:**
```json
{
  "detail": "Not authenticated"
}
```

**Root cause:**
Resume endpoint is protected and no bearer JWT was provided.

**Fix:**
1. Log in.
2. Copy `access_token`.
3. In Postman choose Authorization -> Bearer Token.
4. Paste the token into Token field.

**Verified result:**
Authenticated PDF upload returned `201 Created`.

**Lesson:**
Protected routes require authentication credentials on every request unless the client automatically manages them.

---

## E-003 — DOCX Resume Upload Rejected

**Status:** Expected behavior, not a bug

**Response:**
`400 Bad Request`

```json
{
  "detail": "Only PDF resumes are allowed"
}
```

**Cause:**
Current requirement intentionally supports PDF only.

**Action:**
No fix needed.

**Lesson:**
A 4xx response may mean validation is working correctly, not that the application is broken.

---

## E-004 — `.venv` Accidentally Picked Up by Git

**Status:** Needs repository re-verification

**Context:**
During early Git setup, many `.venv/Lib/site-packages/...` files appeared and produced LF -> CRLF warnings.

**Root cause:**
Virtual environment files were included/staged before ignore rules were correctly established.

**Expected prevention:**
`.gitignore` should include:
```gitignore
.venv/
__pycache__/
*.pyc
*.db
uploads/
.env
```

**Required verification:**
Run:
```bash
git status
git ls-files
```
and ensure `.venv` is not tracked.

**Lesson:**
Generated environments, secrets, runtime DB files, and uploaded user files generally should not be version-controlled.

---

# Template for Future Errors

## E-XXX — Short error title

**Date:**

**Status:** Open / Resolved / Expected behavior

**Task:**

**Exact error:**
```text
...
```

**Where it happened:**

**Root cause:**

**Evidence:**

**Fix attempted:**

**Verified result:**

**Prevention:**

**Lesson learned:**

## 2026-09-11 - Resume debug output and upload cleanup review

Source inspection found print(resume_text) in the upload success path. Removed it to prevent private resume content appearing in terminal logs; source removal verified, live upload not rerun. Also found metadata committed before parsing: parser failure rolls back only the later transaction and deletes the PDF, potentially leaving the previously committed row. Status: open, identified by source inspection; runtime reproduction and targeted transaction fix are next. The Vite spawn EPERM sandbox restriction recurred; approved build outside sandbox passed.


## 2026-09-11 - Failed resume upload cleanup resolved in isolated tests

Context: direct upload-route regression tests using in-memory SQLite and synthetic PDFs.
Exact errors: AssertionError: 1 != 0 after injected parser failure; leftover file assertion after partial disk write; PermissionError: [WinError 32] during corrupt-PDF cleanup.
Root causes: metadata committed before parsing; no partial-write deletion; PyMuPDF filename parsing retained a Windows file handle when malformed-file opening failed.
Fix: parse before one commit, flush and validate response before committing; delete partial writes; open PDF from bytes and close document using a context manager.
Verified: six tests pass, covering success and five failure scenarios. Earlier open transaction-cleanup entry is superseded. Live browser upload after fix is not yet retested.
Prevention: keep regression tests and avoid committing incomplete records. Disk and database cannot be made crash-atomic by rollback alone.
Test environment: initial sandbox run could not access temporary directories (WinError 5). Approved execution outside sandbox enabled reproduction and passing verification. No personal database or resume files used.

## 2026-09-11 - Detail schema declared before parent

Exact error: NameError: name 'ResumeResponse' is not defined.
Context/root cause: first patch placed ResumeDetailResponse above its parent in schemas.py; backend test imports failed.
Fix: moved the subclass below ResumeResponse.
Verified: same unittest discovery command now passes all 13 tests.
Lesson: Python resolves base classes when executing the class declaration; define the parent first. Use precise patch context when multiple classes share Config blocks.

## 2026-09-11 - Postman resume ID placeholder

Context: user sent GET /resumes/<your-resume-id>/skills literally.
Exact response: 422, type int_parsing, loc path/resume_id, Input should be a valid integer.
Root cause: placeholder was not replaced with an actual resume ID; earlier instructions needed clearer substitution guidance.
Fix: GET /resumes with the same bearer token, take a resume's id (not user_id), insert the number into /resumes/NUMBER/skills with no angle brackets.
Verified: user reported the Postman test passed after correction.
Lesson: distinguish documentation placeholders from actual URL values. No application code fix required.

## 2026-09-11 - Overlapping Java Script alias

Context: synthetic evaluation before modifying the matcher.
Observed: Java Script and Angular returned Angular, Java, JavaScript; expected Angular, JavaScript.
Root cause: each alias matched independently; Java matched inside the spaced JavaScript alias.
Fix: gather alias spans and accept longer nonoverlapping spans first. Separate mentions still match.
Verified: evaluation supported exact sets improved 12/13 to 13/13; dedicated overlap and full regression tests pass (24 tests).
Prevention: retain the evaluation fixture and a separate-Java regression. Ordinary-word React ambiguity and uncatalogued Kotlin remain limitations, not resolved by this fix.

## 2026-09-14 - Existing bcrypt warning reconfirmed

During full API-flow tests, the previously documented Passlib warning recurred: AttributeError: module 'bcrypt' has no attribute '__about__'. Registration, correct-password login and wrong-password rejection passed; all 35 tests passed. Status remains open for dependency maintenance. No suppression or dependency change was made.

## 2026-09-15 - Browser test port collision

Exact error: Port 8000 is in use; stop its dev server before this test.
Context: first browser-smoke attempt tried to reserve the normal backend port.
Cause: an existing application server occupied it; sandbox listener inspection did not reveal it.
Fix: isolated test backend now uses port 8001; only the temporary Chrome session redirects its API requests. Existing server was not stopped.
Verified: rerun completed the actual browser workflow with PASS/exit 0 and cleaned up temporary processes/data.
Lesson: do not assume missing process-list output means a port is free; check binding and isolate tests from normal services.

## 2026-09-15 - Passlib/bcrypt warning resolved

Exact reproduced error: AttributeError: module 'bcrypt' has no attribute '__about__', under (trapped) error reading bcrypt version.
Root cause: installed Passlib 1.7.4 wrapper expects metadata absent in bcrypt 4.3.0.
Fix: use bcrypt directly, keep algorithm/cost and legacy verification semantics, remove Passlib requirement. Validate new password lengths before hashing.
Verified: 40 backend tests pass with no metadata warning; legacy synthetic hashes and HTTP login succeed; build/lint and Chrome password-validation/full-flow test pass. This supersedes prior open warning entries.
Prevention: compatibility fixtures and explicit byte-limit tests. Existing account hashes and database untouched.
Editing note: requirements.txt was UTF-16 and rejected by the UTF-8 patch tool; read with BOM detection and saved as UTF-8 while removing only the Passlib pin. No dependency upgrades performed.

## 2026-09-16 - Corrupt PDFs now return client errors

Previously verified behavior: invalid PDF content raised a parser error mapped to 500.
Change: known invalid/password-protected cases now raise InvalidResumePDF and return 400; page limits return 413. Unexpected parser/storage failures retain 500.
Verified: updated corrupt-PDF direct/API tests pass; new boundary/encryption tests confirm no leftover files/rows. Chrome checks corrupt/over-page-limit rejection and successful retry with another file.
Lesson: invalid user input should be distinguishable from an internal server failure. This supersedes historical documentation of corrupt-PDF 500 responses.

## 2026-09-16 - Frontend verification sandbox restrictions repeated

Build reproduced `Error: spawn EPERM`; browser smoke timed out at `http://127.0.0.1:5173/` while starting Vite under the sandbox. Existing child-process restrictions were the likely cause; same commands with approved escalation passed without source changes. Verified build and full Chrome keyboard/workflow checks. Lesson: separate tool execution restrictions from application failures.

## 2026-09-16 - CORS test client dependencies

New CORS test import failed: `The starlette.testclient module requires the httpx2 package to be installed.` An attempted httpx import also failed (`No module named 'httpx'`). Inspection showed existing API tests use direct ASGI requests. Reused that approach instead of adding packages. Verified all 55 backend tests pass. Lesson: inspect existing test infrastructure before choosing a helper.

## 2026-09-16 - Isolated frontend lint scanned dependencies

Context: clean-install verification source copy omitted frontend/.gitignore. Lint emitted dependency warnings such as `eslint(no-unused-expressions)` under node_modules/react-dom. Root cause: incomplete verification copy, not application code. Copied the existing .gitignore and reran lint; exit 0 with no warnings. Prevention: include configuration and ignore files when reproducing an installation.
