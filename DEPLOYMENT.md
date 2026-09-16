# Deployment readiness and runbook

Status: preparation only. No hosting service has been selected or deployed.
Local verification includes 58 backend tests, frontend build/lint, and a real
Chrome workflow. A fresh Windows Python environment passed installation, all tests,
migrations and application startup; an isolated frontend passed npm ci/build/lint.
Linux installation, public HTTPS, persistence across redeploys,
and backup restoration have not been verified.

## Choose the first deployment's data policy

| Option | Data expectations | Required preparation |
| --- | --- | --- |
| Disposable portfolio demo | Synthetic accounts and resumes only; data can disappear | State the reset behavior clearly; test the chosen host |
| Persistent app | Accounts and PDFs survive restarts/redeploys | Persistent storage, backup/restore verification, and storage configuration |

No provider, cost commitment, or real user-data migration is authorized by this
document. Hosting requirements depend on the chosen option.

## Current storage requirements

`CAREER_DATA_DIR` selects an existing absolute directory holding
`career_assistant.db` and `uploads/`. Environment overrides backend/.env; omitting
it uses the repository's backend directory. App and Alembic use the same setting.
Create/mount the directory before startup and run migrations with that setting.

A host that replaces its application filesystem can lose default storage. A
persistent deployment must mount a retained volume and point CAREER_DATA_DIR at
it. This configuration is verified locally across processes, but no actual host
volume or redeploy has been tested. Changing the setting does not move data.
Existing installations require a backup/copy plan and review of saved file paths;
copying just the database is not a complete migration.

Use one backend instance and one worker for the initial deployment plan. Shared
storage, concurrent writers, and multiple instances need separate design and
testing. Do not treat a local SQLite file as a shared hosted database.

## Runtime contract

| Component | Configuration |
| --- | --- |
| Frontend | Build with Node/npm; publish `frontend/dist` as static files |
| Backend | Python 3.12 environment; install `backend/requirements.txt` |
| JWT | Host secret named `JWT_SECRET_KEY`, random and at least 32 bytes |
| Browser origins | `CORS_ORIGINS=https://your-frontend-host` (no trailing slash) |
| API address | `VITE_API_BASE_URL=https://your-api-host` before frontend build |
| Backend working directory | `backend/` for the documented CLI commands |
| Health probe | `GET /health` returns 200 after successful startup |

`/health` reports process liveness; it does not check database queries or disk
space. Startup checks the recorded migration version. These are different checks.

Never put JWT secrets into `VITE_` variables, Git, or frontend files. The frontend
API address is public and embedded at build time. Backend environment changes
require restart; frontend address changes require rebuilding the static files.
Use HTTPS for both public addresses and keep the backend's allowed origins exact.

## Candidate release sequence

These are command templates for the selected host, not evidence of deployment.
Do not run them against an existing valuable database without its backup.

1. Install dependencies into an isolated Python environment. From `backend/`:

   ```text
   python -m pip install -r requirements.txt
   python -m pip check
   ```

2. Configure the JWT secret, frontend origin, and verified storage arrangement.
   Back up existing data using the [migration guide](backend/migrations/README.md).
   Run migrations once before starting the new backend:

   ```text
   python scripts/migrate_database.py
   python -m alembic current
   python -m alembic check
   ```

3. Start the backend bound to the host interface, without development reload:

   ```text
   python -m uvicorn app.main:app --host 0.0.0.0 --port <host-assigned-port> --workers 1
   ```

   Replace the port placeholder with the host's actual port using its launch
   configuration. Health checks must target that port.

4. Set `VITE_API_BASE_URL` in the frontend build environment. From `frontend/`:

   ```text
   npm ci
   npm run build
   ```

   Publish `dist/` using the host's static-file service. The Vite development
   server on port 5173 is for local development.

5. Verify in a browser using synthetic data: register, log in, upload a valid
   PDF, list it, view text/skills/roles, log out. Check invalid input feedback
   and unauthorized access. Verify an unlisted origin does not receive CORS
   permission; CORS is not a replacement for authentication.

6. For persistent mode, restart and redeploy, then verify the synthetic account,
   resume row, extracted text and original PDF all remain. Test restoring a
   backup in a separate disposable environment before claiming recovery works.

## Remaining readiness checks

- Clean installation on the chosen host OS, including PyMuPDF and bcrypt.
- A tested storage arrangement for the selected data policy.
- HTTPS, origin configuration, migration/startup ordering and public smoke test.
- Request-body limits before application spooling and parser resource controls.
- Authentication abuse controls, operational logs, monitoring and disk limits.
- Backup retention and restoration for any persistent user data.
- Full accessibility review and portfolio demo instructions.

Application upload limits (5 MiB / 10 pages) run after multipart receipt; they
do not establish host-level request or parsing resource limits. Authentication rate limiting is not implemented, and logout does not revoke issued JWTs.

If a release fails, preserve its database and uploads. Do not delete the database
or force a migration stamp to make startup pass. Application rollback must be
compatible with the recorded database schema; the baseline downgrade deliberately
refuses to drop user tables. Restore only through a verified recovery procedure.
