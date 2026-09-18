# PROGRESS.md — AI Career Assistant

## Feature checkpoint review - 2026-09-18

Reviewed accumulated comparison/requirement/review/export features, demo mode, recovery verification and documentation for Git checkpoint. Latest local evidence: 74 backend tests, 3 frontend tests, lint, normal/demo builds and both Chrome workflows pass. Private data/configuration and generated output are ignored. Preparing commit/push; updated remote CI remains pending. No deployment is part of this checkpoint.

## Download comparison summary - 2026-09-18

Confirmed working: browser-generated JSON summary with timestamp, resume ID, keyword results, automatic categories, separate user choices, source evidence and limitations. Explicit field selection excludes tokens/resume text. Source excerpts may contain private input; UI explains downloads remain locally after logout. No server write or import feature.

Verified 3 frontend unit tests, lint, both builds, both full Chrome workflows with actual downloaded-file parsing and forced download failure/retry. Backend unchanged; prior 74-test evidence retained. Added npm test to CI, remote run pending. Next suggested checkpoint: review and commit accumulated feature work, then verify remote CI. Changes remain uncommitted; earlier edits preserved.

## Temporary user requirement labels - 2026-09-18

Confirmed working: users can choose a category for each detected job skill while retaining automatic labels/source evidence; reset restores automatic use. Choices are clearly attributed, never submitted or persisted, and do not alter keyword score. Editing/recomparing/closing clears state.

Verified lint, normal/demo builds and both complete Chrome workflows, including keyboard selection, reset, unchanged score, lifecycle and mobile layout. Backend unchanged; previous 74-test result retained. Next suggested product checkpoint: export a comparison summary containing automatic labels, user choices and limitations. No new dependencies or schema changes. All changes uncommitted; earlier edits preserved.

## Requirement labels integrated end to end - 2026-09-18

Confirmed working: comparison API now returns typed requirements/evidence, shown in dashboard with expandable original wording and uncertainty explanation. Existing scores unchanged. Cross-line aliases fall back to uncertain evidence without changing scoring skills.

Verified all 74 backend tests, frontend lint, normal/demo builds, both Chrome workflows and eight malformed client-response probes. Browser checks all labels/conflicts, keyboard disclosure, mobile/reset and safe literal markup. No database/dependency changes. No current blocker; remote CI/host verification remains pending. Next suggested product checkpoint: let users explicitly review uncertain labels before considering any requirement-based score. All accumulated changes uncommitted; prior edits preserved.

## Requirement classifier service verified - 2026-09-18

Confirmed working: conservative standalone service labels catalog skill mentions required, optional, not_required or uncertain and retains original fragment evidence. Explicit supported phrases only; conflicts/unclassified mentions force uncertainty. No API/dashboard integration or score changes in this checkpoint.

Verified 22/22 synthetic policy cases (12 development, 10 review), five focused tests and all 72 backend tests. Existing 16-case keyword baseline remains unchanged. Across fixtures 16 skill records classified, 16 uncertain; results are same-author policy checks, not independently labelled accuracy evidence. No dependencies/schema/data changes. Next: expose labels/evidence in comparison API and dashboard, preserving scores and testing ownership/client/browser behavior. Changes remain uncommitted; prior edits preserved.

## Comparison context evaluation completed - 2026-09-18

Confirmed working: 16/16 synthetic keyword-contract cases; 67 backend tests; frontend lint/demo build; complete demo Chrome workflow. Required-only interpretation probe matches 5/12 sets (12 true positives, 7 false positives, 1 false negative; precision 63.2%, recall 92.3%). This measures misuse of mention output as requirements, not a implemented classifier or real-world accuracy.

Added fixtures/evaluator and a regression test; results explain equal weighting beside the score. No matching-score change: broad negation rules would break not optional/not only examples. No schema/dependency/data changes. Next: define required/optional/negated/uncertain classification and broader independent examples before any semantic scoring change. Product comparison remains usable with explicit limits. Changes uncommitted; prior work preserved.

