# ROADMAP.md — AI Career Assistant

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
