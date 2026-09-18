# Saved comparisons

Explicit Save comparison stores a bounded title (1-120 characters), job text
(1-10,000), server-recomputed results and validated user choices privately under
an owned resume. Automatic results are snapshots, not recalculated on reopen.
Reviewed overlap derives from saved keywords/choices using the current formula.
Each save creates a new read-only row; editing is not yet
implemented. Lost responses can cause duplicate saves on retry: refresh history
first. Demo storage resets can still erase saved rows.

POST /resumes/{id}/comparisons accepts title, job_description and label_choices.
Only detected job skills and known categories are accepted. The server does not
trust client-supplied scores. GET the same path for newest-first metadata; append
/{saved_id} for detail. All routes check ownership. Invalid requests return 422,
foreign/missing resources 404 and missing authentication 401. No external AI or
new dependency. UTC timestamp normalization handles SQLite timezone loss.

## Migration and verification

Revision 0002_saved_comparisons adds a table and two indexes without changing
existing users/resumes. Downgrade refuses deletion. Back up first; from backend
run python scripts/migrate_database.py and python -m alembic check, then restart.
The local migration was applied after an ignored SQLite backup on 2026-09-18.
Existing user/resume rows compared unchanged; integrity and model checks passed.

Verified: 79 backend tests covering fresh/unversioned/versioned migrations,
re-login, ownership, input validation and immutable snapshots. The backup drill
also restores a saved snapshot. Seven frontend tests, lint, both builds and both
Chrome workflows pass, including save failure/retry, logout/login/reopen and mobile.
Test data was synthetic. No commit or remote CI run for this feature, as requested.

DELETE /resumes/{id}/comparisons/{saved_id} removes only the owned snapshot, returns empty 204, and returns 404 if missing or foreign-owned (401 without authentication). The UI requires confirmation, supports cancellation and displays request failures. Refresh after an uncertain response. API tests preserve PDF bytes, resume text and other snapshots; both Chrome modes verify cancel, blocked-request retry and removal after refresh. No additional migration is needed.

History pagination: GET accepts offset >= 0 and limit 1..100 (default 20). Clients must paginate to retrieve all rows. Newest-first ordering uses created_at then ID descending. UI shows ten rows, requests eleven to detect another page, and resets to newest on refresh/save/delete. Concurrent writes may shift offsets. API boundaries/validation/ownership and normal/demo browser navigation verified.

Title search: optional search query (max 120), trimmed and literal substring-matched before offset/limit. SQLAlchemy autoescape prevents percent/underscore wildcard expansion. SQLite case folding is primarily ASCII. UI submits explicitly, clears to all rows and distinguishes no matches. Refresh/delete keeps filter; save resets it. Verified 80 backend tests and both browser modes; search does not examine job descriptions.

PATCH /resumes/{id}/comparisons/{saved_id} accepts title (1-120 characters, nonblank). Only metadata title changes; contents remain snapshots. Verified 81 backend tests and both Chrome modes including rename/reopen.
