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

## D-021 - Illustrative role profiles and equal-weight overlap

Date: 2026-09-11
Context: need a first explainable matching checkpoint using extracted skills.
Options: authored example catalog, external job feed, embeddings/LLM ranking.
Chosen: four explicitly illustrative five-skill software profiles; equal-weight set overlap percentage, positive-overlap results only, stable role-ID ties. Compute on demand through an owner-protected GET endpoint, exposing matched and not-detected terms.
Why: no external service, cost, migration or hidden scoring; straightforward to test and teach.
Tradeoffs: profiles are simplified learning fixtures, not authoritative requirements; all terms weighted equally, no experience/seniority or inferred skills. Extractor false positives/negation affect scores. Low overlap may still produce a result; percentage is not confidence or hiring probability.
Evaluation: exact synthetic partial/full/zero score checks, duplicate invariance, order/tie checks, canonical catalog integrity and API ownership/empty-state checks.
Revisit: actual role data source, independently evaluated requirements, user domain needs or agreed model/provider.

## D-022 - Direct bcrypt with explicit legacy compatibility

Date: 2026-09-15
Context: Passlib 1.7.4 reads missing bcrypt metadata and emits a trapped warning.
Options: downgrade bcrypt, patch library metadata, replace wrapper with direct installed bcrypt, migrate password algorithm.
Chosen: direct bcrypt 4.3.0 hashpw/checkpw, random salts and cost 12; remove unused Passlib requirement. New registrations reject empty/null/over-72-byte passwords with 422; login preserves historical UTF-8 truncation and 4096-character ceiling. Invalid hashes fail closed.
Why: removes incompatible wrapper without new dependencies or database migration; compatibility proven with synthetic hashes generated before the change.
Tradeoffs: legacy long-password equivalence remains for compatibility; bcrypt still has a 72-byte input limit. Local venv may retain unused Passlib. Modern algorithm migration remains a separate design task.
Revisit: production auth review, long-password support, hash upgrades or new algorithm requirements.

## D-023 - Private JWT configuration with dotenv fallback

Date: 2026-09-15
Context: signing key was hardcoded in source and must be retired without changing account data.
Options: environment only; standard dotenv development fallback; custom parser.
Chosen: python-dotenv 1.2.3 reads exact backend/.env; process JWT_SECRET_KEY takes precedence. Require at least 32 non-padding bytes; setup generates 48 random bytes encoded URL-safe. No insecure fallback. HS256 and 30-minute lifetime stay fixed.
Why: standard parsing, simple local setup and deploy-time environment support. Generator refuses to overwrite existing files and never prints keys.
Tradeoffs: one small dependency; key remains plaintext in an ignored local file and needs deployment secret storage later. Key rotation logs out issued sessions; account/password/resume data unchanged. Old key remains in historical commits but is retired.
Revisit: deployment secret management, multiple signing keys/rotation windows or configuration growth.

## D-024 - Resume input limits and explicit PDF errors

Date: 2026-09-16
Context: unbounded stored PDF size/pages and generic 500 for corrupt input.
Options: application limits now; deployment middleware/proxy limits; isolated parsing workers.
Chosen: 5 MiB actual spooled-file limit before saving; 10 pages before extraction; reject password-protected/invalid PDFs with 400, limit violations with 413. Browser size check and clear feedback. Valid empty-text PDFs remain supported.
Why: small, testable safeguards appropriate for resume input, no dependencies/schema changes.
Tradeoffs: limits occur after multipart parsing/spooling; ingress limits and compressed-content/time/memory isolation remain deployment work. Limits may need adjustment for longer CVs.
Revisit: user file needs, deployment resource limits and parser isolation.

## D-025 - Alembic baseline and explicit upgrades

Date: 2026-09-16
Context: create_all cannot evolve existing tables; local accounts/resumes must survive schema setup.
Options: reset SQLite, continue manual SQL, or introduce versioned Alembic migrations.
Chosen: Alembic 1.20.0 with a frozen initial revision. Compare unversioned schemas against that revision before stamping; upgrade fresh/versioned databases normally. Application lifespan requires current revision. SQLite backup before local adoption; baseline downgrade refuses deletion.
Why: supports future schema evolution with a reviewable history while preserving current data. Schema comparison uses the frozen baseline, not future models.
Tradeoffs: an explicit setup command and dependencies; autogeneration needs human review and does not detect every possible schema difference. Startup checks revision, not full schema drift. This is verified for SQLite; other production databases need separate validation. No automated backup service is introduced.
Revisit: first real column change, deployment database choice, multi-instance deployment or backup/restore requirements.

## D-026 - Explicit deployment addresses with local defaults

Date: 2026-09-16
Context: API and CORS addresses were hardcoded.
Options: runtime frontend configuration, Vite build-time variable, or reverse proxy only.
Chosen: VITE_API_BASE_URL with local fallback; comma-separated CORS_ORIGINS using existing dotenv/environment precedence. Exact HTTP(S) origins only, no wildcards or URL paths.
Why: simple configuration with existing dependencies and unchanged local setup.
Tradeoffs: frontend address changes require rebuild; backend requires restart. CORS does not authenticate clients. Hosting and HTTPS setup remain separate work.
Revisit: multiple deployment environments needing identical frontend artifacts or same-origin proxy hosting.

## D-027 - Shared absolute storage root

Date: 2026-09-16
Context: relative paths could select different databases by working directory and could not target a host volume.
Options: separate database/upload variables; database URL plus object storage; one SQLite data directory.
Chosen: CAREER_DATA_DIR, existing absolute directory, environment over dotenv, default anchored backend/. App and Alembic share the engine. No automatic data move or backend change.
Why: smallest local-compatible step for a single-instance deployment; both data types remain together.
Tradeoffs: SQLite only, directory must exist, existing stored paths need review before relocation, actual volume durability unverified. Default behavior intentionally changes from cwd-relative to backend-anchored.
Revisit: hosting selection, multiple instances, object storage or production database migration.

## D-028 - GitHub Actions regression checks

Date: 2026-09-16
Context: clean Windows setup passed but repeatable remote and Linux verification are missing.
Options: manual-only checks, Windows-only CI, or Windows/Linux backend matrix plus frontend build job.
Chosen: backend matrix and Ubuntu frontend, Python 3.12/Node 24, read-only permissions, no deployment or secrets. Browser smoke remains local for now.
Why: reuse existing commands and expose host-OS compatibility issues without choosing hosting.
Tradeoffs: additional runner time, first remote run unverified, major action tags may update. No branch-protection setting changed.
Revisit: initial runner failures, CI duration or adding browser checks.
