# PROJECT_HANDOFF.md --- AI Career Assistant

## Feature checkpoint pushed and CI passed - 2026-09-18

Confirmed working: feature commit e93392001eca1722eb5fbb12f2c763b32c65ccf5 is pushed to origin/main. [Project checks run 35356842127](https://github.com/Vamshinethula/ai-career-assistant/actions/runs/35356842127) passed all three jobs: backend Windows and Ubuntu (74 tests, dependency checks, fresh migration/model agreement), frontend Ubuntu (3 export tests, lint and production build). Local normal/demo Chrome and build evidence remains recorded separately; browser tests are not in CI.

No private data or generated files were committed. No deployment occurred. This documentation-only follow-up records the verified feature commit; application code is unchanged. Next: choose the next product feature or proceed with the already-selected disposable demo hosting setup. No current test blocker.

## Feature checkpoint review - 2026-09-18

Reviewed accumulated comparison/requirement/review/export features, demo mode, recovery verification and documentation for Git checkpoint. Latest local evidence: 74 backend tests, 3 frontend tests, lint, normal/demo builds and both Chrome workflows pass. Private data/configuration and generated output are ignored. Preparing commit/push; updated remote CI remains pending. No deployment is part of this checkpoint.

## Comparison export complete - 2026-09-18

Added services/comparisonExport.js pure JSON serializer and Download comparison summary action in JobComparison.jsx. Explicit fields preserve provenance/null scores, exclude unrelated private fields; evidence may include original input. Blob URL is revoked after download initiation; failures show feedback. Result invalidation removes button. No import/server persistence.

Verified 3 Node built-in unit tests (npm test), lint, normal/demo builds, both Chrome flows reading actual synthetic JSON downloads and testing failure/retry. Added frontend CI test step, not verified remotely. Backend unchanged, prior 74-test count. Test runner initially hit sandbox spawn EPERM; approved rerun passed. Next: review/commit accumulated checkpoints and remote CI verification. All pending edits preserved, no commit/deployment.

## User requirement review UI complete - 2026-09-18

JobComparison.jsx now tracks labelChoices in local state, renders native select with Use automatic label plus four categories, separately displays Your choice, and offers per-skill reset. Automatic category/evidence never overwritten. State clears on edit/submission and unmount. No API transmission, persistence or score change.

Verified lint, both builds and normal/demo Chrome flows. Tests use real keyboard for first choice, then verify reset/recompare/edit/close and mobile. Browser helper initially redeclared a top-level const; wrapping evaluation helper in an IIFE fixed the test failure. Backend unchanged (prior 74 tests). Next suggested product feature: downloadable comparison summary including source/provenance and user choices, with privacy and temporary-state behavior explicit. No commit/deployment; preserve prior pending work.

## Requirement API/UI integration complete - 2026-09-18

JobComparisonResponse now requires requirements list with typed category/evidence. compare_job_description calls the classifier but preserves old score/catalog. Whole-text versus fragment alias mismatch gets uncertain + original input evidence, and extra fragment skills are filtered out. Source excerpts may contain the full job input; no persistence.

JobComparison.jsx displays tentative labels and details/summary excerpts as React text, including conflicts. api.js validates coverage, categories, evidence provenance and aggregation. Update frontend/backend together; old backend missing field produces readable error. No DB migration. Verified 74 backend tests, lint, both builds, both Chrome flows, eight isolated client rejection cases. Source markup never executes, keyboard and mobile pass. Next suggested product work: explicit review of uncertain classifications, evaluated separately before changing any scores. No real data changes, commit or deployment; preserve pending work.

## Explicit requirements service checkpoint - 2026-09-18

Added app/services/job_requirements.py with classify_job_requirements(text), no callers in production API yet. Four categories: required, optional, not_required (absence of obligation, not prohibited skill), uncertain. Full-fragment templates plus catalog-only lists; no cross-line heading inference. Conflicts or an unclassified occurrence produce uncertain. Evidence retains source fragments; duplicates deduplicated.

Added evaluation/requirement_cases.json, evaluate_requirements.py, REQUIREMENTS.md and five tests. Verified 22 policy cases and 72 backend tests; existing job-score evaluator unchanged. Half of 32 emitted fixture skill records abstain. Same-author review group is not independent accuracy validation. Next: additive comparison response schema + UI evidence display with auth/client/browser tests; keep keyword score unchanged. No production endpoint/UI changes, dependencies or database mutations. Changes uncommitted; preserve all earlier work.

## Comparison quality checkpoint complete - 2026-09-18

Added evaluation/job_cases.json (16 examples), evaluate_jobs.py and test_job_evaluation.py. Runner exits nonzero on keyword-contract regressions and reports semantic interpretation gaps separately. All 16 contract cases pass; required-only interpretation is exact on 5/12 with TP=12 FP=7 FN=1. Negated resume experience is separately documented and is not measured by job-side metrics.

Decision: preserve keyword contract rather than add a broad negation heuristic that fails not optional/not only. JobComparison UI now explicitly states every detected term counts equally with required/optional example. Verified all 67 backend tests, lint, demo build and full demo browser flow. No new dependencies or actual user data changes. Next product task: define separate requirement classifications with uncertainty and an independent evaluation set before changing scoring. Existing normal-mode build evidence is from previous checkpoint; current changed copy verified in demo. All pending work uncommitted; preserve earlier edits.

## Job-description comparison complete locally - 2026-09-17

Added services/job_comparison.py, request/response schemas and POST /resumes/{resume_id}/compare-job using get_owned_resume. Job text 1-10,000 chars; no saving or external service. Percentage uses unique detected job skills as denominator, null for absent resume text/no job skills. Existing extractor limitations retained.

JobComparison.jsx is toggled per resume, uses shared client, clears results on edit and text/results on close, aborts on unmount, handles 401 via session reset. Client validates skill partition and rounded score with tolerance for Python/JS ties. See backend/evaluation/JOB_COMPARISON.md and README for examples/limits.

Verified 66 backend tests, lint, both builds, both Chrome workflows and isolated client validation probes. No actual user data changed, no schema/dependency change. Restart normal backend to load the new endpoint; test servers were isolated. Next: comparison-quality evaluation for required/optional/negated phrases, then choose smallest evidence-based improvement. Demo remains prepared but unpublished. Pending edits preserved; nothing committed.

## Product feature: skill review checklist - 2026-09-17

User requested next product feature instead of more hosting work. Added SkillReview.jsx under each role in ResumeMatches, reusing not_detected_skills. Native details/summary disclosure, labelled checkboxes, temporary per-role reviewed state/count, all-terms-detected guidance. Honest wording: review is not mastery; missing keyword is not proven skill gap. Unmount on hiding/switching resumes resets state; nothing persisted.

Verified lint, normal/demo builds and full Chrome workflows in both modes. Keyboard Space, check/uncheck, unchanged score, reset, no-gap branch and mobile overflow covered. Synthetic Enter activation did not open native details; Space with explicit focus passed. Backend unchanged (prior 60 tests). Next suggested product checkpoint: specify user-pasted job-description comparison and its evaluation, then implement incrementally. Demo hosting decision remains disposable, no deployment. All changes uncommitted; preserve earlier edits.

## Disposable demo selected and prepared - 2026-09-17

User chose disposable demo. App.jsx displays notice only when Vite MODE is demo; npm dev:demo/build:demo enable it. Notice is within workspace before forms/dashboard. It requests synthetic details/test password/resume and explains possible resets and cold starts. This is guidance, not personal-data detection or automatic deletion. Normal local storage remains unchanged.

Verified lint, demo/normal builds with notice artifact checks, both Chrome workflows, and four migration tests. CAREER_TEST_DEMO=true uses isolated Vite 5174 and test-only CORS. Full backend suite remains last verified at 60. HOSTING_PLAN.md has selected-policy settings; Render still a candidate, no service created. Next: Git checkpoint/provider setup, actual URLs/separate secret, then hosted verification. Use build:demo on host; last local build was normal and dist is ignored. Preserve all existing pending edits.

## Hosting proposal awaiting data policy - 2026-09-17

HOSTING_PLAN.md is a draft, not an approved host choice. User was asked disposable synthetic demo versus persistent app; no answer yet. Render docs reviewed: free backend loses local files on sleep/restart/redeploy, paid disk accessible at runtime only. Existing frontend timeout is 15 seconds, so cold-start behavior needs verification. Next: obtain data-policy choice, prepare that mode, then review provider/cost and actual deployment. No application changes or external provisioning; prior 60-test evidence retained and pending edits preserved.

## Local backup recovery checkpoint - 2026-09-17

Two new tests in backend/tests/test_backup_recovery.py verify SQLite snapshot plus uploads restored offline to the same absolute path using temporary synthetic data. All 60 backend tests pass locally; only the prior 58-test suite has remote CI evidence. Reuses existing API driver, checks saved login/results, schema version, ownership and exact PDF bytes. Database-only negative case proves dashboard success is insufficient. See backend/tests/BACKUP_RECOVERY.md for command/procedure. Real saved data and normal servers untouched; application code unchanged.

Next: choose demo versus persistent data policy and hosting requirements; no provider selected or deployment performed. Different-path/cross-OS restoration and hosted retention/recovery remain unverified. Changes uncommitted; preserve pre-existing documentation edits.

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

## Latest checkpoint - Keyboard skip navigation, 2026-09-16

App.jsx now includes a skip link to focusable workspace and accurate current-feature copy. App.css gives keyboard controls a visible focus outline and reveals the skip link on focus. Chrome smoke dispatches real Tab/Enter events to verify focus progression to registration; existing full workflow passes. Build/lint pass (build and browser required approved sandbox escalation). Backend code unchanged; prior 52-test result retained. Full accessibility audit remains outstanding. Next small checkpoint: environment-configurable frontend API URL and backend CORS origins. Current and earlier changes remain uncommitted.

## Latest checkpoint - Alembic baseline, 2026-09-16

Installed/pinned Alembic 1.20.0 and dependencies. backend/migrations/versions/0001_initial.py freezes existing schema. scripts/migrate_database.py creates fresh schemas or compares unversioned schemas to the frozen baseline before stamping, then upgrades to head. app/main.py now checks the version in lifespan instead of create_all. Browser server migrates its isolated database first. Baseline downgrade deliberately refuses data deletion.

Verified: 52 backend tests, Chrome flow, alembic current/check and pip check. SQLite backup retained in ignored backend/backups/; all 2 user and 4 resume rows compared unchanged. Existing normal server may need restart. README includes migration setup; backend/migrations/README.md includes backup and future revision workflow. Changes and prior upload checkpoint are uncommitted. Next: UI/accessibility and portfolio presentation review, followed by deployment configuration and clean-machine verification.

## Latest checkpoint - Upload limits, 2026-09-16

Added MAX_RESUME_BYTES=5*1024*1024 and MAX_RESUME_PAGES=10 in config. Route measures actual spooled file before saving; parser checks PDF/password/page count before text extraction. Typed parser errors map to 400 invalid PDF or 413 page limit, with rollback/file cleanup. Unexpected errors remain 500. Frontend size check/copy and 400/413 messages added. Forty-eight tests, build/lint and Chrome failure/recovery flow pass. Existing data untouched; after-multipart limits are not network ingestion or full parser resource isolation. Next: migration baseline and verification without deleting DB. Current edits uncommitted; prior e1ae85a pushed.


## Latest checkpoint - Environment JWT key, 2026-09-15

Added explicit backend/.env loading with python-dotenv 1.2.3; environment JWT_SECRET_KEY wins, absent/blank/under-32-byte values fail startup. init_local_env.py creates a random key only if no .env exists; generated local .env is ignored and never printed. jwt_handler.py now loads config, retaining HS256 and 30 minutes. Test key isolated in test_environment.py and browser_server.py. Forty-four tests, browser smoke, setup idempotence and pip check pass. Restart normal backend/login to use new key. No account hashes or database changes; retired key still in history, no history rewrite. Next: upload resource limits and targeted failure tests, then migrations/deployment. User received scope-based completion/time estimates recorded in ROADMAP.md. Work uncommitted.


## Latest checkpoint - Project README, 2026-09-15

Added root README.md and replaced frontend template README. Documents setup directories, current API/features, test commands, architecture and local-dev limits (including hardcoded JWT configuration, no env loader, no upload limits/migrations). Verified relative links, installed pins and pip check. Fresh-machine installation not tested. No app changes; prior 40-test/build/lint/Chrome results retained. Next: checkpoint review/commit, then environment-based JWT config and startup validation. Existing uncommitted role/auth/browser work preserved.


## Latest checkpoint - Direct bcrypt compatibility fix, 2026-09-15

Reproduced Passlib 1.7.4 metadata warning with bcrypt 4.3.0. Replaced CryptContext usage with bcrypt hashpw/checkpw; kept bcrypt pin and cost 12. Legacy password verification explicitly truncates UTF-8 bytes at 72, preserving old hashes; new registration rejects empty/null/over-72-byte input with 422 and frontend feedback. Four synthetic legacy fixtures captured using old code; no real user hashes accessed/changed. Removed Passlib requirement; requirements encoding normalized UTF-16 -> UTF-8. No package installation/uninstallation occurred. Forty backend tests, build/lint and Chrome workflow including password-length validation pass. Prior browser-smoke user PASS recorded. Next: checkpoint review/commit and portfolio setup docs. All prior uncommitted changes preserved.


## Latest checkpoint - Real Chrome verification, 2026-09-15

Automated browser workflow now passes with installed Chrome: registration/login, actual React/CORS, PDF upload/list/text/skills/role percentages, network error/retry, logout and 390px overflow check. Added backend/tests/browser_smoke.mjs, browser_server.py and BROWSER_TEST.md. Run Node script from root. Requires ports 8001/9223 free; reuses frontend 5173 or starts it. Test-only Chrome requests redirect 8000 to isolated real FastAPI app on 8001, in-memory DB/temp uploads. Existing app server/data untouched; temporary processes/storage removed. Initial 8000 collision led to isolated-port design. Prior browser gaps are closed for these paths, not full visual/accessibility/expiry/race review. Existing bcrypt warning remains open. Next: checkpoint review/commit, then targeted auth-dependency maintenance. No dependency/application changes this session; prior uncommitted work preserved.


## Latest checkpoint - Full API workflow tests, 2026-09-14

Added backend/tests/test_resume_flow.py. Tests register/login through actual routes, upload a synthetic PDF through multipart HTTP, verify stored bytes/text/skills/role output and second-account isolation. Failure test covers wrong password, missing auth and corrupt-file cleanup. All 35 backend tests pass. Uses test FastAPI app with real routers, in-memory DB and temporary storage; no production database touched. Browser/CORS/main app startup not covered. Existing bcrypt metadata warning recurred but auth passed. Next: browser flow review and commit role-matching checkpoint. No application/dependency changes this session; previous uncommitted role/UI work preserved.


## Latest checkpoint - Role overlaps UI, 2026-09-14

Added ResumeMatches.jsx, getResumeMatches and View/Hide role overlaps in ResumeList. Shows example role title, overlap percentage and detected count, matched/not-detected terms, and limitations. Handles missing text, no extracted skills, no matching profiles, retry/401/cancellation. One role panel open at a time independently of text/skills. Build/lint and isolated client tests pass; actual browser interaction unverified. Backend unchanged (prior 33 tests passed). Next: compare dashboard/API results and run manual end-to-end checkpoint. Role backend and current UI work uncommitted; 0836d5e remains the last pushed checkpoint.


## Latest checkpoint - Illustrative role matching, 2026-09-11

Prior work committed/pushed as 0836d5e; this session started clean. Added services/role_matcher.py with four five-skill example profiles (Python backend, React frontend, Java backend, Python data analysis). Canonical skill set intersection determines percentage overlap; returns positive overlaps sorted descending then role_id, plus matched/not_detected skills. GET /resumes/{resume_id}/matches reuses extraction and ownership lookup. Response labels skill_overlap and illustrative_v1. All 33 backend tests pass with synthetic data; no live database changes or new dependencies. Next: Postman check, then dashboard integration. This checkpoint uncommitted; earlier browser skills/text checks remain unverified.


## Git checkpoint preparation - 2026-09-11

User authorized commit and push to origin/main. Final checks passed: 24 backend tests, frontend build/lint, ignored private/runtime artifacts and token-pattern scan. This checkpoint supersedes prior uncommitted notes once committed; inspect Git history/status for the final result. Resume next with illustrative role definitions and overlap scoring. Browser text/skills interaction remains unverified.


## Latest checkpoint - Matcher evaluation, 2026-09-11

Added evaluation/skill_cases.json (15 synthetic cases), evaluate_skills.py and README with reproducible metrics. Reproduced Java Script double match and fixed it with longest nonoverlapping alias spans. All 24 backend tests pass; supported exact cases improved 12/13 to 13/13. Two explicit limitation probes remain: ordinary react false positive, Kotlin outside catalog. Not a held-out/general accuracy benchmark. Run from backend: .venv/Scripts/python.exe -m evaluation.evaluate_skills. Next: define illustrative role catalog and explainable overlap scoring; browser skills/text confirmation still pending. No schema/dependency change, personal data use or commit.


## Latest checkpoint - Skills UI, 2026-09-11

User confirmed Postman skill extraction. Added getResumeSkills in existing API service, ResumeSkills component and View skills/Hide skills in ResumeList. Validates ID/method/text_available/skills response; handles 401,404,network errors and cancellation. Shows separate missing-text and no-match messages and term-matching limitations. Text and skills may be compared side by side in the page; one skills panel open at a time. Build/lint and isolated API client checks pass; browser interaction pending. Backend untouched, last 22 tests passed in prior checkpoint. Next: user checks skills against Postman, then representative matcher evaluation. No new dependencies/schema changes/commit.


## Latest checkpoint - Rule-based skill extraction, 2026-09-11

Implemented backend-only skill extraction. services/skill_extractor.py has 32 canonical software skills and aliases, case/whitespace normalization, boundary matching, deduplication and alphabetical output. GET /resumes/{resume_id}/skills returns resume_id, method=rule_based, text_available and skills. Reuses get_owned_resume for ownership and 404; missing/invalid auth 401. All 22 tests pass. No DB changes, external APIs or dependencies. Results are explicit term mentions, not proficiency; negation, ambiguity and uncatalogued terms remain limitations. Next: connect skill results to React. Prior text-view browser test still unverified. No commit.


## Latest checkpoint - Extracted text view, 2026-09-11

User confirmed browser resume list. Added GET /resumes/{resume_id}, ownership-filtered, 404 for missing/foreign rows. ResumeDetailResponse extends metadata with nullable resume_text; no database change. ResumeList opens one ResumeText component at a time; getResume uses existing API helper. Plain-text rendering preserves line breaks; loading/error/retry/empty/401 and unmount cancellation supported. All 13 backend tests, frontend build/lint and isolated client checks pass; browser text-view checks pending. Next: manual verification, then define rule-based skill extraction scope/evaluation. No commit or dependency change.


## Latest checkpoint - Resume list, 2026-09-11

Added protected GET /resumes to existing router with current_user ownership filter and newest-first order. Reuses ResumeResponse; returns metadata only. Added getResumes and ResumeList component with loading/empty/error/retry/401 handling. Upload completion callback increments Dashboard resumeVersion; key remounts the list to fetch current server data and cancels stale requests. Nine backend tests, build/lint and isolated client checks pass. Browser list/refresh verification pending. Next: manual check, then owner-protected extracted-text view. No schema/dependency change or commit; actual user data untouched by tests.


## Latest checkpoint - Upload transaction cleanup, 2026-09-11

Fixed reproduced parsing-failure stale rows and partial-write files. Parser uses bytes/context manager to avoid Windows malformed-PDF file locks. Route parses before add/flush/response validation/one commit; no post-commit refresh that could trigger destructive cleanup after a successful save. Six direct-route regression tests pass; run from backend with .venv/Scripts/python.exe -m unittest discover -s tests -v. Tests use synthetic data and in-memory SQLite; live database untouched. Next: authenticated resume retrieval and dashboard list. No dependencies/schema changes or commit. Filesystem/database operations are not crash-atomic; deletion denial and process interruption remain limitations. Reading PDF bytes adds memory proportional to file size; upload limits remain future work.


## Latest verification - 2026-09-11

User confirmed successful resume upload in the browser after both development servers were started and returned HTTP 200. Happy-path browser upload is now confirmed by user report. Failure-path browser behavior and independent database/text inspection remain unverified. Resume next with the existing backend parsing-failure cleanup issue, then resume retrieval/display.


## Latest update - PDF upload UI, 2026-09-11

Added ResumeUpload.jsx to Dashboard and uploadResume to the existing API service. Uses multipart resume_file and bearer auth; browser owns Content-Type boundary. Pending/success/errors, 401 session reset and cancellation on unmount implemented. Removed resume-text debug print. Build/lint and isolated client success/error checks passed; browser upload/backend persistence still unverified this session. Next: manual dashboard/upload checks (LEARNING_LOG.md), then address existing upload transaction cleanup before resume retrieval. Existing route commits metadata before parsing and may leave a stale row after parser failure. No schema/dependency changes or commit.


## Latest update - Authenticated dashboard, 2026-09-10

Dashboard.jsx now fetches /users/me through the existing API service using the in-memory token as a bearer header. Displays loading, name/email, retry on recoverable failure and logout. useEffect cleanup aborts requests and ignores stale results; stable App callback clears token and displays re-login message on 401. CORS now allows GET/POST and Content-Type/Authorization for the two existing local origins. Build/lint and isolated backend/client checks passed; actual browser interaction unverified. Next: manually check dashboard, then PDF upload UI. No new dependencies/schema changes/commit; resume edits preserved.

## Latest update - Login integration, 2026-09-10

LoginForm now calls existing POST /auth/login through services/api.js. App stores the returned token only in React state, shows a login-success view, and offers local logout. Refresh clears state. Shared postJson helper preserves registration behavior; registration message updated. No backend/schema/dependency changes. Build/lint, client failure/regression checks and isolated backend login tests passed. Browser login/logout/refresh remains unverified. Next: manual checks then /users/me and dashboard with authorization header/CORS changes and expired-token handling. No commit; prior edits preserved.

## Latest update - Registration connected, 2026-09-10

RegisterForm now calls POST http://127.0.0.1:8000/auth/register through frontend/src/services/api.js. Handles pending/success/error, clears password on success. main.py allows JSON POST from http://127.0.0.1:5173 and http://localhost:5173. Build/lint and isolated backend/API-client checks passed (see PROGRESS.md). Actual browser interaction remains unverified. Next: browser check, then login form/API checkpoint. No account auto-login yet; no schema change or new dependencies. No commit. Earlier frontend-only descriptions are historical.

## Latest update - Registration form, 2026-09-10

Frontend now includes components/RegisterForm.jsx and matching CSS, imported into App.jsx. It is intentionally a frontend-only teaching checkpoint: controlled full name/email/password inputs, required fields, email validation, nonblank-name validation, and local submit feedback. Button says Check details; explanatory copy explicitly says details are not sent. No account is created or API called. Build/lint passed and Vite served the module with HTTP 200; manual interaction tests remain pending. Next task is real registration integration with FastAPI. No backend changes or commits this step.

---


## Latest update - Welcome page, 2026-09-10

User confirmed the starter page and counter worked. Replaced demo App.jsx and demo CSS with a simple static welcome page describing planned product capabilities; changed HTML title. Build/lint passed; updated HTML and React module served successfully by existing server on 127.0.0.1:5173. New page visual verification remains pending. Next: explain JSX/component/CSS relationship, then implement a registration form as a separate checkpoint. Backend unchanged. Work remains uncommitted.

---


## Latest update - 2026-09-10

This update supersedes earlier statements that frontend creation is unconfirmed. The official React JavaScript starter now exists in frontend/. Node.js 24.19.0 and npm 11.17.0 were installed. Dependencies installed; build and lint passed. Vite served the HTML and App.jsx module with HTTP 200 on http://127.0.0.1:5173/. Browser rendering and counter interaction still need manual verification. Next checkpoint: verify the starter in the browser, explain its files, then build the first application page. Backend code was unchanged during frontend setup. No commit was made.

---


**Handoff date:** September 9, 2026\
**Purpose:** Transfer development context from the ChatGPT conversation
to Codex in the IDE.\
**Important evidence rule:** This document deliberately distinguishes
between (a) behavior the user actually demonstrated/reported as working
and (b) code/design that was merely recommended. Codex should inspect
the repository before assuming any suggested code is present.

## 0. SOURCE / HISTORY LIMITATION

This handoff is based on the project conversation history available to
ChatGPT in the current session/context, including the current
conversation summary, user screenshots, code the user shared, and
relevant prior project discussion surfaced in context. I cannot
guarantee that every message from every earlier chat is available
verbatim. Where exact repository state was not demonstrated, this
document says so rather than inventing it.

The most reliable current evidence is: - Successful Git push/status
reported by the user. - Successful FastAPI root, login, protected-route,
PDF upload, rejection of DOCX, PDF text extraction, and SQLite
persistence tests shown/reported by the user. - A VS Code screenshot
showing `resume_text` populated in SQLite and terminal output ending in
`POST /resumes/upload HTTP/1.1" 201 Created`. - Code snippets the user
explicitly shared for authentication, users, and resume upload. - Some
later code (service layer and database text persistence) was originally
suggested by ChatGPT, but the screenshot confirms the resulting behavior
exists. Codex must inspect the actual implementation to see exactly how
it was written.

------------------------------------------------------------------------

# 1. PROJECT VISION

## 1.1 What is being built

The project is an **AI Career Assistant**: a full-stack application
intended to accept a user's resume, understand its contents, extract
career-relevant information such as skills, compare the user's profile
against jobs/career paths, and eventually provide AI-powered career
recommendations.

The backend has intentionally been built incrementally rather than
jumping immediately into AI. The progression has been:

1.  API/backend foundation.
2.  User registration and authentication.
3.  Protected user profile access.
4.  Resume upload.
5.  File validation and storage.
6.  Resume PDF text extraction.
7.  Persist extracted resume text.
8.  Planned skill extraction.
9.  Planned career/job matching.
10. Planned AI recommendations.
11. Frontend/dashboard.

The latest direction changed the immediate priority: **pause further
backend intelligence work and start the frontend now**, while keeping
the working backend as the foundation.

## 1.2 Intended user/problem

The intended user is a job seeker/career-oriented user who wants to
upload a resume and receive structured career assistance rather than
manually interpreting skills and job fit.

The planned problem-solving flow is approximately:

`User account -> upload resume -> parse resume -> understand skills/profile -> compare to roles/jobs -> provide career/AI recommendations -> present results in a usable dashboard`

The project is not intended to remain merely an
authentication/file-storage demo. The user explicitly wants it to become
a **real AI Career Assistant**.

## 1.3 Original goals and evolution

The project began backend-first. Authentication and resume ingestion
were treated as prerequisites before implementing AI features.

After successfully storing extracted resume text, the next proposed
backend feature was skill extraction. The user then explicitly asked:

> "can we stop so far and start on frontend"

Therefore the **latest decision** is: - Preserve the current backend. -
Begin the React frontend. - Return later to skill extraction, matching,
and AI features.

## 1.4 Definition of a successful finished project

From the discussion, a successful finished application should at minimum
allow a user to:

-   Register an account.
-   Log in securely.
-   Remain authenticated when using protected functionality.
-   View their user/profile context.
-   Upload a PDF resume.
-   Have the backend validate and save the resume.
-   Extract text from the PDF.
-   Store that extracted text.
-   Analyze the resume for skills.
-   Use the profile/resume information for career or job matching.
-   Receive AI-assisted recommendations.
-   Interact with these capabilities through a proper frontend/dashboard
    instead of only Postman.

A polished final version should feel like an actual career-assistance
product rather than a collection of isolated API endpoints.

## 1.5 Learning / portfolio / production intent

The conversation strongly establishes a **learning-oriented,
portfolio-quality development process**. The user wants to understand
what is being built rather than blindly copy code. The assistant
explicitly used a "concept -\> file location -\> code -\> test -\> Git
commit" teaching sequence and explained concepts such as service-layer
separation, JWT, HTTP status codes, and API testing.

A strict production deployment requirement has **not** been established.
Production hosting, scale, privacy/compliance, monitoring, payment,
multi-tenancy, and production security hardening have not yet been
specified.

------------------------------------------------------------------------

# 2. REQUIREMENTS AND SCOPE

## 2.1 Confirmed/expected functional requirements

### Account management

-   Register a user with at least:
    -   full name
    -   email
    -   password
-   Prevent duplicate email registration.
-   Log in with email/password.
-   Return a JWT bearer access token after successful login.
-   Reject invalid credentials.
-   Support authenticated/protected routes.
-   `GET /users/me` should return the authenticated user's profile.
-   Protected endpoints should reject missing authentication with
    `401 Unauthorized`.

### Resume ingestion

-   Authenticated users can upload resumes.
-   Current accepted format: **PDF only**.
-   Multipart form-data field name: `resume_file`.
-   Reject non-PDF extensions.
-   Reject uploads whose content type is not `application/pdf`.
-   Save uploaded PDFs to a local `uploads` directory.
-   Generate a unique stored filename (the shared implementation used
    UUID-based `.pdf` names).
-   Persist resume metadata to SQLite.
-   Associate each resume with the authenticated user.
-   Extract text from uploaded PDFs.
-   Persist extracted text in the database.

### Resume intelligence --- planned

-   Clean/normalize extracted resume text.
-   Extract skills from resume text.
-   Return skills through the API.
-   Later compare the user's resume/profile with careers/jobs.
-   Later provide AI recommendations.

### Frontend --- latest priority

Planned frontend workflow: - React application. - Login page. -
Registration page. - Dashboard. - Resume upload UI. - Connect
registration/login to FastAPI. - Store/use JWT for protected API
requests. - Connect resume upload to backend. - Display resume
information. - Later display skills and AI analysis/recommendations.

## 2.2 Expected user workflow

Planned end-to-end user flow:

1.  Open frontend.
2.  Register or log in.
3.  Frontend sends credentials to FastAPI.
4.  Login returns JWT.
5.  Frontend retains the token and uses it for protected requests.
6.  User enters dashboard.
7.  User uploads a PDF resume.
8.  Frontend sends multipart form-data with bearer authorization.
9.  Backend validates PDF.
10. Backend stores file and metadata.
11. Backend extracts PDF text.
12. Backend persists extracted text.
13. Future: skill extraction operates on stored text.
14. Future: job/career matching operates on structured resume/profile
    data.
15. Future: AI generates useful recommendations/gap analysis.
16. Frontend displays those results.

## 2.3 Technical preferences / constraints expressed

-   Backend: Python + FastAPI.
-   ORM/database access: SQLAlchemy.
-   Development database: SQLite.
-   Authentication: JWT bearer token.
-   API testing: **Postman preferred** over browser/Swagger for
    continued testing.
-   Frontend latest recommendation/decision: React + Vite, JavaScript
    variant.
-   Local Windows development environment.
-   VS Code is being used.
-   Current local backend URL: `http://127.0.0.1:8000`.
-   Planned Vite dev URL: normally `http://localhost:5173/`.
-   User wants incremental implementation and verification.
-   Test each important API behavior before advancing.
-   Explanations should include exact method, URL, Postman tab/body
    settings, expected status code, and what the result proves.
-   Avoid rushing through many features at once.
-   User is now moving development to **Codex in the IDE**.

## 2.4 MVP vs later versions

### Reasonable MVP implied by the conversation

The conversation did not formally label an MVP, but the implied first
useful product includes: - Account registration/login. - JWT
authentication. - Dashboard. - PDF resume upload. - Resume text
extraction. - Basic skill extraction. - Some useful career/job matching
or career recommendations. - Frontend displaying the result.

### Later / advanced scope

-   More sophisticated AI recommendations.
-   More advanced job matching.
-   Richer AI/NLP analysis.
-   Production deployment/hardening.
-   More file formats such as DOCX, unless requirements change.
-   Advanced frontend/dashboard polish.
-   External job-data integrations, if later chosen.

## 2.5 Rejected/postponed ideas

### DOCX upload

Current backend intentionally rejects DOCX. This was explicitly tested
with a `.docx` file and correctly returned: `400 Bad Request` with:
`{"detail": "Only PDF resumes are allowed"}`

This is not currently considered a bug. PDF-only was the active
requirement.

### Skill extraction

This was the next backend feature, but it was **postponed**, not
rejected, because the user chose to start frontend development first.

### Full AI implementation

Postponed until the basic data pipeline and UI exist. No AI
provider/API/model has yet been confirmed.

------------------------------------------------------------------------

# 3. TECHNICAL DESIGN

## 3.1 Known stack

### Backend

-   Python
-   FastAPI
-   SQLAlchemy
-   SQLite
-   JWT authentication
-   Password hashing/verification through `app.security`
-   Uvicorn for local development
-   Multipart file upload
-   A PDF parsing service is present based on current repository
    screenshot/behavior.

### PDF parsing

ChatGPT recommended **PyMuPDF** (`pymupdf`, imported as `fitz`) and a
service file `app/services/resume_parser.py`. The repository screenshot
shows `resume_parser.py` exists and resume extraction works. Codex must
verify whether PyMuPDF/`fitz` is in fact the implementation currently
used.

### Frontend

Latest selected direction: - React - Vite - JavaScript

Frontend setup was recommended but **not confirmed executed** before
this handoff.

### Development/testing

-   VS Code
-   Postman
-   Git
-   GitHub

## 3.2 Why these choices were made

-   FastAPI: clean Python API development and appropriate for
    incremental backend/AI work.
-   SQLite: low-friction development database for learning and local
    prototyping.
-   JWT: stateless authentication suitable for frontend/backend
    separation.
-   React + Vite: simple modern frontend setup that can consume the
    FastAPI API.
-   Service layer: PDF parsing should not be embedded directly in route
    handlers; reusable/business logic should live separately.

## 3.3 Known repository paths

Project root: `C:\Users\mrara\ai-career-assistant`

Backend: `C:\Users\mrara\ai-career-assistant\backend`

Observed backend structure:

``` text
ai-career-assistant/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── resumes.py
│   │   │   └── users.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── resume_parser.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── jwt_handler.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── oauth2.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── uploads/
│   ├── career_assistant.db
│   ├── requirements.txt
│   └── .gitignore
└── [frontend planned here]
```

The latest screenshot confirms `services`, `resume_parser.py`,
`uploads`, and `career_assistant.db` exist.

## 3.4 Known database models/schema information

Exact complete `models.py` has not been captured verbatim in the
available context. Known fields can be inferred from shared code and
successful database behavior.

### User

Known usage: - `id` - `full_name` - `email` - `hashed_password`

Likely additional fields may exist, but Codex must inspect `models.py`.

### Resume

Known/observed fields: - `id` - `original_filename` -
`stored_filename` - `file_path` - `resume_text` - `user_id` -
`uploaded_at`

The latest SQLite screenshot confirms a `resume_text` field containing
actual extracted resume content. It also shows one resume row.

The originally suggested model addition was:

``` python
resume_text = Column(Text, nullable=True)
```

Behavior confirms an equivalent field exists, but Codex should verify
exact declaration.

## 3.5 Known API endpoints

### Root

`GET /`

Confirmed response:

``` json
{
  "message": "AI Career Assistant API is running."
}
```

Confirmed `200 OK`.

### Register

`POST /auth/register`

Shared route:

``` python
@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
```

Behavior: - Looks up existing user by email. - Duplicate -\>
`409 Conflict`, detail `"Email already registered"`. - Hashes
password. - Creates user. - Returns user response.

### Login

`POST /auth/login`

Shared route:

``` python
@router.post(
    "/login",
    response_model=schemas.TokenResponse,
)
```

Behavior: - Lookup user by email. - Invalid email/password -\>
`401 Unauthorized`, detail `"Invalid email or password"`. -
`verify_password(...)`. - Generates JWT using:

``` python
create_access_token(
    data={
        "sub": str(user.id),
        "email": user.email,
    }
)
```

-   Returns:

``` json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

A login was successfully tested and returned `200 OK` with a JWT. Do not
place prior test passwords/tokens in project documentation.

### Current user

`GET /users/me`

Shared code:

``` python
@router.get(
    "/me",
    response_model=schemas.UserResponse,
)
def get_my_profile(
    current_user: models.User = Depends(get_current_user),
):
    return current_user
```

Confirmed: - Valid bearer token -\> `200 OK`. - No token -\>
`401 Unauthorized`:

``` json
{
  "detail": "Not authenticated"
}
```

### Resume upload

`POST /resumes/upload`

Authentication required.

Multipart: - Body -\> form-data - key: `resume_file` - type: File

Confirmed PDF upload -\> `201 Created`.

A demonstrated response looked like:

``` json
{
  "id": 1,
  "original_filename": "Vamshi_N Resume.pdf",
  "user_id": 5,
  "uploaded_at": "..."
}
```

IDs/timestamps are test data and should not be hardcoded.

Confirmed DOCX upload -\> `400 Bad Request`:

``` json
{
  "detail": "Only PDF resumes are allowed"
}
```

## 3.6 Resume upload code originally shared by user

This was explicitly shared before the text-persistence enhancement:

``` python
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

@router.post(
    "/upload",
    response_model=schemas.ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_resume(
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    original_filename = Path(resume_file.filename or "").name

    if not original_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A filename is required",
        )

    file_extension = Path(original_filename).suffix.lower()

    if file_extension != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resumes are allowed",
        )

    if resume_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file must be a PDF",
        )

    stored_filename = f"{uuid4()}.pdf"
    destination = UPLOAD_DIRECTORY / stored_filename

    try:
        with destination.open("wb") as output_file:
            shutil.copyfileobj(
                resume_file.file,
                output_file,
            )
    except OSError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save the uploaded resume",
        )
    finally:
        resume_file.file.close()

    new_resume = models.Resume(
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=str(destination),
        user_id=current_user.id,
    )

    try:
        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)
    except Exception:
        db.rollback()

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save resume information",
        )

    return new_resume
