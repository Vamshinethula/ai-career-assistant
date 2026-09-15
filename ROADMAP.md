# ROADMAP.md — AI Career Assistant

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
