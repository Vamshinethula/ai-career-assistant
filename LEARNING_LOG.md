# LEARNING_LOG.md — AI Career Assistant

## Title search before pagination - 2026-09-18

Filtering only the ten rows in the browser would miss matches on other pages. The backend filters all rows belonging to this resume/user, then sorts and pages the matches. SQLAlchemy binds the search value and escapes LIKE wildcard characters; frontend URLSearchParams encodes the query safely.

Run the existing backend/frontend, open saved comparisons, enter part of a title, then Search comparisons. Success shows matching titles; an absent phrase shows a no-match message. Clear search restores history. An offline request displays retry feedback; API search values longer than 120 characters return 422. You should be able to explain why filtering precedes pagination and why literal percent/underscore characters require escaping.

## 2026-09-18 - Pagination

Pagination loads a small portion of a list. In backend/app/routers/resumes.py, offset skips rows and limit caps rows after ownership filtering and newest-first sorting. For example, offset=10&limit=11 skips ten records and requests eleven. SavedComparisons.jsx shows ten and uses the extra record to enable Older, avoiding a separate count query.

Run the normal backend/frontend, save eleven synthetic snapshots and navigate Older/Newer. Success shows ten entries then one; Older is disabled on the last page. Invalid API limits return 422, while network failure shows readable feedback. Refresh starts again at the newest page. Concurrent saves/deletes can shift offsets; this is not a frozen history view. You should now be able to explain bounded queries, offsets, limits and why pagination needs stable ordering.

## 2026-09-18 ? Deleting one resource safely

A snapshot is a separate database row linked to a resume. Deleting that row does not require deleting its parent resume or PDF. In backend/app/routers/resumes.py, the existing owner lookup runs before db.delete and commit. For example, DELETE /resumes/1/comparisons/2 returns 204 with no JSON body on success; another user's request returns 404.

The frontend API client accepts an empty 204 response. SavedComparisons.jsx asks for confirmation and refreshes history after success. Run the app, open a saved snapshot, cancel first, then confirm deletion using synthetic data. The row should disappear while the resume stays available. An offline request should show an error; refresh if the server may have completed the request.

You should now be able to explain resource ownership, parent/child deletion, HTTP 204, and why an uncertain network response does not prove a database operation failed.

## 2026-09-18 - Persistence and snapshots

React state disappears when a panel closes; a saved database row survives login sessions while storage exists. Explicit saving now keeps private job text, server results and labels. Reopening reads the saved automatic result. Reviewed score uses saved keywords and choices.

Migration 0002 adds a table without replacing users or resumes. SQLite was backed up and existing rows compared unchanged afterward. SQLite drops datetime timezone metadata, so the response schema restores UTC meaning. Try saving a titled comparison, logging out/in and reopening it. Success is preserved results/labels; invalid input returns 422 and other users get 404. Refresh history before retrying an uncertain save response to avoid duplicates. You should now distinguish temporary state, snapshot persistence and schema migration.

## 2026-09-18 - Choosing a denominator explicitly

A score depends on what it divides by. Original overlap counts all detected job terms. The reviewed score counts only terms you personally mark Required. If you confirm Python and Docker and the resume mentions only Python, the reviewed overlap is 1/2 = 50%. Optional, not-required, uncertain and unreviewed terms are excluded.

No confirmed requirements means null (no score), not zero. Confirming one matching term can produce 100% while other terms remain unreviewed, so the UI shows coverage counts and a subset warning. UI and export share one pure function to avoid inconsistent calculations. Tests cover these distinctions. You should now explain why percentages need their denominator and why user review does not prove proficiency.

## 2026-09-18 - A verified Git checkpoint

A commit records a reviewable snapshot; pushing sends it to GitHub and triggers CI. Feature commit e933920 passed fresh backend checks on Windows/Linux and frontend checks on Ubuntu. CI confirms those commands for that exact commit, not hosted deployment or every browser behavior. Documentation records the run link so verification can be traced. You should now distinguish local tests, remote CI and deployment.

## 2026-09-18 - Browser downloads and explicit serialization

A serializer converts current data into a file format. comparisonExport.js selects fields explicitly rather than exporting every object property, keeping authentication tokens and resume text out. JSON preserves automatic labels and user choices separately; null remains unknown rather than becoming zero.

The browser wraps the JSON in a Blob, creates a temporary object URL and activates a download link. The URL is released afterward. Downloaded files are separate from temporary React state and remain after logout. Evidence may contain private source text, so review before sharing.

Try Download comparison summary after choosing a label; open the JSON and compare automatic_category with user_choice. npm test runs three pure serializer checks; Chrome checks a real download and simulated failure/retry. You should now explain serialization, browser-created files and why download initiation does not prove a user saved a file.

## 2026-09-18 - User review without overwriting model output

A user interpretation and an automatic label are different facts. JobComparison stores choices in a separate object keyed by skill; it never edits the API result. A controlled select displays the chosen value. Reset removes that choice, and a fresh comparison starts with an empty object.

Try a description with SQL is required. SQL is optional. The automatic label is uncertain. Choose Required in Your label for SQL: Your choice appears, while the original label and score remain. Reset returns to automatic use. This is temporary React state, not a saved correction or model training. You should now explain provenance and why editing input should invalidate derived state.

## 2026-09-18 - Connecting a service through an API contract

A tested function becomes a product feature when the route response schema, API client and UI agree. The comparison now carries requirements records: a skill, a tentative label and source fragments. Pydantic constrains allowed labels; the frontend checks the response before displaying it. JSX renders snippets as text, so pasted HTML-like content does not execute.

Try Python is required. Docker is optional. Java is not required. SQL is required. SQL is optional. The labels include uncertain SQL with both source statements, while the keyword score still counts all four terms. Open Source wording for SQL with Space. Success is visible evidence; malformed API results show a readable error. You should now explain additive response fields, coordinated frontend/backend updates, and why evidence display is separate from changing a score.

## 2026-09-18 - Abstention and evidence in classification