```

**Important:** This exact snippet predates confirmed text persistence.
The repository now has modifications (`resumes.py` and `models.py`
showed `M` in VS Code), so Codex must inspect current files instead of
restoring this older version.

## 3.7 Authentication code explicitly shared by user

`app/routers/auth.py`:

``` python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.security import hash_password, verify_password
from app.jwt_handler import create_access_token

from app import models, schemas
from app.dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    hashed_password = hash_password(user.password)

    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post(
    "/login",
    response_model=schemas.TokenResponse,
)
def login_user(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == credentials.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    password_is_correct = verify_password(
        credentials.password,
        user.hashed_password,
    )

    if not password_is_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
```

Again, Codex should compare this with the current repository before
modifying it.

## 3.8 User route explicitly shared

`app/routers/users.py`:

``` python
from fastapi import APIRouter, Depends

from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "/me",
    response_model=schemas.UserResponse,
)
def get_my_profile(
    current_user: models.User = Depends(get_current_user),
):
    return current_user
```

## 3.9 PDF parser design suggested and apparently implemented

Suggested file: `app/services/resume_parser.py`

Suggested implementation:

``` python
import fitz

def extract_text_from_pdf(file_path: str) -> str:
    document = fitz.open(file_path)

    extracted_text = ""

    for page in document:
        extracted_text += page.get_text()

    document.close()

    return extracted_text.strip()
