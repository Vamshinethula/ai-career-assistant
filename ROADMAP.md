# ROADMAP.md — AI Career Assistant

## Comparison export checkpoint - 2026-09-18

Completed JSON download with automatic/user provenance and verified real-browser file output. Next workflow checkpoint: review and commit accumulated feature work, then verify updated GitHub Actions including frontend unit tests. Further product scope can follow a stable checkpoint; saved comparisons/import/PDF reports remain unimplemented.

## User label review checkpoint - 2026-09-18

Completed temporary label corrections with source provenance and both-mode browser verification. Suggested next feature: export the reviewed comparison with automatic/user labels, score meaning and limitations. Saved comparison persistence and reviewed scoring remain unimplemented; backend remains at 74 verified tests.

## Requirement labels visible in comparison - 2026-09-18

Completed API/client/UI integration with source evidence and unchanged keyword score; all 74 backend tests and both browser modes pass. Suggested next product checkpoint: explicit user review/correction of uncertain labels, with scope and persistence defined before any requirement-based scoring. Broader independent semantic evaluation remains needed. Hosting remains separate.

## Requirement classification service - 2026-09-18

Completed standalone conservative classifier and evidence output, verified against 22 policy examples and full 72-test backend suite. Next checkpoint: add labels/source excerpts to comparison API/UI while preserving existing scores; verify schemas, ownership, error handling and browser presentation. Independent semantic evaluation and broader coverage remain future work.

## Context evaluation complete - 2026-09-18

Completed reproducible job-context evaluation and documented gaps; 16/16 keyword-contract cases and 67 backend tests pass. Added explicit score interpretation in UI. Next product checkpoint: define separate required/optional/negated/uncertain outputs and independent examples before implementing context-aware matching. No automatic requirement classification is implemented. Hosting remains separately prepared.

## Job-description comparison checkpoint - 2026-09-17

Completed stateless pasted-job comparison API and UI with 66 backend tests and browser/build/lint evidence. Next product checkpoint: evaluate required/optional/negated language and catalog gaps with explicit expected results before expanding matching intelligence. Saved comparisons, external AI and live job feeds remain unimplemented; hosting stays separate.

## Product features resumed - 2026-09-17

Completed temporary per-role skill review checklist with full browser verification. User requested product feature work; hosting remains prepared separately. Suggested next checkpoint: define and then build comparison against a pasted job description, reusing skill extraction with clear keyword limitations and synthetic evaluation. No live job integration or LLM provider selected.

## Disposable demo selected - 2026-09-17

Completed demo-specific frontend notice/build commands and local verification. Next: review Git checkpoint, configure chosen free hosting with real URLs and separate secret, then verify public workflow and reset behavior. No hosted deployment yet. Persistent hosting/operational backups remain deferred rather than required for this synthetic demo.

## Recovery checkpoint - 2026-09-17

Completed local offline same-path recovery drill with synthetic database and uploads; all 60 backend tests pass. Next milestone remains choosing disposable demo versus persistent hosting and validating the selected host. Automated operational backups, retention, hosted restore and path relocation are not implemented or verified by this drill.

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

## Migration checkpoint - 2026-09-16

Confirmed working: Alembic baseline, guarded existing-schema adoption, startup version enforcement and preserved local data. All 52 backend tests and Chrome workflow pass. Upload limits and migration baseline are now implemented. Next: frontend accessibility/portfolio presentation review; then deployment configuration, clean-machine setup and deployment verification. Future schema changes require reviewed migrations; no feature columns were added in this checkpoint.

## Upload safeguards update - 2026-09-16

Application byte/page limits and invalid-PDF errors implemented; 48 tests and browser flow pass. Next: database migration baseline without data loss. Deployment request-size limits and parser time/memory isolation remain outstanding.


## Scope estimate and next checkpoints - 2026-09-15

Planning estimate, not a measured completion metric: roughly 65–75% of a portfolio-ready local MVP is complete; roughly 45–55% of a broader deployed/hardened project. Completed foundation includes auth, React/API integration, resume text/skills, illustrative role overlap, evaluation, API/browser tests, documentation and private JWT configuration.

Assuming 1–2 focused hours per day: allow about 14–28 additional days for a polished local portfolio demo, or 28–56 for deployment with further hardening. Learning pace, hosting decisions and scope changes can extend this. Real job data and optional LLM/ML integration are additional scope; no provider/budget has been chosen.

Remaining sequence: upload byte/page limits and errors; schema migration approach; UI/accessibility/portfolio presentation; clean-machine setup and deployment configuration; deployment verification. Representative extraction evaluation and broader role requirements remain improvements. JWT config is now implemented with 44 backend tests and passing Chrome smoke. Next small checkpoint: upload resource limits. Current changes are uncommitted.