A classifier need not guess. Our new service only labels supported explicit phrases: Python is not optional means required, while Java is not required means not_required. Mixed wording or contradictory statements becomes uncertain, with both original fragments retained for review.

The service is a pure function: text in, structured records out, with no database or external AI call. Reusing the skill catalog preserves canonical names. Splitting text into fragments scopes each rule, though unsupported cross-line headings remain uncertain.

Run python -m evaluation.evaluate_requirements from backend. Expect 12/12 development and 10/10 review policy matches, alongside 16 classified and 16 uncertain records. Those passes include intentional abstentions, so they are not 100% semantic accuracy. You should now explain why evidence and uncertainty are useful outputs and why a tested service can precede API/UI integration.

## 2026-09-18 - Correct output versus useful interpretation

A keyword matcher can work exactly as designed and still be unsuitable for identifying requirements. Our 16 keyword checks pass, yet only 5 of 12 contextual examples match manually labelled required-skill sets. Precision asks how many reported terms are truly required; recall asks how many labelled required terms were found. These synthetic metrics are not hiring accuracy.

Example: Python required; Docker optional counts two mentions. A Python-only resume scores 50% keyword overlap, even though it mentions the sole required skill. Simply deleting terms near not breaks Python is not optional. We kept the score meaning and clarified it on screen instead of claiming semantic understanding.

Run python -m evaluation.evaluate_jobs from backend. Success is 16 contract passes plus a visible report of known interpretation gaps, not zero limitations. You should now explain regression tests versus quality evaluation and why a passing test suite does not validate every interpretation of a score.

## 2026-09-17 - Comparing sets through a protected POST endpoint

A set removes duplicates. For job skills Python, Docker and Kubernetes, a resume containing Python and Docker shares two of three terms: 66.7%. The service uses set intersection for shared terms and subtraction for job terms not detected in the resume. No detected job terms means an unknown score (null), not zero.

The route validates the JSON body and checks ownership before calling the service; the schema defines the response. React submits through the existing API client and clears old results when text changes so the displayed percentage cannot silently describe an earlier input. An AbortController cancels requests when the panel closes.

Try Compare job description with Python Docker Kubernetes, then replace it with Team player. Expect an explained score first and an insufficient-information message second. Blank input gets validation feedback; another user's resume returns 404. You should now explain set operations, POST bodies, null versus zero and why matching keywords is not measuring proficiency. See backend/evaluation/JOB_COMPARISON.md for limits.

## 2026-09-17 - Component state and honest skill feedback

SkillReview receives a role match through props and keeps reviewed terms in useState. Toggling a checkbox makes a new array, which tells React to render the updated count. Each role owns its state. Closing role overlaps removes the component, so reopening creates a fresh empty checklist; this is not database persistence.

Example: a resume containing Python FastAPI SQL Git Docker has two undetected terms for the Java example role. Reviewing one produces 1 of 2 terms reviewed while the 60% overlap stays unchanged. Review does not prove proficiency. Open View role overlaps, expand Review next steps, and press Space on a focused checkbox to try it. Success is an updated count; missing text/results or network errors retain the existing readable error/retry paths. You should now explain props versus local state and why a checklist is separate from evidence of skill.

## 2026-09-17 - Build modes and temporary hosting storage

A Vite build mode selects which frontend we produce. In App.jsx, import.meta.env.MODE === 'demo' includes the visitor notice. npm run build:demo builds that version; npm run build creates the normal one. Both write dist, so the hosting command matters. Browser tests verify the visible difference while exercising the same API features.

A notice cannot delete data or prevent personal uploads. The host's temporary filesystem controls resets; our local SQLite files remain saved on normal restarts. You should now be able to distinguish frontend configuration from backend storage behavior. Run the demo browser command in HOSTING_PLAN.md; success is PASS, while missing notice or broken API flow fails the check.

## 2026-09-17 - Hosting code versus keeping data

A static host serves built React files; a Python web service runs FastAPI. An ephemeral filesystem can be replaced when the service restarts, losing SQLite and PDFs even though code redeploys successfully. Persistent storage preserves files under its mount path, but still needs backups. HOSTING_PLAN.md maps both options to our project. Migrations must run against the runtime storage before the app starts. You should now be able to explain why deploying code and preserving user data are separate checks. The proposed host has not been tested with this app.

## 2026-09-17 - A backup needs a recovery test

Our app keeps records/text in SQLite and PDF bytes in uploads/. Saving only the database misses half of that relationship. In backend/tests/test_backup_recovery.py, restoring only SQLite still allows login and text viewing, but opening the original PDF fails. A complete snapshot restores both and checks the file bytes as well as API responses.

Stop writes while capturing both parts so they describe the same moment. Restore at the original absolute path because records currently save file paths. Run the two-test command in backend/tests/BACKUP_RECOVERY.md; success is OK, including the deliberately detected missing-PDF case. You should now be able to explain why a backup file existing, or a dashboard loading, does not prove recovery works. Hosted and relocated recovery need their own evidence.

## 2026-09-16 - Keyboard focus and skip links

Keyboard users press Tab to move between controls. A skip link jumps past repeated introductory content. In frontend/src/App.jsx, its href points to workspace; tabIndex={-1} allows that container to receive focus without adding it to the normal Tab sequence. App.css reveals the link when focused and gives controls a visible outline.

Try it at http://127.0.0.1:5173/ after starting both servers: reload, press Tab, then Enter, then Tab. Success: the skip link appears, focus jumps to the workspace, then the name field. Failure would be an invisible link or focus staying in the introduction. The real Chrome test verifies this sequence and existing network-error recovery. You should now be able to explain focus versus clicking and why keyboard users need a visible location indicator. Screen-reader announcements and a full accessibility audit still need separate review.

## 2026-09-16 - Database migrations

A model describes the tables the code expects. A migration records how to build or change those tables. SQLAlchemy create_all creates missing tables but does not evolve existing ones. Alembic stores the applied revision in alembic_version, like a checkpoint for database structure.