```

The user later showed `resume_parser.py` in the repository and
demonstrated extracted text persisted in SQLite. Therefore **PDF
extraction behavior is confirmed**, but the exact current
code/dependency should be verified.

## 3.10 Data flow currently confirmed

``` text
Postman
  -> FastAPI route
  -> JWT authentication
  -> PDF extension/content-type validation
  -> filesystem save under uploads/
  -> Resume database row
  -> PDF text extraction
  -> resume_text persisted in SQLite
  -> 201 Created
```

The latest screenshot showed extracted resume content beginning with the
user's name/contact section and summary, and the terminal showed the
upload returning `201 Created`.

## 3.11 Important design decisions

### Separate service layer

PDF parsing was moved/planned outside `routers/resumes.py` into
`services/resume_parser.py`. Reason: route handlers should focus on
HTTP/request orchestration, while parsing/business logic should be
reusable and independently maintainable.

### PDF-only validation

The API deliberately enforces PDF-only resumes. The failure test for
DOCX was used to teach that a `400` can represent correct behavior.

### Backend-first, then frontend

The project deliberately established authentication and resume
processing before frontend work. The user has now decided the backend is
sufficiently developed to pause and build the UI.

### Postman as API checkpoint tool

The user prefers concrete Postman tests and successfully used it to
validate endpoints.

------------------------------------------------------------------------

# 4. IMPLEMENTATION STATUS

## 4.1 Confirmed implemented and working

### Git repository

Confirmed: - Git initialized at project root, not inside `backend`. -
Initial commit message: `Initial backend setup`. - Branch renamed
`master` -\> `main`. - Remote changed to the `ai-career-assistant`
GitHub repository. - `git push -u origin main` succeeded. - At that
earlier checkpoint, `git status` showed branch up to date and working
tree clean.

**Current caveat:** latest VS Code screenshot shows modified/untracked
files after subsequent work, so later PDF-text work may not yet be
committed/pushed.

### FastAPI application

Confirmed local server runs using:

``` powershell
uvicorn app.main:app --reload
```

### Root health endpoint

Confirmed `GET /` -\> `200 OK` and API-running message.

### Registration

Registration code exists. A user was successfully created/recreated
during testing.

### Login/JWT

Confirmed successful login returns JWT.

### Protected user profile

Confirmed: - valid bearer token -\> `GET /users/me` returns `200 OK` -
no token -\> `401 Unauthorized`, `"Not authenticated"`

### Resume upload

Confirmed: - valid authenticated PDF -\> `201 Created` - response
contains resume metadata - file is saved/persisted

### PDF-only validation

Confirmed `.docx` -\> `400 Bad Request` with:
`"Only PDF resumes are allowed"`

### Resume PDF text extraction

Confirmed by latest VS Code screenshot: - actual resume text visible in
SQLite `resume_text`. - terminal showed extracted resume text and
`201 Created`.

### Resume text persistence

Confirmed by SQLite Viewer screenshot: `resume_text` contains extracted
text.

## 4.2 Implemented but repository details need verification

### PDF parser implementation

Behavior works, and `app/services/resume_parser.py` exists. Exact parser
library/code should be inspected.

### Resume model migration/recreation

The database contains `resume_text`, so the schema change is effective
locally. However: - No migration framework was established. - The
development workflow suggested deleting/recreating SQLite. - Codex must
verify whether the DB schema is created through
`Base.metadata.create_all` and whether a migration solution is needed
later.

### Current `resumes.py`

The latest screenshot marks it modified (`M`). It likely contains
extraction/persistence logic, but the exact current code was not
supplied verbatim after modification.

### Current `models.py`

Also marked modified (`M`) in screenshot. Exact declaration needs
inspection.

## 4.3 Discussed/suggested but not confirmed implemented

### `skill_extractor.py`

Suggested: `app/services/skill_extractor.py`

Not confirmed created.

### Skills endpoint

Suggested: `GET /resumes/{resume_id}/skills`

Not confirmed implemented.

### Frontend directory/project

Suggested:

``` powershell
npm create vite@latest frontend
```

then select React -\> JavaScript, followed by:

``` powershell
cd frontend
npm install
npm run dev
```

The user asked for the handoff before confirming that these commands
were run. Therefore **do not assume `frontend/` exists**.

### CORS

Not yet discussed/confirmed in the available history. This will be
necessary when React on port 5173 calls FastAPI on port 8000.

### Frontend JWT storage strategy

Planned conceptually, but exact implementation/storage choice was not
decided.

## 4.4 Not started

-   Frontend pages/components, unless repository inspection proves
    otherwise.
-   Frontend API client.
-   Frontend authentication state.
-   Frontend protected routes.
-   Resume upload frontend.
-   Skill extraction.
-   Resume normalization/cleaning beyond raw parser output.
-   Job/career matching.
-   AI recommendation engine.
-   AI provider/model integration.
-   Job API/data-source integration.
-   Automated backend test suite.
-   Frontend tests.
-   Production deployment.
-   CI/CD.
-   Production database.
-   Formal migrations.
-   Production-grade file storage.
-   Monitoring/logging/security hardening.

## 4.5 Blocked/broken

No currently confirmed blocker.

Previously encountered and resolved/understood issues:

### Postman Cloud Agent / localhost

Error: `Cloud agent error: cannot send request`

Cause: Postman Web Cloud Agent cannot access localhost.

Resolution: use Postman Desktop/Desktop Agent. Local requests later
worked.

### Unauthorized resume upload

Initial `POST /resumes/upload` returned:

``` json
{
  "detail": "Not authenticated"
}
```

Cause: no bearer token.

Resolution: log in, copy `access_token`, set Postman Authorization -\>
Bearer Token. Upload then succeeded.

### DOCX upload

Returned `400 Bad Request`, `"Only PDF resumes are allowed"`. This is
expected validation, not a bug.

### Git `.venv` staging issue

Earlier, `.venv` contents were accidentally picked up and produced many
LF -\> CRLF warnings. `.gitignore` should exclude `.venv`.

Codex should verify `.venv` is not currently tracked:

``` bash
git status
git ls-files | findstr /i ".venv"
```

(or equivalent Git command in the IDE terminal).

------------------------------------------------------------------------

# 5. EXACT STOPPING POINT

## 5.1 Last completed backend checkpoint

The user showed VS Code with: - `career_assistant.db` open in SQLite
Viewer. - `resumes` table selected. - `resume_text` populated with
actual extracted resume content. - terminal output showing resume
text. - terminal line: `POST /resumes/upload HTTP/1.1" 201 Created`

