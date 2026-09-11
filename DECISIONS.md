# DECISIONS.md — AI Career Assistant

This file records important project decisions so future development does not repeatedly revisit or silently reverse them.

---

## D-001 — Backend Framework

**Decision:** Use FastAPI.

**Reason:** Python-based, clear API structure, good fit for learning backend development and future AI/ML integration.

**Status:** Active.

---

## D-002 — Development Database

**Decision:** Use SQLite during early development.

**Reason:** Simple local setup, easy to inspect, sufficient for learning and MVP development.

**Tradeoff:** Not necessarily the final production database.

**Revisit when:** Deployment, concurrency, scale, or production requirements are introduced.

---

## D-003 — ORM

**Decision:** Use SQLAlchemy.

**Reason:** Learn ORM/database modeling and integrate cleanly with FastAPI.

**Status:** Active.

---

## D-004 — Authentication

**Decision:** Use JWT bearer authentication.

**Reason:** Appropriate for separated frontend/backend application and teaches modern API authentication concepts.

**Status:** Active.

---

## D-005 — Resume Format

**Decision:** Accept PDF only for the current version.

**Reason:** Simplifies parsing and validation while building the first working resume pipeline.

**Evidence:** DOCX upload was intentionally tested and correctly rejected.

**Revisit when:** There is a clear requirement for DOCX or other formats.

---

## D-006 — Resume File Storage

**Decision:** Store uploaded resume files locally in `uploads/` during development.

**Reason:** Simple local MVP behavior.

**Tradeoff:** Production will likely require more robust storage.

**Revisit when:** Deployment/storage requirements are defined.

---

## D-007 — Service Layer for Parsing

**Decision:** Keep PDF parsing logic separate from the API route, under a service layer such as `app/services/resume_parser.py`.

**Reason:** Routers should focus on HTTP orchestration; reusable parsing belongs in business/service logic.

**Status:** Behavior confirmed; exact repository implementation must be inspected.

---

## D-008 — API Testing Tool

**Decision:** Use Postman for API testing.

**Reason:** User prefers Postman and benefits from seeing method, URL, authorization, body, and status explicitly.

**Status:** Active.

---

## D-009 — Frontend Technology

**Decision:** Use React + Vite + JavaScript.

**Reason:** Modern, lightweight frontend development and suitable for learning full-stack integration.

**Status:** Latest frontend decision.

---

## D-010 — Development Order Change

**Earlier plan:** Implement resume skill extraction immediately after resume text persistence.

**New decision:** Pause deeper backend work and start frontend.

**Reason:** User explicitly requested frontend development after reaching a working backend resume-ingestion checkpoint.

**Status:** Latest decision; frontend takes priority.

---

## D-011 — Teaching Is a Core Requirement

**Decision:** Every meaningful development task must be taught, not only implemented.

**Reason:** User’s project goal is learning Python full-stack + AI/ML development and professional tools such as Git/GitHub.

**Status:** Permanent project rule.

---

## D-012 — Repository Beats Documentation

**Decision:** The real repository is the source of truth for implementation status.

**Reason:** Previous assistant recommendations may not exactly equal what was actually implemented.

**Status:** Permanent engineering rule.

---

# Template for Future Decisions

## D-XXX — Title

**Date:**

**Decision:**

**Context:**

**Options considered:**
1.
2.
3.

**Chosen option:**

**Why:**

**Tradeoffs:**

**Revisit when:**


## D-013 - Local registration API connection

**Date:** 2026-09-10
**Context:** Registration UI needs to call the existing FastAPI route.
**Options considered:** native fetch with explicit CORS; Vite proxy; added HTTP client dependency.
**Chosen option:** native fetch in a separate services/api.js, fixed local backend address, explicit localhost/127.0.0.1 port 5173 CORS origins for JSON POST.
**Why:** No new dependencies; teaches requests and cross-origin browser behavior directly.
**Tradeoffs:** Local-only URL and CORS configuration; requires both development servers. 15-second timeout bounds waiting; after a lost response an account might already exist.
**Revisit when:** adding authenticated API operations or deployment configuration.


## D-014 - In-memory login checkpoint

**Date:** 2026-09-10
**Context:** Login UI needs to retain the existing API's bearer token and reflect session state.
**Options considered:** React state, browser storage, cookie-based backend redesign.
**Chosen option:** App-level React state and callback prop from LoginForm; local logout clears state.
**Why:** Small incremental lesson using the existing API and no new dependencies.
**Tradeoffs:** Refresh loses login; logout does not revoke issued JWTs; token expiration/protected-request handling is next. No persistent or production session claim.
**Revisit when:** implementing /users/me, session persistence or production deployment.