The frozen initial revision lives in backend/migrations/versions/. Our helper compares existing unversioned tables with that baseline before recording the version; a fresh database runs the revision instead. This preserves existing accounts and resumes. FastAPI now refuses startup when the revision is behind, with the command to run.

From backend, run `.venv/Scripts/python.exe scripts/migrate_database.py`, then `.venv/Scripts/python.exe -m alembic current`. Success shows 0001_initial (head). A differing old schema raises an error instead of being silently accepted. Four migration tests cover fresh/repeated runs, existing data, schema mismatch and startup checks; all 52 backend tests pass. The local data was also compared against a backup.

You should now be able to explain the difference between a model, a migration, an upgrade and a stamp: a stamp records a version without creating its tables. Always review generated future migrations and back up valuable data first; version tracking alone does not prove that nobody manually changed a table.

## 2026-09-16 - Validate uploads at multiple layers

The browser checks file.size for fast feedback, but any client can bypass it. The upload route measures the actual spooled file before saving, rather than trusting a size header. config.py defines a 5 MiB (5,242,880-byte) maximum and 10-page maximum. The parser checks page count and password protection before extracting text. Services raise typed errors; the route converts them to HTTP responses and removes rejected artifacts.

Example: 10 pages succeeds; 11 pages returns 413. A corrupt or encrypted PDF returns 400. File-size and page-limit tests verify both exact-boundary acceptance and rejection with no leftover record/file. Unexpected server/storage errors remain 500. A blank but valid PDF can still have no extracted text; existing UI handles that case.

Run from backend: .venv/Scripts/python.exe -m unittest discover -s tests -q -> 48 tests OK; node tests/browser_smoke.mjs -> PASS including oversized/corrupt/11-page errors and successful upload recovery. In the normal dashboard, a file larger than 5 MiB should immediately show a size message. Postman can independently verify 413; a readable PDF within both limits should return 201. Existing servers can be reused; usual startup commands are in README.

These checks bound storage and parsing inputs after FastAPI receives multipart data. They do not prevent initial network/spool usage or guarantee bounded parsing time for compressed/complex PDFs; deployment ingress limits and parser isolation are separate tasks. You should now explain frontend feedback versus backend enforcement, 400/413/500 distinctions and boundary testing.


## 2026-09-15 - Configuration versus code

JWT signing keys belong outside source code. app/config.py reads JWT_SECRET_KEY from the environment or an explicitly located backend/.env using python-dotenv; environment values win. Startup rejects missing/short keys rather than using a shared fallback. scripts/init_local_env.py uses Python secrets to create a private random key and exclusive file creation prevents overwriting it. .env.example contains no secret; .gitignore excludes the real file.

Example: the same code can run locally with .env and on a host with an injected environment variable. A changed key cannot verify tokens signed with the old key, so users log in again. Password hashes and resume rows do not depend on the JWT key and remain unchanged. The old hardcoded key remains in Git history but is retired; history was not rewritten.

From backend: .venv/Scripts/python.exe scripts/init_local_env.py, then .venv/Scripts/python.exe -m uvicorn app.main:app --reload. Setup has already generated the local file this session. Never paste its contents into chat or Git. Tests: .venv/Scripts/python.exe -m unittest discover -s tests -q -> 44 passing; node tests/browser_smoke.mjs -> PASS. Tests use random test-only keys. Invalid config should stop startup with a message naming JWT_SECRET_KEY without revealing a value. Source: https://github.com/theskumar/python-dotenv . You should now explain environment precedence, fail-fast configuration, key rotation and the difference between token invalidation and password storage.


## 2026-09-15 - Write a runnable project README

A README is the entry point for someone who has not seen the development conversation. Ours now explains what works, where code belongs, how to start both servers, what success looks like and what is still limited. Commands specify their starting folder because relative paths resolve from the terminal directory. Example: from root use node backend/tests/browser_smoke.mjs; from backend use node tests/browser_smoke.mjs.

The setup uses the venv's Python directly, so activation is optional. npm ci uses the committed lockfile for frontend dependency installation. The database URL is relative to backend; starting there prevents creating a database in an unintended folder. The README distinguishes existing verification from untested clean-machine setup.

Verification this checkpoint: all relative README links resolve, backend requirement pins equal installed versions, pip check passes. No source code changed. You should now explain setup documentation, working directories, lockfiles, and why a tested local environment is not proof of clean-machine reproducibility.


## 2026-09-15 - Preserve password compatibility during maintenance

Passlib wrapped bcrypt but expected removed bcrypt.__about__ metadata. security.py now calls the already-installed bcrypt library directly. hashpw combines password bytes with a random salt; checkpw verifies without storing/recovering plaintext. gensalt(rounds=12) preserves the prior work factor. Stored bcrypt hashes contain the salt and cost, so they need no database migration.

Bcrypt processes at most 72 bytes. Bytes differ from characters: 36 copies of an accented e use 72 UTF-8 bytes. New registration rejects empty, null-containing or longer passwords at both backend validation and the form. Login preserves the prior first-72-byte behavior for historical long passwords; new hashing does not silently truncate. This is compatibility, not a new long-password security design. Invalid stored hashes fail verification rather than exposing an internal exception.

Before editing, generated four synthetic hashes with the old Passlib code and saved them in tests/fixtures/legacy_bcrypt.json. These are public test values, never real account data. Tests verify those hashes through the new code, including a multibyte boundary. The old library is no longer a project requirement; it may remain unused in the local venv.

Run from backend: .venv/Scripts/python.exe -m unittest discover -s tests -q -> 40 tests OK with no bcrypt metadata warning. From backend: node tests/browser_smoke.mjs; from root: node backend/tests/browser_smoke.mjs -> PASS including too-long-password feedback, valid registration and login. Restart the normal backend if reload is not active; existing credentials should still work. Chrome test uses isolated data.

Sources: https://github.com/pyca/bcrypt and https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html . You should now explain salts, cost, byte limits, backward compatibility and regression fixtures. Next: review/commit checkpoint, then setup documentation.


## 2026-09-15 - Browser tests versus API tests