## Authentication maintenance update - 2026-09-15

Passlib metadata warning resolved using direct bcrypt with legacy compatibility tests and registration byte-limit validation. Forty backend tests and Chrome flow pass. Next: checkpoint review/commit and portfolio setup documentation.


## Browser checkpoint update - 2026-09-15

Automated real-Chrome happy flow and network-retry path verified with isolated data. Next: commit checkpoint after review, then resolve known bcrypt/Passlib compatibility warning in a focused maintenance task. Broader visual/accessibility and session-edge checks remain future verification.


## Role display update - 2026-09-14

Dashboard role overlaps implemented; build/lint and client checks passed. Next: manual browser/API comparison and end-to-end verification before extending the product. Earlier role-backend checkpoint is preserved.


## Role matching update - 2026-09-11

Backend role overlap implemented using four authored example profiles; 33 tests pass. Next: Postman verification and dashboard role display. Profiles are illustrative, without job-market or hiring claims; live job sources remain undecided.


## Evaluation update - 2026-09-11

Synthetic matcher evaluation completed with a targeted alias fix and documented context/catalog limitations. Next: define a small illustrative role catalog and transparent overlap-based matching, with no claim of live job data or hiring suitability. Browser skills/text verification still pending.


## Skills UI update - 2026-09-11

Skills dashboard is implemented; build/lint and client checks pass, browser verification pending. Backend skills passed the user's Postman test. Next: browser comparison, then representative catalog evaluation before role matching.


## Current checkpoint update - 2026-09-11

Local rule-based skill extraction backend is implemented and verified with synthetic tests. Next: show skills in the dashboard, then evaluate catalog coverage and false positives on representative non-sensitive examples before career matching or LLM integration. Prior phase descriptions below are historical where superseded.


## Phase 0 — Project Foundation

### Goals
- Create project repository.
- Set up Python backend.
- Establish Git/GitHub.

### Status
Mostly complete.

---

# Phase 1 — Backend Foundation

## Completed
- FastAPI application
- SQLite database
- SQLAlchemy
- user model
- registration
- login
- password hashing
- JWT
- protected route
- Postman testing

### Status
✅ Core foundation confirmed working.

---

# Phase 2 — Resume Ingestion

## Completed
- authenticated resume upload
- PDF validation
- local storage
- database metadata
- PDF text extraction
- extracted text persisted

### Status
✅ Confirmed working.

---

# Phase 3 — Frontend Foundation

## Tasks
1. Create React + Vite frontend.
2. Understand project structure.
3. Clean default starter UI.
4. Create page/component structure.
5. Add basic navigation/routing if needed.

### Status
🔵 Immediate priority.

---

# Phase 4 — Frontend Authentication

## Tasks
1. Register page.
2. Login page.
3. API service/client.
4. Configure CORS.
5. Connect registration.
6. Connect login.
7. Token handling.
8. Protected frontend/dashboard.
9. Logout.
10. `/users/me` integration.

---

# Phase 5 — Resume Dashboard

## Tasks
1. Resume upload UI.
2. PDF validation in frontend.
3. Multipart upload.
4. Loading state.
5. Success/error messages.
6. Display uploaded resume metadata.
7. Add resume retrieval endpoint if dashboard persistence requires it.

---

# Phase 6 — Resume Intelligence

## Tasks
1. Text cleaning.
2. Section detection.
3. Skill extraction.
4. Skills API.
5. Display skills in frontend.
6. Evaluate extraction quality.

---

# Phase 7 — Career / Job Matching

## Tasks
1. Define job/career data source.
2. Define matching criteria.
3. Implement initial matching method.
4. Produce score/explanation.
5. Display matches.
6. Evaluate quality.

---

# Phase 8 — AI Features

Possible features:
- resume feedback
- role recommendations
- skill-gap analysis
- learning roadmap
- tailored improvement suggestions

Before implementation:
- choose provider/model,
- define cost/privacy constraints,
- define structured output,
- define evaluation.

---

# Phase 9 — Testing / Quality

## Backend
- unit tests
- API tests
- ownership/security tests

## Frontend
- component tests
- form/error tests

## End-to-End
- registration
- login
- upload
- analysis
- recommendations

---

# Phase 10 — Portfolio Polish

- professional UI
- README
- architecture diagram
- screenshots
- setup instructions
- demo data
- project explanation
- interview talking points

---

# Phase 11 — Deployment

To decide later:
- frontend host
- backend host
- production database
- file storage
- environment secrets
- domain
- monitoring
- CI/CD