## Job-description comparison - 2026-09-17

Confirmed working: 66 backend tests, frontend lint, normal/demo builds and normal/demo Chrome workflows. Added owner-protected POST /resumes/{resume_id}/compare-job, 1-10,000-character validation and deterministic service using existing skill extraction. Returns job/shared/not-detected terms and nullable percentage; no persistence or external AI call.

UI supports pasted text, pending/errors/retry, clear-on-edit/close and cancellation on unmount. Verified API ownership/validation/boundaries, aliases, null versus zero, browser empty/failure/retry/mobile/reset paths. Isolated client check accepts Python rounding ties and rejects malformed/inconsistent responses. No schema/dependency changes. Next: improve comparison quality with explicit synthetic required/optional/negated examples before semantic features. Hosted verification remains pending. All changes uncommitted; earlier work preserved.

## Skill review checklist - 2026-09-17

Confirmed working: per-role Review next steps disclosure, temporary reviewed checkboxes/count, full-overlap guidance and reset after closing role results. Lint, normal/demo builds and both Chrome workflows pass, including keyboard Space, unchanged score, network retry and mobile overflow. No backend/schema/dependency changes; prior 60-backend-test evidence retained.

User redirected work toward product features. Reuses not_detected_skills; no LLM, paid API or personal-data transfer. Checklist progress is not saved and does not indicate mastery. Next suggested feature checkpoint: define comparison against a user-pasted job description with explicit input/output/evaluation before implementation. Deployment stays prepared but unpublished. Changes uncommitted, existing edits preserved.

## Disposable demo prepared - 2026-09-17

Confirmed working locally: demo/normal frontend builds, lint, both real Chrome workflows and four migration tests. Demo build shows synthetic-data/reset guidance before and after login; normal build omits it. Mobile overflow, failures/retries, uploads/results and logout pass. Existing full 60-backend-test evidence retained; no backend application changes.

Added dev:demo/build:demo commands and isolated browser mode on port 5174. User selected disposable synthetic data. HOSTING_PLAN.md records exact build/storage settings. No local data deletion, reset scheduler, public deployment or paid service. Next: review Git checkpoint and select/provision the proposed free hosting services with actual URLs and a fresh hosted key, then run hosted smoke/reset checks. Changes remain uncommitted; prior edits preserved.

## Hosting proposal prepared - 2026-09-17

Added HOSTING_PLAN.md with a candidate Render backend/static-site layout, repository-specific commands, configuration and separate demo/persistent acceptance checks. Provider documentation reviewed; no service selected, purchased or deployed. Data-policy question is pending. Next: receive that choice, then implement the selected mode and verify locally before deployment. Corrected README/DEPLOYMENT local test count to 60; remote evidence remains 58. Documentation checks pass; application tests were not rerun because code is unchanged.

## Local backup recovery verified - 2026-09-17

- Confirmed working: two new synthetic recovery tests; all 60 backend tests pass locally on Windows. Complete offline same-path snapshot restores account login, API results, ownership protection and identical PDF bytes.
- Expected failure verified: database-only restore retains text/API responses but original PDF is missing. No normal database, uploads or running servers changed.
- Added backend/tests/BACKUP_RECOVERY.md with repeatable command, offline procedure and path limits. No application/schema/dependency changes.
- Next: choose disposable demo versus persistent hosting, then validate the chosen host. Hosted restore, relocation, retention and public deployment remain unverified. No local blocker. Changes remain uncommitted; earlier documentation edits preserved.

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

## Keyboard navigation and accurate overview - 2026-09-16