API tests call FastAPI directly; they cannot prove React event handlers or browser-origin rules work. The new browser_smoke.mjs drives installed Chrome through its debugging protocol, types into actual forms and checks rendered results. browser_server.py loads the real FastAPI app after configuring an in-memory database. A temporary browser profile redirects only test API traffic to port 8001, so port 8000 and personal data remain untouched.

Example: browser selects a synthetic PDF -> React builds FormData -> real CORS/auth/upload/parser/database code runs -> success message and refreshed list appear -> text, skills and role counts are inspected. Blocking the role request produces a connection error; unblocking and clicking Try again restores results. Logout clears the displayed results. At 390px viewport the document fits without horizontal overflow.

Run from root: node backend/tests/browser_smoke.mjs (or use the explicit Node path in backend/tests/BROWSER_TEST.md). Success: PASS summary and exit 0. Failure: nonzero exit with the failed/timed-out step. Test setup requires frontend dependencies, backend venv, Chrome, free ports 8001/9223, and this project's frontend on 5173 or a free 5173. It cleans up only its own processes and temporary directory. No new dependencies or real account uploads.

Confirmed this run: full tested browser flow and recovery. Not covered: comprehensive visual/accessibility assessment, production networking, expiry UI and rapid-selection races. You should now explain why browser tests complement API tests and why test-data isolation matters.


## 2026-09-14 - Integration tests across the workflow

Unit tests check a small function, such as skill overlap. The new test_resume_flow.py checks connected behavior: create account -> obtain token -> upload PDF -> read list/text/skills/roles. It uses actual routers, password hashing, JWT authentication, PDF parser and database queries. This can catch disagreements between components that individual function tests miss.

The test constructs a synthetic PDF containing Python FastAPI SQL Git Docker and uploads it as multipart form data. It verifies 201, persisted file bytes and text, five detected skills and 100% overlap with the illustrative Python backend profile. A second registered account receives an empty list and 404 for the first account's details/skills/matches. Wrong password and missing auth return 401; corrupt upload returns 500 and leaves no file or record.

Run from backend: .venv/Scripts/python.exe -m unittest discover -s tests -v. Expected: 35 tests OK. The known bcrypt metadata warning may appear, but is not a failed assertion. Tests use temporary storage and an in-memory database; they do not need the development servers or access personal resumes. They call FastAPI through ASGI without a network socket; React, CORS and main-app startup are not exercised.

Manual next check: with both servers running, log in at http://127.0.0.1:5173/, upload a disposable PDF, then open text, skills and role overlaps. Confirm outputs correspond to that file and logout returns to login. Start servers only if needed: backend .venv/Scripts/python.exe -m uvicorn app.main:app --reload; frontend npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort. You should now explain unit versus integration testing and why API-flow success does not prove browser behavior.


## 2026-09-14 - Explain a score in the interface

ResumeList owns matchesId; its View role overlaps button mounts ResumeMatches. The effect calls services/api.js with a bearer token and renders the structured result. Hiding/switching aborts the old request and ignores stale responses. The API client validates the resume ID, method/catalog labels, skill lists and score range before displaying data.

Each profile displays matched count divided by total profile terms as well as the percentage. Example: Python and SQL matched out of five terms -> 40% overlap. Not detected terms are absent from extraction, not necessarily skills the user lacks. Empty text, no detected catalog skills and no profile overlap produce different messages. These are authored examples, not live vacancies or qualification judgments.

With servers running, open http://127.0.0.1:5173/, log in, and click View role overlaps. Compare results with Postman for that resume's numeric ID. Check counts explain percentages; Hide role overlaps should close the panel. To test retry, block the /matches request in browser developer tools, open the panel, then unblock and click Try again. Check switching resumes during slow requests and logout while loading. Actual browser checks remain pending.

Start servers only if needed: from backend, .venv/Scripts/python.exe -m uvicorn app.main:app --reload; from frontend, npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort. Build/lint and isolated client tests passed, including populated/empty/error/malformed/offline/cancellation cases. You should now explain conditional rendering, score explanations and why numerical overlap is not a confidence score.


## 2026-09-11 - Explainable role overlap

services/role_matcher.py contains four authored example profiles, not live vacancies or authoritative hiring requirements. Input is the canonical skills already extracted from a resume. Sets remove duplicate mentions. Intersection gives matched skills; profile minus detected skills gives not-detected skills. Score = matched count / profile skill count * 100. Example: Python and SQL overlap two of Python backend's five profile skills, yielding 40%; FastAPI, Git and Docker are not detected. Not detected is not proof of missing ability.

routers/resumes.py adds GET /resumes/{resume_id}/matches. It checks the owner, extracts terms from stored text and calls the pure scoring function. schemas.py validates a structured response with catalog=illustrative_v1, method=skill_overlap, text_available, extracted_skills and matches. Roles with zero overlap are omitted; ties use stable role IDs. Repeated words never increase a score; unknown skills do not lower it. Scores reflect these manually chosen profiles, inherit extraction errors and do not estimate hiring chances or proficiency.

Run tests from backend: .venv/Scripts/python.exe -m unittest discover -s tests -v. Expected: 33 tests OK. Start backend if needed: .venv/Scripts/python.exe -m uvicorn app.main:app --reload. In Postman first GET http://127.0.0.1:8000/resumes using your bearer token. Copy a resume's numeric id, not user_id. If it is 3, send GET http://127.0.0.1:8000/resumes/3/matches with the same token and no body; replace 3 with your actual ID. Expected 200 with matches; empty text or zero overlap yields an empty matches array. Missing token -> 401; another user's or nonexistent ID -> 404.

These endpoint behaviors are verified in isolated ASGI tests; user Postman verification is pending. The dashboard does not display roles yet. You should now explain sets, intersection/difference, score denominators, deterministic tie ordering and the distinction between overlap and qualification.


## 2026-09-11 - Commit versus push

A commit saves a named snapshot in local Git history. A push sends commits to the configured GitHub remote. We reviewed changed files and ignore rules, ran 24 backend tests plus frontend build/lint, then prepared a checkpoint for origin/main. Runtime databases, uploaded resumes, tokens and environments must stay out of the snapshot. Use git status to inspect local changes and git log -1 --oneline to identify the latest checkpoint. A successful push synchronizes the commit with GitHub; it does not deploy the application.


