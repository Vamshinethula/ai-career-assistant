# CHANGELOG.md — AI Career Assistant

## Feature checkpoint review - 2026-09-18

Reviewed accumulated comparison/requirement/review/export features, demo mode, recovery verification and documentation for Git checkpoint. Latest local evidence: 74 backend tests, 3 frontend tests, lint, normal/demo builds and both Chrome workflows pass. Private data/configuration and generated output are ignored. Preparing commit/push; updated remote CI remains pending. No deployment is part of this checkpoint.

## Export comparison summaries - 2026-09-18

Added browser-only JSON downloads with automatic/user labels, evidence, score meaning and privacy guidance. Added three serializer tests and CI test command; verified actual Chrome downloads and error/retry in both modes, lint and both builds. Backend unchanged; remote workflow run pending.

## Review requirement labels - 2026-09-18

Added per-skill temporary user label selection and reset while preserving automatic evidence and keyword score. Native labelled controls support keyboard input. Verified lint, both builds and both browser workflows including lifecycle resets. No backend or database changes.

## Display job requirement labels and evidence - 2026-09-18

Added typed requirement results to comparison response and dashboard source disclosures. Preserved keyword scores with uncertain fallback for cross-line aliases. Added API/browser regression checks and client evidence validation. Verified 74 backend tests, lint, both builds and both Chrome workflows; no schema migration or dependency change.

## Conservative requirement classification service - 2026-09-18

Added explicit-phrase required/optional/not_required/uncertain classification with original evidence and conflict handling. Added 22 synthetic policy examples, evaluator, documentation and five regression tests. All 72 backend tests pass. Service is not yet integrated into the comparison API or UI; scores unchanged.

## Evaluate job context - 2026-09-18

Added 16 synthetic job-comparison cases, a repeatable evaluator and regression integration. Documented required/optional/negation/catalog gaps and exact metrics. Clarified equal weighting next to UI scores; matching algorithm unchanged. Verified 67 backend tests, lint, demo build and Chrome workflow.

## Compare resumes with job descriptions - 2026-09-17

- Added owner-protected comparison endpoint with bounded input, structured results and null-score empty states.
- Added per-resume pasted-text form with transient results, loading/errors/retry, stale-result clearing and cancellation.
- Reused catalog extraction; no external AI, persistence, schema change or dependencies.
- Verified 66 backend tests, lint, normal/demo builds, both Chrome flows and client validation probes. Documented synthetic evaluation and known contextual limitations.

## Skill review checklist - 2026-09-17

Added per-role expandable next steps with temporary reviewed-term checkboxes and full-overlap guidance. Reuses existing matching results without API/schema changes. Verified lint, both builds and both Chrome workflows including keyboard/count/reset/score/mobile checks. Updated product direction and usage documentation.

## Disposable demo mode - 2026-09-17

- Added demo-only synthetic-data/reset/cold-start notice and dev:demo/build:demo commands.
- Extended isolated Chrome checks for demo notice and normal-mode absence.
- Verified lint, both builds/browser workflows and four migration checks. Recorded user-selected disposable policy and deployment settings. No backend behavior changes or deployment.

## Hosting proposal - 2026-09-17

Added a reviewed candidate deployment layout with build/start commands, configuration, storage-policy choices and hosted verification steps. Corrected current local test count to 60. Provider/data-policy selection remains pending; nothing deployed.

## Offline backup recovery drill - 2026-09-17

- Added two isolated tests for complete same-path SQLite/PDF recovery and incomplete database-only recovery.
- Verified restored login, resume results, ownership and PDF bytes; all 60 backend tests pass on Windows.
- Added recovery runbook and linked migration/deployment guidance. No application changes or real-data restore.

## First remote CI run passed - 2026-09-16