- Confirmed working: frontend build/lint and expanded real Chrome workflow pass. First Tab reveals skip link, Enter focuses workspace, next Tab reaches registration name field. Existing upload failure/recovery, results, mobile overflow and logout checks pass.
- Added skip link and visible keyboard focus styling in App.jsx/App.css. Replaced stale coming-soon overview with implemented PDF/text/keyword/example-role behavior.
- Build initially hit known sandbox spawn EPERM; approved rerun passed. Browser startup timed out on sandbox Vite launch; approved full rerun passed.
- Previous 52 backend test result retained; no backend application changes this checkpoint. Full screen-reader/contrast/visual audit remains unverified. No local-development blocker.
- Next: configurable frontend API address and backend allowed origins for deployment preparation. All accumulated changes remain uncommitted.

## Database migrations verified - 2026-09-16

- Confirmed working: 52 backend tests and real Chrome workflow pass. Alembic current reports 0001_initial (head), check detects no pending model changes, and pip check passes.
- Added frozen initial migration, guarded adoption of existing unversioned tables, and startup version check. Fresh databases are created by the migration command; repeat execution is safe. Tested mismatched schema rejection without stamping.
- Backed up local SQLite using its backup API into ignored backend/backups/. Compared all rows before/after: 2 users and 4 resumes unchanged. Upload files untouched.
- Next planned checkpoint: frontend accessibility and portfolio presentation review. Deployment configuration and clean-machine setup remain unverified; no blocker for local development.
- Current migration and earlier upload-limit changes remain uncommitted. Restart backend after updating dependencies and running scripts/migrate_database.py from backend.

## Upload limits verified - 2026-09-16

- Started clean at pushed checkpoint e1ae85a. Confirmed working: 48 backend tests, frontend build/lint and expanded real Chrome workflow pass.
- Added 5 MiB actual spooled-file limit and 10-page parser limit; exact boundaries accepted. Empty/corrupt/password-protected PDFs -> 400; too large/too many pages -> 413. Rejected files leave no DB record or stored PDF. Existing server/storage failures still 500.
- Browser checks size early, shows limits and handles invalid/limit errors; Chrome verifies oversized/corrupt/11-page failures then successful upload and results.
- These limits apply after multipart receipt/spooling; deployment request limits and parser time/memory isolation remain future work. Existing resumes untouched; no schema/dependency change.
- Next: establish database migration baseline while preserving current data. Changes uncommitted.


## Private JWT configuration - 2026-09-15

- Confirmed working: 44 backend tests and Chrome smoke pass; dotenv file loading, environment precedence, missing/short-key rejection, startup failure, token signature/expiry and setup idempotence verified. pip check passes.
- Added app/config.py, scripts/init_local_env.py and safe .env.example. Installed/pinned python-dotenv 1.2.3. Generated ignored backend/.env without printing its value; existing files are never overwritten. Removed hardcoded current signing key, kept HS256/30 minutes. No account/password/resume changes.
- Tests now use independent generated keys. Old key remains in Git history but is retired for new app startups; existing sessions require login after backend restart.
- Scope estimate: local portfolio MVP roughly 65–75% complete; broader deployed/hardened scope roughly 45–55%. At 1–2 focused hours/day, estimated 14–28 more days for local portfolio polish or 28–56 for deployed scope; uncertain and scope-dependent.
- Next: upload size/page limits and clear failure responses, then migration plan and deployment setup. Work remains uncommitted; normal backend should be restarted to load the new key.


## Project README checkpoint - 2026-09-15

- Added root README with verified feature scope, architecture, Windows setup, API/Postman instructions, tests, demo steps, troubleshooting and current limitations. Replaced Vite-template frontend README with project guidance.
- Confirmed working: relative documentation links exist, installed backend versions match requirement pins, pip check reports no broken requirements. Setup commands checked against actual app/scripts and prior test runs. Fresh-machine dependency installation remains unverified.
- No application or dependency changes this checkpoint; prior 40-test/build/lint/browser results retained rather than rerun for prose edits.
- Next: review/commit accumulated checkpoint, then move hardcoded JWT configuration to environment variables with compatibility and startup tests. Existing account data untouched; work uncommitted.