## 2026-09-11 - Measuring extraction instead of guessing

We wrote synthetic resume snippets with expected skill sets in backend/evaluation/skill_cases.json. evaluate_skills.py compares expected and actual sets: their intersection is correct matches, actual-only values are false positives, and expected-only values are misses. Precision asks how many returned skills were correct; recall asks how many expected skills were found. Exact match requires the whole set to agree.

Example: Java Script expected JavaScript but returned Java and JavaScript. The extra Java lowered precision. skill_extractor.py now finds alias spans and prefers longer overlapping matches, preventing that false positive while preserving Java elsewhere. Supported cases improved from 12/13 to 13/13 exact sets. Ordinary react and missing Kotlin remain visible limitation probes. These development examples are not unseen test data or a claim of real-world accuracy.

Run from backend: .venv/Scripts/python.exe -m evaluation.evaluate_skills. Expect supported exact_matches 13, no supported mismatches, and two limitation mismatches. Full regression command: .venv/Scripts/python.exe -m unittest discover -s tests -v; expect 24 tests OK. A future change adding false matches or missing known terms should fail the supported-case regression. No server is needed for evaluation.

You should now explain precision, recall, false positives, missed skills, regression fixtures and why tuning against examples cannot establish performance on unseen resumes.


## 2026-09-11 - Display structured API results in React

ResumeList owns skillsId, which identifies the open skills panel. Clicking View skills mounts ResumeSkills; its effect calls getResumeSkills in services/api.js and stores the structured response in state. The skills array becomes list items using map. Hide/switch unmounts the old panel, cancelling its request and ignoring late responses. Text and skill selections are independent so they can be compared.

The response has two different empty cases. text_available=false means the parser supplied no readable text. text_available=true with skills=[] means the limited catalog found no matches. Separate messages help the user understand what happened. Matched terms do not establish proficiency.

With both development servers running, open http://127.0.0.1:5173/, log in and click View skills beside a resume. Expected: skills match the Postman response for the same resume ID; Hide skills closes the panel. Open View text to compare. For a failure check, block the /skills request in browser developer tools, open the panel, unblock and click Try again. Expect a readable error followed by results. Try switching panels while a request is slow; old results must not appear under another resume. Browser tests remain pending.

Start servers only if needed: from backend, .venv/Scripts/python.exe -m uvicorn app.main:app --reload; from frontend, npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort. Verification: frontend npm.cmd run build and npm.cmd run lint passed, plus isolated client checks for success, both empty states, failures and cancellation. You should now explain conditional rendering, structured response validation and effect cleanup.


## 2026-09-11 - A deterministic extraction baseline

Input: stored resume text. Output: canonical skill names mentioned in that text. services/skill_extractor.py owns the matching rules; routers/resumes.py owns HTTP and user authorization; schemas.py defines the response shape. This separation lets us test matching without a web server or database.

The matcher normalizes case and repeated whitespace, checks a small software-skills catalog with regular-expression boundaries, then sorts canonical names. Aliases such as postgres and postgresql map to PostgreSQL. Example: Python, FastAPI and python -> FastAPI, Python. The boundary prevents Java matching inside JavaScript. Each canonical skill is added at most once.

This is a rule-based baseline, not a trained model or LLM. It runs locally with no API cost or external transfer. A mention can occur in a negative statement, so No experience with Python still matches Python. No matches does not mean no skills; it means no terms from this catalog were found. text_available separates missing/blank parser output from usable text with no matches. Results are calculated on request and are not persisted.

Run tests from backend/: .venv/Scripts/python.exe -m unittest discover -s tests -v. Expected: 22 passing tests. Start backend if needed: .venv/Scripts/python.exe -m uvicorn app.main:app --reload; reuse the existing server. Postman: GET http://127.0.0.1:8000/resumes/<your resume ID>/skills with Bearer Token authentication. Expect 200 and keys resume_id, method, text_available, skills. Missing token -> 401; unavailable/foreign ID -> 404. For stored Python and FastAPI text, expected skills are FastAPI and Python. The dashboard does not display these results yet.

Evaluation at this checkpoint uses exact expected results on synthetic fixtures for matching, aliases, false substrings and failure cases. It does not establish real-world precision/recall. You should now explain deterministic rules versus model inference, aliases, boundary matching and why recognizing a term does not prove competence.


## 2026-09-11 - Resume details and on-demand loading

The list endpoint returns metadata; GET /resumes/{resume_id} loads one selected resume's stored text. In backend/app/routers/resumes.py the query checks both ID and current_user.id. A foreign or missing ID returns the same 404. In schemas.py ResumeDetailResponse inherits ResumeResponse and adds resume_text; Python must define the parent class first. The database model already has this field, so this response-schema extension does not require a migration.

ResumeList keeps selectedId in state. Clicking View text mounts ResumeText, whose effect calls services/api.js. Hiding or switching unmounts it and aborts its request. React renders the string in a pre element with wrapping; text is not inserted as HTML. Example: Python followed by a newline and FastAPI remains two lines. Empty/null text gets explanatory feedback. This is stored parser output, not AI-generated analysis.

With the existing servers running, open http://127.0.0.1:5173/, log in, and click View text beside your resume. Success: extracted text appears; Hide text closes it. Switch between resumes and confirm the displayed text belongs to the selected filename. To test a recoverable error, block the detail request in browser developer tools, open the text view, unblock and click Try again. Postman GET /resumes/<your ID> with bearer token -> 200 and resume_text; missing auth -> 401; another user's or nonexistent ID -> 404. Browser checks pending.

Run backend tests from backend/: .venv/Scripts/python.exe -m unittest discover -s tests -v. Expected: 13 tests pass. Run servers if needed: backend .venv/Scripts/python.exe -m uvicorn app.main:app --reload; frontend npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort. You should now explain path parameters, schema inheritance, ownership checks and loading details only when requested.


