# CHANGELOG.md — AI Career Assistant

## 2026-09-15 - Environment-based JWT configuration

- Removed hardcoded active signing key; added private dotenv/environment configuration and startup validation.
- Added non-overwriting local key generator, safe example file and isolated test keys; installed python-dotenv 1.2.3.
- Forty-four backend tests and Chrome workflow pass; documented session invalidation and setup steps.


## 2026-09-15 - Project setup documentation

- Added root README with setup, architecture, demo, API, tests and known limitations.
- Replaced frontend starter README with project-specific guidance.
- Verified local links, installed requirement pins and dependency consistency; fresh-machine setup not tested.


## 2026-09-15 - Resolve Passlib/bcrypt warning

- Use bcrypt directly with existing hash format/cost; remove Passlib requirement.
- Preserve legacy long-password verification; validate new registrations at 72 UTF-8 bytes with readable frontend feedback.
- Added synthetic compatibility fixtures and regression/browser checks. Forty backend tests, build/lint and Chrome smoke pass. No database/hash migration.


## 2026-09-15 - Real browser smoke verification

- Added repeatable Chrome workflow test using actual frontend/backend with isolated data.
- Verified account creation through role results, network failure/retry, mobile overflow and logout.
- Documented test setup and limits; existing normal server and personal data preserved.


## 2026-09-14 - Verify complete API workflow

- Added isolated HTTP workflow tests spanning registration through role results and cross-user isolation.
- Verified wrong-login/missing-auth/corrupt-upload failure paths; all 35 backend tests pass.
- Existing bcrypt warning remains unresolved; browser end-to-end verification pending.


## 2026-09-14 - Dashboard role overlaps

- Added on-demand illustrative role results with scores, counts, matched/not-detected skills and clear limitations.
- Added loading/retry/error/session handling and separate empty states.
- Frontend build/lint and isolated client checks pass; browser verification pending.


## 2026-09-11 - Illustrative role matching API

- Added four local example role profiles and explainable skill-overlap scoring.
- Added protected matches endpoint and structured role responses, with matched/not-detected terms.
- All 33 backend tests pass; frontend integration is next. No schema migration, external API or dependency change.


## 2026-09-11 - Evaluate skill matcher

- Added synthetic evaluation cases, metrics runner and documented before/after results.
- Fixed overlapping Java Script/Java aliases while preserving separate mentions.
- All 24 backend tests pass; two catalog/context limitation probes remain documented.


## 2026-09-11 - Display extracted skills

- Added per-resume View skills/Hide skills with loading/retry/error states and plain-language limitations.
- Distinguished no readable text from no catalog matches; validated skills API responses.
- User confirmed backend Postman test. Frontend build/lint and client checks pass; browser verification pending.


## 2026-09-11 - Local skill extraction endpoint

- Added deterministic skill-matching service and protected per-resume skills endpoint.
- Reused ownership lookup; structured response distinguishes no text from no catalog matches.
- All 22 backend tests pass. Frontend integration is next; no external service, dependency or database change.


## 2026-09-11 - View extracted resume text

- Added owner-protected resume detail endpoint and nullable text response schema.
- Added View text/Hide text with plain-text display, empty/loading/error/retry states.
- User confirmed prior resume-list browser milestone; text-view browser check pending. Thirteen backend tests, build/lint and client checks pass.


## 2026-09-11 - List uploaded resumes

- Added authenticated, ownership-filtered GET /resumes with metadata-only response.
- Dashboard displays filenames and reloads list after successful upload; handles empty/loading/error states.
- Nine backend tests, frontend build/lint and client checks pass; browser verification pending.


## 2026-09-11 - Fix failed-upload cleanup

- Defer database commit until parsing and response validation succeed; remove partial writes.
- Parse PDF bytes with a context manager to avoid filesystem locks on corrupt PDFs.
- Added six passing isolated upload regression tests; preserved existing user data.


## 2026-09-11 - Browser verification

- User confirmed successful resume upload through the frontend.
- Both local servers started and responded with HTTP 200; no application code changed for this verification.


## 2026-09-11 - Dashboard PDF upload

- Added authenticated multipart upload client and dashboard file form with pending/success/error feedback.
- Removed backend resume-text debug output.
- Build/lint and isolated API client checks passed; browser end-to-end verification pending.


## 2026-09-10 - Load authenticated user dashboard

- Replaced temporary login-success screen with profile dashboard, loading/error/retry/logout behavior.
- Added authenticated GET support in existing API client, status-aware errors and cancellation.
- Added session reset on profile 401; extended local CORS for GET and Authorization.
- Build/lint and isolated client/backend tests passed; browser checks pending.

## 2026-09-10 - Login form and local session state

- Added LoginForm with controlled inputs, pending state and error feedback.
- Extended existing API service with shared JSON POST handling and login response validation.
- App stores token in memory and offers logout; registration feedback points to login.
- Build/lint and isolated API/client checks passed. Browser interaction pending.

## 2026-09-10 - Connect registration to FastAPI

- Added registration API client with timeout and readable HTTP/network failures.
- Added pending state, real submission and success feedback to RegisterForm.
- Allowed JSON POST requests from the two local Vite origins in FastAPI.
- Build/lint and isolated backend/client checks passed; browser verification pending.

## 2026-09-10 - Registration form UI

- Added RegisterForm component and scoped form styles, composed in App.jsx.
- Added controlled full name/email/password inputs, browser validation, and explicit local-only submit feedback.
- Verified build/lint and HTTP module delivery. Manual browser checks pending; account creation/API integration not implemented.

---


## 2026-09-10 - Welcome page

- Replaced Vite demo component/styles with a static AI Career Assistant welcome page and planned-feature overview.
- Updated browser title.
- Build/lint passed; updated HTML and module served over HTTP 200. Visual check pending.
- Recorded user confirmation that the previous starter counter worked.

---


## 2026-09-10 - Frontend starter

- Added official React + Vite JavaScript starter under frontend/, alongside backend/.
- Installed Node.js LTS 24.19.0, npm 11.17.0, and frontend dependencies; generated package-lock.json.
- Verified production build, lint, HTTP 200 for the development page and App module, and Git exclusion of node_modules/dist.
- Browser rendering/counter verification remains pending. Backend code unchanged; no commit created.

---


Record meaningful project changes, not every tiny edit.

---

## Existing Project History

### Backend foundation
- Created FastAPI backend structure.
- Added database layer.
- Added user registration.
- Added password hashing.
- Added login.
- Added JWT generation/verification.
- Added protected current-user route.

### API testing
- Confirmed root endpoint.
- Confirmed login.
- Confirmed protected user endpoint.
- Confirmed unauthorized behavior.

### Resume upload
- Added authenticated resume upload.
- Added PDF-only validation.
- Added local upload storage.
- Added resume database records.
- Confirmed PDF upload returns `201 Created`.
- Confirmed DOCX is rejected with `400 Bad Request`.

### Resume parsing
- Added/created resume parsing service in repository.
- Extracted text from PDF.
- Added persisted `resume_text`.
- Confirmed extracted text visible in SQLite Viewer.

### Development priority change
- Paused skill-extraction work.
- Chose to begin frontend development using React + Vite + JavaScript.

---

# Template

## YYYY-MM-DD

### Added
-

### Changed
-

### Fixed
-

### Verified
-