## Authentication warning resolved - 2026-09-15

- Confirmed working: 40 backend tests pass without Passlib/bcrypt warning; legacy synthetic Passlib hashes verify (ASCII/Unicode/long/multibyte boundary), new random salts/cost 12, invalid input/hash handling and HTTP 422 registration limits. Existing saved hashes untouched.
- Confirmed working: frontend build/lint and Chrome smoke test including too-long-password feedback/recovery and full workflow. User also reported prior browser smoke PASS.
- security.py now uses existing bcrypt 4.3.0 directly. Removed Passlib from requirements, preserving other pins; normalized requirements from UTF-16 to UTF-8. Existing environment may still contain unused Passlib; application no longer imports it.
- New registrations accept nonempty passwords up to 72 UTF-8 bytes without nulls. Login retains historical first-72-byte behavior for existing long passwords and historical 4096-character ceiling. No hash migration or database edits.
- Next: review/commit pending role/browser/auth checkpoint, then portfolio setup documentation. Changes remain uncommitted.


## Real browser workflow verified - 2026-09-15

- Confirmed working: automated headless Chrome registration/login, actual app CORS communication, synthetic PDF upload, list refresh, text, skills, role results/counts, blocked-network error/retry, logout, and no horizontal overflow at 390px. Smoke command exited 0.
- Added repeatable browser_smoke.mjs and isolated browser_server.py plus BROWSER_TEST.md. Uses temporary browser profile/uploads, in-memory DB and browser-only API redirect to port 8001. Existing backend on 8000 and personal data preserved; test processes/storage cleaned up.
- Supersedes prior pending browser checks for the tested paths. Full visual/accessibility review, expiry UI and rapid selection races remain outside this smoke test. Existing bcrypt warning remains unresolved.
- Next: review and commit role-matching/browser-test checkpoint, then address authentication dependency warning as a separate maintenance step. Application code/dependencies unchanged this session; work uncommitted.


## Full API workflow verified - 2026-09-14

- Confirmed working: 35 backend tests pass. New isolated flow tests cover registration/login/profile, empty list, real multipart synthetic PDF upload, persisted file/text, skill results, role ranking, second-account isolation, missing auth, wrong password and corrupt-upload cleanup.
- Tests exercise real routers, hashing/JWT, parsing and SQLite via ASGI, with temporary files and an in-memory database. Existing personal account/database/uploads were untouched. Main app startup, browser/CORS and React interactions are outside this test scope.
- Existing Passlib/bcrypt metadata warning recurred; auth tests pass, warning remains open. No dependency or application-code changes this checkpoint.
- Next: browser upload -> text -> skills -> role overlaps check, then commit the verified role-matching checkpoint. Browser confirmation remains pending; work uncommitted.


## Role overlaps dashboard - 2026-09-14

- Confirmed working: frontend build/lint and client checks for authenticated GET, populated and three empty-result cases, 401/404/500, malformed schema/JSON, network failure and cancellation.
- Implemented but unverified in browser: View/Hide role overlaps, ranked results with percentages/counts, matched/not-detected skills, loading/retry/session handling. Text and skills panels remain available independently.
- Backend unchanged this checkpoint; prior 33-test result retained. Manual Postman matches confirmation and browser text/skills/role checks are pending.
- Next: verify role display against API results, then review end-to-end behavior before adding features. Prior role backend edits preserved. No new dependencies/schema changes; work uncommitted.


## Role matching backend - 2026-09-11

- Confirmed starting state: main synchronized with origin/main at 0836d5e; working tree was clean.
- Confirmed working: 33 backend tests pass. Added six role-service and three HTTP tests covering full/partial/zero overlap, duplicate handling, ranking/ties, catalog integrity, ownership/auth, empty text, no role matches and unchanged stored text.
- Added four illustrative profiles and GET /resumes/{resume_id}/matches. Returns extracted skills, overlap percentages, matched and not-detected profile terms, method and catalog labels. No live jobs, AI provider, dependency or database changes.
- Implemented but unverified: user Postman/browser use of the new matches endpoint. Frontend matching UI is not started. Earlier text/skills browser confirmation remains pending.
- Next: test matches in Postman, then display illustrative role overlaps on dashboard with clear limitations. This checkpoint is uncommitted; prior work was pushed as 0836d5e.