Confirmed working: [Project checks run 35131859172](https://github.com/Vamshinethula/ai-career-assistant/actions/runs/35131859172) completed successfully for pushed commit 1c468db4a8f8c76923e5a6f04926576d86fa5e09. GitHub API verified success for every step in Backend (windows-latest), Backend (ubuntu-latest), and Frontend (Ubuntu). Backend pinned installation, pip check, 58-test suite, fresh migration and model comparison passed on both OS runners. Frontend npm ci, lint and build passed on Ubuntu.

Previous workflow/Linux uncertainty is resolved for these checks. This is not a hosted deployment, browser CI run, or persistence/restore test. No code fix was needed. Working tree was clean at session start; only verification documentation changed. Next: choose deployment data policy/hosting, or verify backup recovery locally before persistent deployment. No host or paid service selected. Documentation changes remain uncommitted.

## Continuous integration workflow added - 2026-09-16

Implemented but unverified on GitHub: .github/workflows/ci.yml runs backend dependency/test/migration checks on Windows and Ubuntu and frontend install/lint/build on Ubuntu. Python 3.12 and Node 24 explicit; read-only permissions, no application secrets or deployment, concurrency cancellation and job timeouts. .github/CI.md explains results and troubleshooting. Official GitHub examples and repository command paths reviewed; prior clean Windows 58-test/build/lint evidence retained. No application changes or unnecessary test reruns.

Next: review/commit/push accumulated work and inspect the first Project checks run. Linux compatibility and remote workflow execution remain unverified until that run. Hosting/data policy is still undecided. Changes remain uncommitted; no push performed in this checkpoint.

## Clean Windows environment verified - 2026-09-16

Confirmed working in a newly created temporary Python 3.12 venv: pip install -r backend/requirements.txt, pip check, all 58 backend tests, fresh temporary-storage migrations, alembic check and FastAPI lifespan startup. Separate frontend source copy: npm ci, build and lint passed. Pip/npm caches were available; this was a fresh environment on the current Windows machine, not a new machine or Linux host. Normal servers and saved data were not changed.

The first frontend verification copy omitted .gitignore, causing lint to inspect dependencies; copying the repository ignore file resolved the harness issue without application changes. No dependency changes needed. Next: hosting/data-policy decision, then host-specific install/persistence verification. Hosting, HTTPS, volume durability and backup restore remain unverified. Changes remain uncommitted.

## Configurable storage directory - 2026-09-16

Confirmed working: 58 backend tests and full Chrome workflow pass. CAREER_DATA_DIR selects an existing absolute directory for career_assistant.db and uploads/. Environment overrides backend/.env; omitted value anchors to backend/ independent of working directory. Invalid/relative/missing directories fail configuration. SQLAlchemy URL construction safely handles spaces/percent signs. Alembic CLI and helper share the app engine; injected test connections remain supported.

Verified in temporary storage across subprocess restarts and alternate working directory: migration helper, alembic current/check, app schema guard, upload directory and retained synthetic file. Existing local data not moved. No schema/dependency changes. Real host persistence, backup restore and hosting choice remain unverified; this is storage configuration, not deployment. Next: choose demo versus persistent hosting and test a clean installation for the selected host. Changes remain uncommitted.

## Deployment readiness review - 2026-09-16

Added DEPLOYMENT.md with repository-verified runtime/storage requirements, configuration, migration/startup sequence, synthetic smoke checks and persistence/recovery checks. Confirmed both local servers return HTTP 200; Uvicorn CLI options and referenced migration guide verified. Documentation-only checkpoint; prior 55-test/build/lint/Chrome evidence retained without rerunning unchanged application tests.

Hosting remains planned, not deployed. Current SQLite and upload paths are relative to backend working directory; a separate persistent mount needs shared configurable paths and migration alignment. Clean host installation, HTTPS, persistence and restore are unverified. Pending user preference: disposable synthetic demo versus persistent app (potential storage cost). Next: implement and test storage-path configuration if persistent mode is chosen, then select hosting requirements. No new dependency, database mutation or external deployment. Changes remain uncommitted.

## Configurable API and CORS addresses - 2026-09-16

Confirmed working: 55 backend tests, frontend build/lint and real Chrome workflow pass. VITE_API_BASE_URL controls the frontend API base (local fallback, trims trailing slashes). CORS_ORIGINS controls exact allowed frontend origins, process environment over backend/.env over localhost defaults. Invalid values fail startup. Tests cover file/default/override behavior, allowed and rejected preflights. No dependencies or database changes. Existing local servers remain running; backend must restart to pick up future CORS changes. Full hosting/deployment and clean-machine setup remain unverified. Next: deployment readiness checklist and hosting requirements; changes remain uncommitted.

## 2026-09-16 - Improve keyboard access and overview copy

- Added keyboard skip link to account forms/dashboard and visible focus outlines.
- Replaced stale planned-feature copy with current capabilities and role-score limitations.
- Verified keyboard navigation in real Chrome, existing full browser workflow, build and lint.

## 2026-09-16 - Add database migration baseline

- Added Alembic baseline, guarded adoption command and application startup version check.
- Preserved existing local rows against SQLite backup; added fresh/repeat/adoption/mismatch/startup tests.
- Verified 52 backend tests, Chrome workflow, model/schema parity and dependency health. Updated setup instructions.

## 2026-09-16 - Bound resume uploads

- Added 5 MiB and 10-page limits, password-protected/invalid PDF rejection and cleanup.
- Changed corrupt-PDF response from 500 to 400; limit violations return 413.
- Added browser validation/messages and boundary/failure tests. Forty-eight backend tests, build/lint and Chrome workflow pass.


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