The user also stated they had already created the new user.

Therefore the backend checkpoint is:

**Authenticated PDF resume upload -\> extraction -\> database
persistence is working.**

## 5.2 Last task being worked on

After that successful backend checkpoint, the user asked:

> "can we stop so far and start on frontend"

The assistant agreed and recommended React + Vite.

The exact frontend setup instructions given were: 1. Stop backend with
`Ctrl + C` if desired. 2. Open terminal at:
`C:\Users\mrara\ai-career-assistant` 3. Run:
`powershell    npm create vite@latest frontend` 4. Select: - Framework:
React - Variant: JavaScript 5. Run:
`powershell    cd frontend    npm install    npm run dev` 6. Expect Vite
at approximately: `http://localhost:5173/` 7. Do not start design yet;
first verify the default Vite/React page.

**No confirmation was received that frontend setup was actually
executed.**

## 5.3 Latest confirmed working behavior

-   Backend runs locally.
-   User authentication works.
-   Protected routes work.
-   PDF resume upload works.
-   Non-PDF rejection works.
-   PDF text extraction works.
-   Extracted resume text is stored in SQLite.

## 5.4 Current errors/bugs

None confirmed at stopping point.

Potential issue to verify: - `resumes.py` and `models.py` were marked
modified. - `services/__init__.py` and `services/resume_parser.py` were
marked untracked (`U`) in the screenshot. - This strongly suggests the
latest resume parsing work had not yet been committed to Git at the
moment of the screenshot. - Verify with `git status`.

