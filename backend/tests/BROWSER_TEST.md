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