## Git checkpoint preparation - 2026-09-11

User requested commit and push of all work so far. Re-ran 24 backend tests, frontend build and lint successfully. Verified runtime/private files are ignored and no token-pattern matches were found. Checkpoint includes frontend authentication/dashboard/upload/text/skills, backend parsing/retrieval/skills, regression tests, evaluation and learning notes. Browser text/skills checks remain pending. Next development checkpoint: define illustrative roles and transparent overlap scoring. Commit/push outcome is recorded in Git history and the session response.


## Matcher evaluation - 2026-09-11

- Confirmed working: 24 backend tests pass. Added 15 synthetic labeled examples and repeatable evaluation runner. Thirteen supported cases now match exactly (previously 12); two limitation probes remain mismatches.
- Fixed Java Script also producing Java by preferring longer overlapping aliases; separate Java mentions preserved.
- Evaluation reports precision/recall and extra/missing skills by group. See backend/evaluation/README.md for before/after and limitations. These development examples are not held-out accuracy evidence.
- Next: define a small illustrative role catalog and transparent skill-overlap scoring, preserving keyword/proficiency limitations. Skills/text browser checks remain unverified. No schema/dependency changes; work uncommitted.


## Skills dashboard checkpoint - 2026-09-11

- Confirmed working by user report: skill endpoint passed in Postman after replacing the resume-ID placeholder with a numeric ID.
- Confirmed working: frontend build/lint and isolated client checks for request/auth, populated/no-match/no-text responses, 401/404/500, malformed schema/JSON, offline and abort propagation.
- Implemented but unverified in browser: View skills/Hide skills, list rendering, loading/retry/errors, no-readable-text versus no-catalog-match messages, cancellation and session reset.
- Added ResumeSkills and getResumeSkills; ResumeList tracks one open skills panel independently of text. Backend unchanged; previous 22-test result retained, not rerun for this frontend-only change.
- Next: compare browser skills with Postman results, then evaluate matcher precision/coverage on representative synthetic examples before matching roles. Earlier text-view browser test remains pending. No dependency change or commit.


## Skill extraction backend - 2026-09-11

- Confirmed working: 22 backend tests pass, including six matcher cases and three skills HTTP cases plus all prior tests. Covers explicit mentions, aliases, whitespace, duplicates, punctuation, longer-word exclusions, missing text, no matches, owner access, 401 and 404. Stored text remains unchanged.
- Added local 32-skill software catalog, extract_skills service, structured ResumeSkillsResponse and GET /resumes/{resume_id}/skills. Shared owner lookup with detail endpoint. No database/dependency changes or external API use.
- Scope: deterministic term matching, not proficiency assessment; negation/context and skills outside catalog are unsupported. Synthetic test checks are not real-world quality evaluation.
- Next: display skill results in React with empty-text/no-match/error states. Text-view browser verification remains pending. Work uncommitted.


## Extracted text checkpoint - 2026-09-11

- Confirmed working by user report: uploaded-resume list visible in browser.
- Confirmed working: 13 backend tests, frontend build/lint and detail-client checks. Detail HTTP tests cover owner text, other-owner/missing 404, missing/invalid token 401, null/empty text and response fields. Existing list/upload regressions pass.
- Implemented but unverified in browser: View text/Hide text, loading/retry/errors, empty-text explanation, switching resumes and cancellation.
- Next: manual extracted-text check; then plan a deterministic skill-extraction checkpoint with explicit input/output/evaluation. No schema/dependency changes; tests used synthetic data. Work uncommitted.