## 5.5 Intended next task

The immediate next task is **frontend setup and initial frontend
architecture**, not skill extraction.

After frontend setup: - Build/clean basic React structure. - Add
registration/login UI. - Connect to FastAPI. - Add CORS backend
configuration as needed. - Handle JWT. - Add dashboard and resume
upload. - Verify end-to-end upload through the browser UI. - Then resume
backend intelligence work.

------------------------------------------------------------------------

# 6. REMAINING WORK

The following is an ordered plan based on the user's latest priorities.

## Phase A --- Repository verification before modifying anything

1.  Run `git status`.
2.  Inspect current:
    -   `backend/app/main.py`
    -   `backend/app/models.py`
    -   `backend/app/schemas.py`
    -   `backend/app/routers/auth.py`
    -   `backend/app/routers/users.py`
    -   `backend/app/routers/resumes.py`
    -   `backend/app/services/resume_parser.py`
    -   `backend/app/jwt_handler.py`
    -   `backend/app/oauth2.py`
    -   `backend/app/security.py`
    -   `backend/requirements.txt`
    -   `.gitignore`
3.  Verify whether `frontend/` already exists.
4.  Verify PDF library actually used.
5.  Verify `.venv`, database, uploads, and secrets are ignored
    appropriately.
6.  Do not overwrite working backend code with older snippets from this
    handoff.

