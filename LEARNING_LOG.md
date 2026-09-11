# LEARNING_LOG.md — AI Career Assistant

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