## D-015 - Fetch authenticated profile on dashboard mount

**Date:** 2026-09-10
**Context:** The frontend must display a backend-verified profile using the existing JWT.
**Options considered:** load in the login handler; dashboard effect; query/state library.
**Chosen option:** Dashboard useEffect with cancellation, existing API helper extended for GET, App callback on 401.
**Why:** Keeps login and profile responsibilities separate and teaches effects without dependencies.
**Tradeoffs:** Expiration detected at request time; no polling/session persistence. Retry handles temporary server/network failures.
**CORS:** Extends D-013 with GET and Authorization while retaining the same local origins.
**Revisit when:** multiple protected resources need shared loading/cache/session handling.

## D-016 - Commit resume only after parsing

Date: 2026-09-11
Context: metadata committed before parsing survived a later rollback.
Options: one deferred commit; compensating database deletion; staged-upload model.
Chosen: parse first, add/flush, validate response, then one commit. Use a response snapshot so post-commit refresh failures cannot cause deletion of a successfully saved file.
Why: smallest change preserving existing endpoint/schema behavior.
Tradeoffs: filesystem and database are not crash-atomic; cleanup can fail if deletion is denied. PDF bytes parsing avoids Windows handle locks but adds memory proportional to file size. Parser failures retain existing 500 response.
Revisit: upload size limits, background parsing, production storage, crash recovery or richer invalid-PDF errors.

## D-017 - Owner-filtered resume metadata list

Date: 2026-09-11
Context: uploaded resumes need to be visible on the dashboard.
Options: metadata list, full extracted text in every list row, paginated list.
Chosen: GET /resumes using the existing ResumeResponse, filtered by the authenticated user's ID and sorted by uploaded_at/id descending. React refetches after successful uploads.
Why: small testable checkpoint without schema changes; reuse existing authentication and API client.
Tradeoffs: no pagination yet; list shows filenames only; list-key remount resets its state on upload. Text viewing is a separate checkpoint.
Revisit: large upload histories, pagination, richer list controls or text details.

## D-018 - Load extracted text on demand

Date: 2026-09-11
Context: users need to inspect saved parser output.
Options: include all text in list; owner-protected detail request.
Chosen: GET /resumes/{resume_id} and one expanded text view; detail response inherits metadata and adds nullable text. Foreign/missing rows return identical 404 responses.
Why: keeps list small and uses existing stored text/authentication without schema changes.
Tradeoffs: an extra request on each opening; no OCR, editing or text cache.
Revisit: larger documents, caching, OCR or editing requirements.

## D-019 - Rule-based software skill baseline

Date: 2026-09-11
Context: first skill-extraction checkpoint needs defined input, output and evaluation.
Options: explicit catalog rules, trained model, embeddings, external LLM.
Chosen: 32-skill software-development starter catalog with canonical aliases; local deterministic matching of stored text; read-only protected skills endpoint. Response labels method and text availability. No inference of proficiency, persistence or external data transfer.
Why: explainable, testable baseline with no new dependency or API cost; existing project examples and stack guide initial scope without hardcoding any personal resume.
Tradeoffs: limited software catalog, ambiguous terms/negation unhandled, no inferred skills or spelling correction, recomputed on each request. Synthetic fixtures validate mechanics rather than general resume accuracy.
Evaluation: exact expected skill sets for positive mentions, aliases/duplicates, boundary negatives, punctuation and empty/unknown text; API ownership/auth/status tests.
Revisit: representative evaluation reveals catalog/precision gaps, broader career domains are needed, or user authorizes a model/provider after cost/privacy discussion.

## D-020 - Separate supported evaluation cases from limitation probes

Date: 2026-09-11
Context: mechanics tests alone did not show alias overlap and broader matching limits.
Options: ad hoc resume checks; synthetic labeled development cases; external benchmark.
Chosen: 15 synthetic cases, reported by supported scope and known limitation probes; retain visible errors and label development-set results honestly. Prefer longest nonoverlapping alias spans for overlapping names.
Why: reproducible and local, with no sensitive data or new dependencies; fixes a demonstrated false positive.
Tradeoffs: small, manually authored, tuned-on examples do not estimate real-world accuracy. Context ambiguity, negation/proficiency and catalog gaps remain.
Revisit: independent labeled corpus or broader role-domain requirements.