## 2026-09-11 - Read saved records and refresh React state

backend/app/routers/resumes.py now exposes GET /resumes. Its SQLAlchemy filter compares Resume.user_id with current_user.id from the validated token. Example: user 1 owns rows 1 and 3, user 2 owns row 2; user 1 receives only rows 3 and 1. Authentication identifies the caller; authorization limits the data they may read. ResumeResponse controls which fields leave the backend.

frontend/src/components/ResumeList.jsx calls getResumes through services/api.js in an effect. The result becomes React state, and map renders one list item per resume with a stable ID key. ResumeUpload calls onUploaded after success. Dashboard increments resumeVersion; changing the list component's key resets it and triggers a fresh fetch. Cleanup aborts the old request, preventing late responses replacing current results.

Run backend from backend/: .venv/Scripts/python.exe -m uvicorn app.main:app --reload. Run frontend from frontend/: npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort. Reuse existing servers. Open http://127.0.0.1:5173/ and log in: Your uploaded resumes should show existing filenames. Upload a disposable PDF: the list should reload and include it. A user with no resumes should see You have not uploaded a resume yet. For a recoverable failure, block /resumes in browser developer tools, load dashboard, then unblock and click Try again. Expect readable error followed by the list. Browser checks pending.

Postman: GET http://127.0.0.1:8000/resumes with Bearer Token auth -> 200 array; without token -> 401. Backend tests: .venv/Scripts/python.exe -m unittest discover -s tests -v (nine passing). You should now be able to explain GET versus POST, ownership filtering, empty arrays, rendering lists and callback-driven refresh.


## 2026-09-11 - Transactions and cleanup

In backend/app/routers/resumes.py, the original first commit permanently saved metadata before parsing. A later rollback could not undo it. Now parsing succeeds first, flush sends the row to SQLite within a reversible transaction, response validation runs, then one commit makes the row permanent. Example: parser raises -> rollback -> remove PDF -> error response, with no resume row. The filesystem is separate from SQLite, so removing the file requires explicit cleanup; this is not an atomic transaction across both systems.

The PDF service reads bytes before parsing and uses a with block to close the document even on failure. This prevents the reproduced corrupt-PDF Windows file lock, at the cost of loading the PDF into memory.

Run tests from backend: .venv/Scripts/python.exe -m unittest discover -s tests -v. Success: six tests report OK, including valid text persistence and failure cleanup. Before the fix the parser-failure test reported AssertionError: 1 != 0. Tests use unittest from Python itself; no added dependency. They call the route directly, so browser/auth/HTTP testing is separate. For a browser check, keep both servers running and upload a disposable valid PDF: expect success. A corrupt .pdf should show an upload error. Existing API behavior remains 500 for parser failures.

You should now be able to explain flush, commit, rollback, context managers, and why tests use an isolated database.


## 2026-09-11 - Browser upload milestone verified

User successfully uploaded a resume from the frontend. This exercises the React form -> multipart API request -> protected FastAPI upload -> success feedback flow. FormData carries the file, while the bearer header identifies its owner. You should now be able to explain why the file and authentication token travel in different parts of the same request. Failure-path browser checks remain pending.


## 2026-09-11 - Sending a file from React

ResumeUpload.jsx owns the form feedback and pending state; services/api.js owns HTTP communication. FormData packages the selected file under resume_file, matching FastAPI's parameter name. Example: body.append('resume_file', file). The browser sets multipart Content-Type including its boundary; setting application/json would prevent FastAPI from receiving the file. Authorization identifies the signed-in user. The accept attribute guides selection; backend validation remains authoritative. Disabling submit prevents repeat clicks while waiting. Aborting on logout stops the client waiting, but cannot undo a server save. A lost response can therefore mean the upload succeeded without confirmation.

Run backend from backend/: .venv/Scripts/python.exe -m uvicorn app.main:app --reload
Run frontend from frontend/: npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort
Reuse existing development servers when already running. Open http://127.0.0.1:5173/ and log in.

Happy path: select a disposable PDF containing selectable text and click Upload resume. Expect pending feedback, then Uploaded <filename> successfully; Network tab should show POST /resumes/upload with 201. Failure: select a non-PDF using the file-picker override; expect a readable validation message. Stop backend after loading dashboard, then upload: expect readable connection feedback and the button to become available again. Restart backend. A 401 should return to login. Verify browser behavior manually; current automated checks cover the API client only. Every upload saves a new row; there is no resume list or replacement UI yet.

You should be able to explain FormData versus JSON, the multipart field name, pending state and why cancelling a request does not undo a database write.


## 2026-09-10 - Effects and protected profile requests

Dashboard.jsx uses useEffect to load profile data when mounted. getCurrentUser in services/api.js sends GET /users/me with an Authorization bearer header. FastAPI validates the token and selects its user, then React renders the returned full_name/email. The effect cleanup aborts the request when leaving; checking the abort signal prevents old results changing a later screen. App uses useCallback to keep the session-expired callback stable so unrelated renders do not restart the request.

Example: login -> token in App state -> Dashboard mounts -> GET /users/me -> Welcome, name. If a protected request returns 401, App clears the token and asks for login. Network/server failures retain the session and offer Try again. Expiration is detected when requesting data, not by a background timer. Local logout still does not revoke issued tokens. Refresh still clears memory; production session design remains future work.

Run backend from backend/: .venv/Scripts/python.exe -m uvicorn app.main:app --reload. Run frontend from frontend/: npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort. Reuse existing servers; restart backend if it is not using reload, to pick up CORS changes. Open http://127.0.0.1:5173, log in, and expect Your dashboard with the registered name/email. Logout should restore the account forms. To check retry, use browser developer tools to temporarily block /users/me, log in, then unblock it and click Try again. Expect the profile to appear. Browser checks remain pending; token expiry and identity isolation were checked directly against the backend.

You should now be able to explain effects, cleanup, bearer headers, and why a 401 requires different UI behavior from a connection failure.

## 2026-09-10 - Login, callback props and shared state