Acceptance: - Codex can state the actual current repository state and
differences from this handoff.

## Phase B --- Preserve current backend checkpoint

Before frontend changes, make sure current backend work is safely
committed if user wants it committed.

Suggested checkpoint:

``` bash
git status
git add backend/app backend/requirements.txt backend/.gitignore
git commit -m "Add resume text extraction and persistence"
git push
```

Do not blindly use this exact `git add` command if repo paths/ignore
rules differ. Do not commit `career_assistant.db`, uploaded resumes,
`.venv`, or secrets.

Acceptance: - Working backend changes are version-controlled. - No
virtualenv/database/uploaded resume/secrets accidentally committed.

## Phase C --- Create React/Vite frontend

If `frontend/` does not exist:

``` powershell
cd C:\Users\mrara\ai-career-assistant
npm create vite@latest frontend
```

Select React + JavaScript.

Then:

``` powershell
cd frontend
npm install
npm run dev
```

Acceptance: - React dev server starts. - Default app loads in browser. -
No need for backend integration yet.

## Phase D --- Establish frontend structure

Planned structure:

``` text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── vite.config.js
```

Likely pages: - Login - Register - Dashboard - Resume upload/dashboard
section

Do not overengineer state management initially.

## Phase E --- Backend CORS

Because frontend and backend use different origins during development,
configure FastAPI CORS for the Vite development origin.

