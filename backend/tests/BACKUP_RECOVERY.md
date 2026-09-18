# Local backup recovery drill

Run from `backend/`:

```powershell
./.venv/Scripts/python.exe -m unittest discover -s tests -p test_backup_recovery.py -q
```

Success is `Ran 2 tests` and `OK`. The drill creates only temporary synthetic
accounts, a migrated SQLite database, and a generated PDF. It never backs up,
renames, restores, or overwrites the normal application data directory.

## What is verified

The test registers two users and uploads a PDF through the real API routes.
With no requests in progress, it closes database connections, takes a SQLite
backup using `Connection.backup`, checks database integrity, and copies uploads.
It renames the temporary original directory out of the way, then restores the
snapshot to the same original absolute path and opens a new database engine.

Checks cover migration version, fresh login with the saved password, profile,
resume list/text/skills/role results, byte-for-byte PDF equality, wrong-password
rejection (401), unauthenticated access (401), and another user's access (404).
The second test deliberately restores only the database: login and saved text
still work, but reading the PDF raises FileNotFoundError. That is the expected
failure case and demonstrates why dashboard success alone is insufficient.

This is an offline local drill, not a production backup service, browser test,
cross-machine restore, hosted-volume test, or recovery-time guarantee. The normal
backend regression suite discovers both tests automatically.

## Operational procedure for a future persistent installation

1. Stop the application and all other writers for the entire snapshot operation.
   SQLite's backup API protects the database snapshot; it does not atomically
   snapshot the separate upload files.
2. Record the application revision, migration revision, absolute data directory,
   and runtime configuration. Protect secrets separately; do not commit them.
3. In a new private backup directory, take the SQLite snapshot using the
   [migration guide](../migrations/README.md), selecting the actual configured
   database. Copy the complete `uploads/` directory while writers remain stopped.
   Check database integrity and record file hashes/counts before accepting it.
4. Keep the snapshot immutable and preserve the failed/current data separately.
   Rehearse recovery in an isolated environment before changing valuable data.
5. Restore database and uploads together at the same absolute storage path.
   Set CAREER_DATA_DIR accordingly and use the matching application revision.
   Check migration compatibility before startup; do not force a version stamp.
6. Verify login, ownership, row counts, saved text/results, and the existence and
   hashes of every referenced PDF before reopening access. A missing or altered
   PDF means recovery is incomplete even if the dashboard works.

Current resume records contain saved file paths. A different root, drive, or OS
can make those paths invalid. Path relocation and older relative-path records
require a separate reviewed migration; this drill does not rewrite paths.
JWT configuration is separate from account data: a new signing key requires fresh
login but does not require resetting saved password hashes.

Real backups contain private resumes and password hashes. Restrict access and
choose protected off-machine storage and retention before persistent deployment.
Neither off-machine storage nor a retention schedule is implemented here.