LoginForm.jsx owns email/password/pending/error state. It calls loginUser in services/api.js; the API returns a bearer token when credentials match. App.jsx owns accessToken because it controls the page. Passing onLogin={setAccessToken} gives the child a callback prop: onLogin(result.access_token) changes the parent's state. App then conditionally renders the signed-in view. Logout sets state to null. The token is never rendered or persisted by application code.

Example: form submission -> loginUser -> POST /auth/login -> 200 + token -> callback -> App re-renders. Wrong password -> 401 -> readable error, form remains visible. A token in state is preparation for protected requests; the backend must validate it on each future protected operation. Local logout clears this UI's token but does not revoke a issued JWT on the server. This is a local learning checkpoint, not a production session design; expiration handling comes with /users/me.

Run FastAPI from backend/: .venv/Scripts/python.exe -m uvicorn app.main:app --reload. Run Vite from frontend/: npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort. Reuse running servers. Open http://127.0.0.1:5173 and register synthetic test details if needed. Login with the wrong password: expect Invalid email or password. Login correctly: expect You are logged in and Log out. Logout: expect forms again. Login then refresh: expect forms again. Stop backend and submit: expect readable connection feedback. These browser interactions remain pending verification.

You should now be able to explain why a parent holds shared state, how callback props move results from child to parent, and why refreshing clears in-memory state.

## 2026-09-10 - Connecting React to FastAPI

RegisterForm holds input values in state. Its async submit handler calls registerUser in src/services/api.js. fetch sends a POST with JSON.stringify converting a JavaScript object into JSON text. await waits for a response; catch displays failures; finally enables inputs again. fetch does not throw for HTTP 409/422, so response.ok must be checked explicitly.

Example: Create account -> JSON request -> FastAPI /auth/register -> hashed password and database row -> 201 response -> success message. React and FastAPI use different ports (different origins), so the browser first asks permission with an OPTIONS preflight. CORSMiddleware in backend/app/main.py allows the two specified local frontend origins. CORS is browser permission, not authentication.

Run backend from backend/: .venv/Scripts/python.exe -m uvicorn app.main:app --reload. Run frontend from frontend/: npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort. Reuse any existing dev servers. Open http://127.0.0.1:5173. Submit synthetic test details: expect success. Repeat email: expect duplicate feedback. Stop backend and submit: expect connection feedback. Browser checks remain pending.

You should now be able to trace an input from React state through JSON/HTTP to a database row and explain why HTTP errors require explicit handling.

## 2026-09-10 - Controlled inputs and form events

RegisterForm is a separate component so App can compose the welcome content and form without holding all input logic. useState stores each typed value; value displays that state and onChange updates it from event.target.value. This is a controlled input.

Example: const [email, setEmail] = useState('') pairs the current email with a function that changes it. The email input uses value={email} and onChange={(event) => setEmail(event.target.value)}.

handleSubmit receives the submit event. event.preventDefault() stops normal browser submission/navigation. Here it only sets a message; backend connection is next. required/type=email/pattern provide browser checks, but server validation will still be necessary. Labels use htmlFor matching input id, and role=status announces feedback.

Practice: explain the path from typing to state to rendered input. Try valid details, blank fields, invalid email, and spaces-only name. These browser checks are pending user verification.

---


## 2026-09-10 - First application component

App in frontend/src/App.jsx is a JavaScript function returning JSX, which describes the page. main.jsx renders App. A JSX className such as welcome connects an element to .welcome in App.css. index.css holds shared styles; App.css styles this page. Semantic main, header, section, and heading elements describe its structure.

Example: <h1>AI Career Assistant</h1> displays the main heading. Editing that text and saving updates the development page. The old counter state was removed because this welcome page displays static information.

Practice: explain how App.jsx content and CSS styling combine; refresh the page and narrow the browser to inspect wrapping. User already confirmed starter counter interaction.

---


## 2026-09-10 - Frontend tooling and the starter app

Node.js runs JavaScript development tools on the computer. npm installs the packages listed in frontend/package.json. Vite provides the local development server and creates a production build. React describes the interface using components.

In this project, index.html loads src/main.jsx, which renders the App component from src/App.jsx. The starter uses useState(0) to remember a count; clicking the button calls setCount to increase it and React updates the page.

Example: from frontend/, npm.cmd run dev starts the development server. npm.cmd run build creates dist/; npm.cmd run lint checks source code. node_modules/ contains downloaded dependencies; package-lock.json records resolved versions. Generated dependencies and dist/ are ignored by Git.

Practice: explain the role of each tool, open the starter page, and click the counter. Browser practice remains pending user verification.

---


This is the user’s learning record. Update it after meaningful development milestones.

---

# Concepts Already Introduced

## 1. HTTP Requests

The frontend/client sends HTTP requests to the backend.

Important parts:
- method
- URL
- headers
- body
- response
- status code

Examples:
- `GET` retrieves information.
- `POST` creates/submits information.

---

## 2. HTTP Status Codes

### 200 OK
Request succeeded.

### 201 Created
A new resource was successfully created.

Used for successful resume upload.

### 400 Bad Request
The request violates validation rules.

Example:
DOCX sent to a PDF-only endpoint.

### 401 Unauthorized
Authentication is missing or invalid.

Example:
Calling a protected resume endpoint without JWT.

---

## 3. FastAPI Routers

Routers organize endpoints by responsibility.

Current examples:
- authentication routes
- user routes
- resume routes

This prevents all API code from being placed into one huge file.

---

## 4. Dependency Injection

FastAPI uses `Depends(...)` to provide things a route needs.

Examples:
- database session
- authenticated current user

This keeps reusable logic out of individual route bodies.

---

## 5. Password Hashing

Applications should not store plaintext passwords.

Registration hashes the password before storing it.

Login verifies the submitted password against the stored hash.

---

## 6. JWT Authentication

After login, the server returns a JWT access token.

The client sends that token to protected endpoints using bearer authentication.

Mental model:

```text
Login
  -> server verifies password
  -> server creates token
  -> client stores/uses token
  -> protected request includes token
  -> backend identifies user
```