Acceptance: - Browser requests from the frontend origin to
`http://127.0.0.1:8000` succeed without CORS errors. - Avoid permissive
production CORS assumptions later.

## Phase F --- Frontend authentication

Implement: - Register form -\> `POST /auth/register`. - Login form -\>
`POST /auth/login`. - Capture `access_token`. - Attach bearer token to
protected requests. - `GET /users/me` to verify current user. - Logout
behavior.

A secure production token-storage strategy is not yet decided. For
learning/local MVP, choose a clear strategy and explain tradeoffs to the
user.

Acceptance: - User can register/login from UI. - Wrong credentials show
understandable error. - Protected user data loads after login. -
Unauthenticated access to protected UI is handled.

## Phase G --- Resume upload frontend

Implement: - File picker. - PDF-only UI validation consistent with
backend. - Multipart form-data key exactly `resume_file`. -
Authorization header. - Upload state/error/success feedback. - Call
`POST /resumes/upload`.

Acceptance: - PDF upload from browser returns `201`. - DOCX is prevented
or clearly rejected. - Missing/expired auth is handled. - Response
metadata is displayed.

## Phase H --- Resume retrieval/API design

Current known API supports upload, but no confirmed endpoint exists for
listing/getting a user's uploaded resumes or extracted text.

Codex should decide with the user whether to add: - `GET /resumes` -
`GET /resumes/{id}` - possibly delete/replace resume endpoints

Authorization must ensure users only access their own resumes.

Acceptance: - Dashboard can retrieve persistent resume state after
refresh, rather than relying only on upload response.

## Phase I --- Resume text cleaning/normalization

Planned but not implemented.

Acceptance: - Extracted text is normalized enough for reliable skill
extraction. - Original extracted text can remain available if useful.

## Phase J --- Skill extraction

Previously planned next backend feature:
`app/services/skill_extractor.py`

Potential endpoint suggested: `GET /resumes/{resume_id}/skills`

Do not assume a simplistic keyword list is the final design; first
define expected skill taxonomy/behavior.

Acceptance: - Given stored resume text, backend returns a structured
list of detected skills. - User ownership is enforced. - Results are
testable in Postman and then displayed in frontend.

## Phase K --- Career/job matching

Requirements need further definition: - Are jobs fetched live? - Are
roles drawn from an internal catalog? - Is matching
semantic/embedding-based, rule-based, LLM-based, or hybrid? - What
should the score mean?

Acceptance criteria should be agreed before implementation.

## Phase L --- AI recommendations

No provider/model is selected yet.

Potential outputs: - best-fit roles - skill gaps - learning
recommendations - resume improvement suggestions - explanation of match

Before implementation, decide: - AI provider/model. - Cost limits. -
Prompt/data handling. - Whether resume text leaves local system. -
Structured output schema. - Failure/rate-limit handling.

## Phase M --- Polish/testing/deployment

Later: - backend automated tests - frontend tests - input/file-size
validation - PDF security considerations - database migrations -
environment variables - production database/storage - logging -
deployment - README/screenshots - portfolio documentation

------------------------------------------------------------------------

# 7. USER WORKING PREFERENCES

## 7.1 Experience level

The user is learning full-stack/backend concepts while building the
project. They can follow code and terminal commands, but benefit from
concrete explanation of: - what a file does - where to create it - why
it exists - exact command to run - exact API method/URL - what to click
in Postman - expected HTTP response/status - what a successful result
proves

Do not assume familiarity with tooling details merely because a feature
is already working.

## 7.2 Preferred teaching style

Use incremental checkpoints:

`Concept -> implement one small change -> run -> test -> inspect result -> commit -> next`

The user responded well to this.

Avoid dumping a large architecture or many files at once unless
explicitly requested.

## 7.3 Testing preference

User explicitly prefers **Postman** for API testing.

For Postman instructions, be precise: - method - URL - Authorization
tab - Bearer Token - Body type - field names - expected status -
expected response

For bearer auth: - paste only token into Postman's Token field - do not
manually prepend `Bearer` when using the Bearer Token auth type.

## 7.4 Coding/architecture preference

The user accepted: - modular routers - service layer - separate
frontend/backend - incremental architecture

They want to learn why architecture is structured that way.

## 7.5 Pacing

Focus on one working checkpoint at a time. The user often replies with
short messages like `"next"` after completing a step.

## 7.6 Cost constraints

No explicit project-wide cloud/API budget was established in this
project discussion. Do not assume paid AI APIs are acceptable. Ask
before introducing recurring paid services.

## 7.7 Current development tool change

The user is now moving project development to **Codex in their IDE**.
Codex should inspect the repository directly and use this handoff as
context, not as a substitute for repository truth.

------------------------------------------------------------------------

# 8. CONTEXT AND VERIFICATION GAPS

## 8.1 Latest decisions that supersede earlier plans

### Backend skill extraction vs frontend

Earlier: - Next planned step was skill extraction.

Latest: - User explicitly chose to pause backend work and start
frontend.

Therefore frontend is the immediate priority.

### Database recreation

At one point the assistant suggested deleting/recreating
`career_assistant.db` to add `resume_text` because no migration
framework was in use. The user later showed the new field populated and
said they had already created a new user. That work is complete locally.
Do not delete the database again unless there is a new reason.

## 8.2 Suggested code vs confirmed code

Codex must verify: - Exact `models.py`. - Exact `schemas.py`. - Exact
`resumes.py` after parser integration. - Exact `resume_parser.py`. -
Exact PDF dependency. - Exact JWT implementation/expiration/secret
loading. - Whether `main.py` uses `Base.metadata.create_all`. - Whether
router inclusion is exactly as expected. - Whether CORS exists
already. - Whether frontend has since been created. - Whether latest
changes are committed.

Do not assume the assistant's suggested snippets equal current files.

## 8.3 Git ignore / repository hygiene gap

Earlier `.venv` content was accidentally staged and caused extensive LF
-\> CRLF warnings.

Expected `.gitignore` coverage should include at least:

``` gitignore
.venv/
__pycache__/
*.pyc
*.db
uploads/
.env
```

But exact current `.gitignore` must be inspected.

Also verify whether the root `.gitignore` or backend `.gitignore`
location matches repository layout.

## 8.4 Security gaps