## Resume list checkpoint - 2026-09-11

- Confirmed working: nine backend tests pass. New ASGI HTTP tests verify GET /resumes returns only the token owner's rows, newest first, empty 200 list, missing/invalid auth 401, and metadata-only response. Existing six upload regression tests pass.
- Confirmed working: frontend build/lint and client checks for GET/bearer header, populated/empty list, 401/500, malformed responses and offline server.
- Implemented but unverified in browser: ResumeList filenames, loading/empty/error/retry behavior, reload after upload, cancellation and 401 session reset.
- Next: manually verify saved resume list and upload refresh, then add owner-protected extracted-text viewing. No schema/dependency changes. Tests used isolated data. No commit; earlier work preserved.


## Upload cleanup verified - 2026-09-11

- Confirmed working: six isolated unittest cases pass: valid PDF text/file/owner, corrupt PDF, injected parser failure, commit failure, partial disk write, non-PDF rejection. Tests call the route directly, using synthetic PDFs, temporary files and in-memory SQLite; HTTP transport/auth were not retested.
- Reproduced premature commit (AssertionError: 1 != 0), leftover partial file, and corrupt-PDF Windows file lock before fixing them.
- Upload now parses, flushes and builds the response before one commit. Parser reads bytes and closes its document with a context manager. Write failures remove partial files.
- Next: resume retrieval API and dashboard list with user ownership checks. No schema/dependency change; existing user data untouched. Browser upload after this fix remains unverified. Work remains uncommitted.


## Browser upload confirmed - 2026-09-11

- Confirmed working (user report): successfully uploaded a resume through the running frontend. This supersedes the happy-path browser verification gap below.
- Both servers returned HTTP 200 during startup verification.
- Browser failure paths and independent inspection of stored text remain unverified.
- Next checkpoint: reproduce and fix backend parsing-failure transaction cleanup, then resume retrieval/display. Existing changes remain uncommitted.


## Latest checkpoint - PDF upload UI, 2026-09-11

- Confirmed working: production build (approved execution outside sandbox), lint, isolated JavaScript client checks for multipart field resume_file, bearer header, no manually set Content-Type, 201 response, 400/401/422/500 errors, offline server and malformed response.
- Implemented but unverified: ResumeUpload component on the authenticated dashboard; PDF selection, pending state, success feedback, session-expired handling and unmount cancellation. Real browser upload and backend persistence were not retested this session.
- Removed backend debug printing of extracted resume text. No schema or dependency changes.
- Current/next: run the browser happy/failure checks in LEARNING_LOG.md before adding resume retrieval. Browser automation tools unavailable. Existing backend commits the resume row before parsing; parse failure cleanup can leave a row pointing to a removed file. Separate targeted backend checkpoint needed.
- Work remains uncommitted; existing backend/frontend/documentation edits preserved.


## Latest checkpoint - Authenticated dashboard, 2026-09-10

- Confirmed working: build/lint; client checks for GET /users/me bearer header, profile success, 401/500 status preservation, connection failure, malformed responses and abort propagation; login/register POST regression checks.
- Confirmed working: isolated backend ASGI checks with two users return the profile matching each token; missing/invalid/expired/unknown-user tokens return 401; both allowed origins pass GET/Authorization preflight, untrusted origin returns 400. In-memory database only; no tokens printed.
- Implemented but unverified: browser dashboard loading, profile display, retry, logout during loading and return to login with session message on 401. Browser automation unavailable in this session.
- Added Dashboard.jsx and getCurrentUser; generalized existing JSON helper. App replaces temporary success view with dashboard, keeps token in memory and clears it on protected-request 401. CORS permits GET and Authorization alongside existing POST/Content-Type.
- Current: manual dashboard checkpoint. Next: PDF resume upload form connected to existing protected upload endpoint. No known blocker; no database/schema/dependency changes. Prior edits preserved; no commit.