---

## 7. Multipart Form Data

File uploads are commonly sent as `multipart/form-data`.

For resume upload:
- key: `resume_file`
- type: File

---

## 8. File Validation

Current backend checks that resume uploads are PDFs.

This prevents unsupported file types from entering the parsing pipeline.

---

## 9. File Storage

Uploaded PDF is saved to a local `uploads` directory during development.

A generated stored filename avoids relying directly on user filenames.

---

## 10. SQLAlchemy

SQLAlchemy is used to communicate with the database through Python models and sessions.

Typical flow:

```text
Create Python model object
 -> add to session
 -> commit
 -> refresh
 -> database row exists
```

---

## 11. SQLite

SQLite is the current local database.

It is easy to inspect with SQLite Viewer and is appropriate for early development.

---

## 12. PDF Text Extraction

The project now takes a PDF resume and converts its content into text.

This changes the application from merely storing a file to being able to analyze the resume.

---

## 13. Service Layer

Reusable business logic such as PDF parsing should be separated from API route code.

Example concept:

```text
router
 -> receives HTTP request
 -> validates/orchestrates
 -> calls service

service
 -> performs reusable parsing/business logic
```

---

## 14. Git

Git tracks source-code history locally.

Important concepts already encountered:
- repository
- staging
- commit
- branch
- `.gitignore`

---

## 15. GitHub

GitHub stores the remote repository.

The project uses the `main` branch and has already been pushed successfully at an earlier checkpoint.

---

## 16. Postman

Postman is being used to test API endpoints before frontend integration.

This is useful because it isolates backend behavior from frontend bugs.

---

# Upcoming Learning Topics

## Frontend
- Node.js/npm role in frontend tooling
- Vite
- React
- JSX
- components
- props
- state
- event handlers
- forms
- routing
- API calls
- loading/error states

## Full Stack
- CORS
- browser requests
- Authorization header
- frontend token handling
- environment variables

## AI / ML
- resume cleaning
- information extraction
- skill extraction
- rule-based vs ML vs LLM
- embeddings
- semantic similarity
- AI evaluation
- prompt engineering
- structured output

## Production Engineering
- migrations
- environment management
- deployment
- CI/CD
- logging
- security
- testing

## 2026-09-16 - Environment-specific addresses

React needs the backend address; FastAPI needs the permitted frontend origins. These are different settings. For example, VITE_API_BASE_URL=https://api.example.com sends requests to the API, while CORS_ORIGINS=https://app.example.com permits that browser origin. Vite embeds its configuration when building, so changing the deployed server environment alone does not change an already-built frontend. Backend settings load on process startup. Neither setting replaces authentication. You should now be able to explain which address belongs on each side and when to restart versus rebuild. README contains run/test steps; 55 backend tests and Chrome workflow pass.

## 2026-09-16 - Application files versus persistent data

A deployment publishes code, but accounts and PDFs are data created while the app runs. In our project the SQLite file and uploads folder live relative to backend/. A host that replaces that folder can lose them. A persistent volume keeps data separate from replaceable code; it still needs backups. DEPLOYMENT.md describes the release sequence and the proof needed: create synthetic data, restart/redeploy, then verify rows AND uploaded files survive. Restoring a backup in a separate environment verifies recovery. A /health 200 only proves the process answers; it does not prove persistence. You should now be able to explain why a successful build is different from a verified deployment.

## 2026-09-16 - One storage setting for app and migrations

CAREER_DATA_DIR is the parent directory for SQLite and uploads. app/config.py validates it; database.py builds the SQLite URL; the resume router uses its uploads child. Alembic now uses the same engine, avoiding accidentally migrating one database while serving another. Defaults are anchored to backend/, so changing terminal directories cannot select a different database. Example: set an existing absolute directory in backend/.env, run migrations, restart backend. Success is data created under that directory; a relative/missing directory fails configuration. Tests use temporary directories, including spaces and percent signs, and verify the file remains in a fresh process. You should explain why configured storage survives process restarts but needs a real retained volume to survive host replacement. Existing data is never automatically moved.

## 2026-09-16 - Clean environments reveal hidden dependencies

A project can work locally because an old package is installed even when it is missing from requirements.txt. A new virtual environment tests the written dependency list. We installed only the pinned requirements there, ran pip check and all 58 tests, then migrated a temporary database and started the FastAPI lifespan. An isolated frontend copy passed npm ci, build and lint. npm ci uses the lockfile for reproducible dependency versions. The copy must include ignore files too: omitting .gitignore made lint inspect node_modules until the file was restored. You should distinguish a clean environment from a clean operating system: Windows success does not verify Linux hosting. Normal development files and databases remained untouched.

## 2026-09-16 - Continuous integration

CI runs repeatable checks after code changes arrive on GitHub. .github/workflows/ci.yml describes events, jobs and steps. The backend matrix runs the same checks on two operating systems; the frontend job installs locked dependencies and runs lint/build. This can expose OS-specific failures that Windows-only testing misses. After pushing, open Actions > Project checks: green jobs mean their commands passed, while a red job requires reading the first failing step. Workflow creation alone is not proof it runs: the first remote run remains pending. You should explain the difference between local testing, CI verification and deployment. CI here publishes no app and uses no production data.

## 2026-09-16 - Reading the first successful CI run

[Project checks](https://github.com/Vamshinethula/ai-career-assistant/actions/runs/35131859172) passed on GitHub for commit 1c468db. Each backend job installed dependencies, ran the test suite and checked migrations; the Ubuntu frontend job installed, linted and built. A green run is evidence for that exact commit and those commands. It does not prove the hosted app is reachable or that uploaded files survive redeployment. To investigate a red run, open the failed job and first failed step. You should now be able to separate installation failures, test failures, build failures and deployment failures. No source change or test rerun was needed to record this successful result.

## Renaming a snapshot

PATCH updates part of a resource. The backend shares title validation between save and rename, checks ownership first, and writes only the title. The frontend refreshes history because a renamed title may no longer match the current search. Tests compare the entire response to prove snapshot contents remain unchanged.