Unknown/unverified: - JWT secret source. - Token expiration. -
Algorithm. - Password hashing algorithm. - Environment variable
handling. - CORS. - Rate limiting. - Upload size limits. - PDF content
safety. - Filename/storage security beyond `Path(...).name` and UUID. -
Refresh tokens. - Email verification. - Password reset. - Account
deletion.

These are not blockers for the immediate learning MVP, but must not be
presented as already solved.

## 8.5 Database gaps

-   SQLite is current local DB.
-   No confirmed Alembic/migration framework.
-   Relationships/cascade behavior not documented.
-   Unique/index constraints beyond what appeared in snippets need
    inspection.
-   One or multiple resumes per user has not been formally decided.
-   Resume replacement/versioning policy has not been decided.

## 8.6 Frontend gaps

No confirmed decisions yet for: - CSS approach (plain CSS, Tailwind,
component library, etc.). - Routing library. - State management. - Token
storage. - dashboard visual design. - responsive/mobile requirements. -
accessibility requirements.

Start simple; ask only when a choice materially affects implementation.

## 8.7 AI gaps

No confirmed: - LLM provider/model. - embeddings provider. - vector
database. - job data provider. - prompt architecture. - skill
taxonomy. - matching algorithm. - recommendation output schema. -
cost/privacy policy.

Do not invent these choices.

## 8.8 Resume content

A resume PDF was used successfully for testing and parsing. It included
a Java full-stack profile and skills/projects. That file is test input,
not a hardcoded application profile. The application must remain generic
for arbitrary users.

## 8.9 Questions still unanswered

Questions Codex may need to resolve later, preferably when relevant
rather than all at once:

1.  Should each user have one active resume or multiple saved resumes?
2.  Should users be able to delete/replace resumes?
3.  Should the dashboard show raw extracted resume text?
4.  What exact skill categories should be extracted?
5.  What is the intended career/job matching source?
6.  Should the app target general software/IT careers or all careers?
7.  Which AI provider/model is acceptable?
8.  What AI/API budget is acceptable?
9.  Is the final app expected to be publicly deployed?
10. What frontend visual style does the user want?
11. What token-storage/auth strategy should be used for the MVP versus
    production?
12. Should DOCX support be added later?
13. What file-size/page-count limits should apply?
14. Is resume analysis performed automatically on upload or via a
    separate Analyze action?

------------------------------------------------------------------------

# 9. COMMANDS / TESTING REFERENCE

## Backend working directory

``` powershell
cd C:\Users\mrara\ai-career-assistant\backend
```

## Start backend

``` powershell
uvicorn app.main:app --reload
```

Expected base URL: `http://127.0.0.1:8000`

## Frontend planned working directory

``` powershell
cd C:\Users\mrara\ai-career-assistant
```

## Planned Vite creation

``` powershell
npm create vite@latest frontend
```

Choose React -\> JavaScript.

Then:

``` powershell
cd frontend
npm install
npm run dev
```

Expected default local URL is normally: `http://localhost:5173/`

## API testing reference

### Register

``` text
POST http://127.0.0.1:8000/auth/register
Content-Type: application/json
```

Body schema:

``` json
{
  "full_name": "Example User",
  "email": "example@example.com",
  "password": "<user supplied password>"
}
```

Do not put real passwords into repository documentation.

### Login

``` text
POST http://127.0.0.1:8000/auth/login
Content-Type: application/json
```

Body:

``` json
{
  "email": "example@example.com",
  "password": "<user supplied password>"
}
```

Expected:

``` json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

### Current user

``` text
GET http://127.0.0.1:8000/users/me
Authorization: Bearer <JWT>
```

### Resume upload

``` text
POST http://127.0.0.1:8000/resumes/upload
Authorization: Bearer <JWT>
Body: form-data
resume_file: [File]
```

Expected valid PDF: `201 Created`

Expected `.docx`: `400 Bad Request`

``` json
{
  "detail": "Only PDF resumes are allowed"
}
```

Expected missing auth: `401 Unauthorized`

``` json
{
  "detail": "Not authenticated"
}
```

------------------------------------------------------------------------

# 10. GIT / GITHUB HISTORY

Known sequence: 1. Git initialized at `ai-career-assistant` project
root. 2. Initial backend commit: `Initial backend setup` 3. Branch
renamed:

``` bash
git branch -M main
```

4.  Original remote pointed to an older/different repository:
    `AI-ML-PROJECT.git`
5.  Remote changed to the intended `ai-career-assistant` repository.
6.  Push:

``` bash
git push -u origin main
```

succeeded. 7. At that earlier point:

``` text
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

Later screenshot showed: - `resumes.py` modified - `models.py`
modified - `services/__init__.py` untracked -
`services/resume_parser.py` untracked

So first Codex action should include `git status` and protecting these
working changes.

Do not expose or add credentials/tokens to Git.

------------------------------------------------------------------------

# 11. DEVELOPMENT LESSONS / CONCEPTS ALREADY COVERED

The user has already been introduced to these concepts, though
explanations may still be useful:

-   HTTP methods and status codes.
-   `200 OK` vs `201 Created`.
-   `400 Bad Request` can be correct expected validation.
-   `401 Unauthorized` from missing auth.
-   FastAPI routers.
-   Dependency injection using `Depends`.
-   SQLAlchemy session usage.
-   Password hashing vs storing raw passwords.
-   JWT bearer authentication.
-   Protected endpoints.
-   Multipart `form-data`.
-   File validation.
-   Filesystem storage.
-   Database persistence.
-   PDF text extraction.
-   Service-layer separation.
-   Git/GitHub basics.
-   Postman testing.

A useful mental model previously presented was:

``` text
Postman
  -> FastAPI routing
  -> request validation
  -> JWT authentication
  -> dependency injection
  -> file upload
  -> file validation
  -> filesystem storage
  -> SQLAlchemy database operation
  -> HTTP response
```

The next learning transition is from API-only development to
frontend/backend integration.

------------------------------------------------------------------------

# 12. NEXT SESSION HANDOFF

## Current state in one paragraph

The AI Career Assistant has a working FastAPI/SQLite backend with
registration, login/JWT, protected `GET /users/me`, authenticated
PDF-only resume upload, local file storage, PDF text extraction, and
persistence of extracted text into a `resume_text` database field. PDF
upload has been verified with `201 Created`; DOCX rejection with `400`;
missing auth with `401`; and SQLite Viewer visibly contains the
extracted resume text. Skill extraction, career/job matching, and AI
recommendations have not yet been built. The user deliberately paused
backend intelligence work to begin the frontend. React + Vite +
JavaScript was selected/recommended, but frontend creation was not
confirmed before this handoff.

## First concrete task for Codex

**Inspect before editing.**

1.  Run `git status`.
2.  Inspect the repository tree.
3.  Confirm and preserve the currently modified/untracked resume
    parser/persistence work.
4.  Verify `.gitignore` prevents `.venv`, `*.db`, `uploads`, `.env`,
    etc. from being committed.
5.  Check whether `frontend/` exists.
6.  If it does not exist, create the React/Vite JavaScript frontend at
    project root.
7.  Start it and verify the default Vite page before implementing
    application UI.
8.  Then establish the minimal frontend structure and prepare for
    FastAPI integration, adding development CORS only when needed.

Do **not** begin skill extraction first; the latest user decision is
frontend-first.

------------------------------------------------------------------------

# 13. CODEX OPERATING INSTRUCTIONS FOR THIS PROJECT

-   Treat the actual repository as the source of truth.
-   Do not replace working code simply because a different version
    appears in this handoff.
-   Distinguish confirmed behavior from proposed architecture.
-   Preserve the working backend while adding frontend.
-   Work incrementally and explain changes in plain language.
-   Prefer one checkpoint at a time.
-   After meaningful changes, tell the user exactly how to run/test
    them.
-   For API behavior, use concrete method/URL/body/status examples.
-   Never hardcode or expose passwords, JWTs, API keys, secrets, or
    personal test data.
-   Keep AI provider choices open until the user decides cost/privacy
    requirements.
-   Keep the application generic; do not hardcode the test resume's
    career profile.
-   Before major architecture additions, explain why they are needed.