## Latest checkpoint - Login integration, 2026-09-10

- Confirmed working: production build and lint; client checks for login JSON payload/success, 401/422/500, network failure, malformed JSON/token response; registration success/error regression checks.
- Confirmed working: isolated in-memory backend ASGI checks for registration 201, login 200 + bearer token, allowed CORS response, wrong password/unknown email 401 and invalid email 422. Existing database untouched; tokens not printed.
- Implemented but unverified: LoginForm browser behavior, pending state, App success view, logout and refresh resetting session. Manual checks below in LEARNING_LOG.md.
- Added LoginForm; shared JSON POST helper in existing api.js; App holds token in React state, hides account forms after login, clears token on logout. Registration feedback now points to login below.
- Current: manual login UI checkpoint. Next: authenticated /users/me request and dashboard, including expired-token handling. No implementation blocker. Existing bcrypt warning persists; no backend changes this step.
- Work uncommitted; earlier registration/resume changes preserved.

## Latest checkpoint - Registration API integration, 2026-09-10

- ? Confirmed working: production build and lint; API client checks for JSON payload, success, 409, 422, 500 and network failure. Backend ASGI checks with an isolated in-memory SQLite database: registration 201, hashed password verified, no password in response, duplicate 409, invalid email 422, local CORS preflights 200 and untrusted origin 400.
- Added frontend/src/services/api.js; RegisterForm now submits, disables inputs while waiting, clears password on success, and shows feedback. FastAPI permits the two local Vite origins for JSON POST requests.
- ?? Implemented but unverified: actual browser submission/rendering. Refresh the frontend with FastAPI running; new test email should show success; repeat should show duplicate feedback; backend offline should show readable connection feedback.
- Current: manual browser checkpoint. Next: login form and API integration. No implementation blocker. Existing Passlib/bcrypt warning recorded separately; no dependency changes.
- Existing database and resume edits preserved. No commit made. This supersedes earlier frontend-only registration status.

## Latest checkpoint - Registration form, 2026-09-10

- Added: components/RegisterForm.jsx and RegisterForm.css, rendered below the welcome overview in App.jsx.
- Scope: frontend-only form with full_name, email, and password; controlled inputs and browser validation. Check details prevents default submission and shows a local message; no network request or account creation. Password is held only in React state, not logged or persisted by application code.
- Verified: build and lint exit 0; Vite serves form module with HTTP 200.
- Implemented but unverified: browser interaction and responsive layout. Happy path: enter a nonblank name, valid email, and nonempty test password; Check details shows that checks passed and no account was created. Failure paths: empty required fields, invalid email, spaces-only name should block submission. Editing fields clears previous feedback.
- Current task: manual form checks and learning controlled inputs. Next: connect registration to FastAPI with API client, browser cross-origin configuration, and success/error handling.
- No known build blocker. Backend unchanged. No commit made.

---


## Latest checkpoint - Welcome page, 2026-09-10

- Confirmed working (user report): starter page opened and counter increased.
- Completed: replaced demo counter with a static AI Career Assistant welcome page; simplified global/page CSS; updated browser title.
- Verified: npm run build and npm run lint exit 0; existing server returns HTTP 200 and serves updated title and welcome module.
- Implemented but unverified: visual layout of the new welcome page. User should refresh http://127.0.0.1:5173/ and check heading and all three planned-feature descriptions; narrow browser to check wrapping and horizontal overflow.
- Current task: user visual check and learning JSX/components/className. Next: registration form checkpoint.
- No known build blockers. Changes uncommitted. Backend unchanged.
- Earlier starter-browser-pending entries below are superseded by the user confirmation above.

---


## Latest checkpoint - 2026-09-10

- Completed: installed Node.js 24.19.0 and npm 11.17.0; created frontend/ with the official React JavaScript Vite starter; installed dependencies.
- Confirmed working: npm run build and npm run lint exit 0. Vite serves / and /src/App.jsx with HTTP 200 at http://127.0.0.1:5173/. Git ignores frontend/node_modules and frontend/dist.
- Implemented but unverified: browser rendering and interactive counter. Open the URL and click Count is 0; expect Count is 1.
- Failure check to perform: stop the dev server, then reload; expect connection refused. Restart with npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort.
- Current task: finish the visual starter-page checkpoint. No known build blocker.
- Next: explain the starter files, then replace the starter with the first AI Career Assistant page, one checkpoint at a time.
- Repository inspection supersedes older unknowns below: frontend now exists; PyMuPDF parsing and resume_text persistence code were inspected on September 9, but backend runtime tests were not repeated. Existing backend edits remain uncommitted.
- Prior backend success claims below come from the imported handoff.

---


## Status Legend

- ✅ Confirmed working
- 🟡 Implemented but unverified
- 🔵 Planned
- ⛔ Blocked
- ❌ Broken
- ⚪ Unknown — repository verification required

---

# Current Overall State

## Backend

### ✅ FastAPI application
Local development backend has been confirmed running at:
`http://127.0.0.1:8000`

### ✅ Root endpoint
`GET /` confirmed `200 OK`.

### ✅ User registration
Registration exists and test users have been created successfully.

### ✅ Login
`POST /auth/login` confirmed working and returns JWT bearer token.

### ✅ Protected current-user route
`GET /users/me` confirmed:
- valid bearer token -> 200
- no token -> 401

### ✅ Resume upload
`POST /resumes/upload` confirmed working for authenticated PDF upload.

### ✅ PDF-only validation
DOCX upload confirmed rejected with:
`400 Bad Request`
`Only PDF resumes are allowed`

### ✅ Resume text extraction
Confirmed from terminal/database inspection.

### ✅ Resume text persistence
`resume_text` confirmed populated in SQLite.

### ⚪ Exact current implementation details
Codex must inspect:
- `models.py`
- `resumes.py`
- `resume_parser.py`
- requirements

because some code was previously suggested and later behavior was confirmed, but the exact current source must be verified.

---

# Git

### ✅ Git repository initialized
At project root.

### ✅ Main branch
Branch renamed to `main`.

### ✅ GitHub push
Earlier backend checkpoint successfully pushed.

### ⚪ Latest backend parsing changes
Latest screenshot showed modified/untracked files.

First Codex action:
```bash
git status
```

Verify latest resume parser/model changes are preserved and not accidentally lost.

---

# Frontend

### 🔵 React + Vite frontend
Latest decision is to begin frontend development.

Recommended stack:
- React
- Vite
- JavaScript

### ⚪ Frontend project existence
Not confirmed before handoff.

Codex must inspect whether:
`frontend/`
already exists.

---

# AI / ML

### 🔵 Resume cleaning / normalization
Not started.

### 🔵 Skill extraction
Postponed until after frontend foundation.

### 🔵 Career/job matching
Not started.

### 🔵 AI recommendations
Not started.

### 🔵 AI provider/model selection
Not decided.

---

# Current Task

**Frontend-first development.**

First checkpoint:

1. Inspect repository.
2. Protect existing backend changes.
3. Verify whether frontend exists.
4. If not, create React + Vite frontend.
5. Start frontend.
6. Confirm default React page loads.
7. Teach the user what Vite, React, npm, `package.json`, `src`, and the dev server are.

---

# Next Major Checkpoints

1. Frontend project running.
2. Clean default Vite UI.
3. Create project page/component structure.
4. Build Register page.
5. Build Login page.
6. Configure backend CORS.
7. Connect registration.
8. Connect login.
9. Handle JWT.
10. Create dashboard.
11. Connect `/users/me`.
12. Add resume upload UI.
13. Upload PDF end-to-end from browser.
14. Add resume retrieval API if needed.
15. Resume skill extraction.
16. Career matching.
17. AI recommendations.
