# First deployment proposal

Status: disposable synthetic demo selected by the user, 2026-09-17. Render is
a candidate, not a selected or provisioned host. No account, paid service,
deployment, or data migration has been created.

## Proposed layout

Use a Python web service for FastAPI and a static site for the built React app.
This preserves the current architecture and lets each service use its own build
command. Start with one backend instance and one worker.

| Setting | Backend | Frontend |
| --- | --- | --- |
| Repository root directory | `backend` | `frontend` |
| Runtime | Python 3.12, explicitly select a supported patch version | Node 24 |
| Build | `python -m pip install -r requirements.txt` | `npm ci && npm run build:demo` |
| Published files | Not applicable | `dist` |
| Health check | `/health` | Open the site in a browser |
| Public configuration | `CORS_ORIGINS` = exact frontend HTTPS origin | `VITE_API_BASE_URL` = backend HTTPS origin |
| Private configuration | New random `JWT_SECRET_KEY`, at least 32 bytes | None |

Candidate Linux start command, entered in the hosting dashboard, not PowerShell:

```sh
python scripts/migrate_database.py && exec python -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --workers 1
```

This runs migrations before serving requests and stops startup if migration
fails. For a disk-backed instance, migrations must run where the mounted disk
is available, not against a build-time database. The configured storage directory
must already exist. This command has been reviewed against repository paths;
it has not been executed on Render.

## Data policy changes the storage plan

Selected: disposable synthetic demo. Leave CAREER_DATA_DIR unset for the proposed
ephemeral backend and do not attach a paid disk. Do not transfer local accounts,
PDFs, database files or `.env`. Generate a separate hosted JWT key.

The frontend demo build displays a synthetic-data/reset notice above account
forms and the dashboard. This build mode is informational: it does not detect
personal data, delete records, or schedule resets. Storage resets belong to the
host lifecycle. A normal local restart still preserves local data.

Preview the notice locally from `frontend/` with `npm.cmd run dev:demo -- --host
127.0.0.1 --port 5174 --strictPort`. For API use on that port, configure backend
CORS explicitly or use the isolated browser test below. A UI-only preview does
not require changing the normal backend configuration.

From the project root, run the isolated demo verification:

```powershell
$env:CAREER_TEST_DEMO='true'
node backend/tests/browser_smoke.mjs
Remove-Item Env:CAREER_TEST_DEMO
```

Verified locally: lint, demo/normal production builds, notice presence/absence
in built JavaScript, and full real Chrome workflow in both modes. Demo testing
uses a separate Vite server on port 5174 with temporary synthetic backend data.
Both build commands write `frontend/dist`; the last command wins. The hosting
build must use `build:demo`, not publish an older normal-build directory.

| Policy | Proposed storage | Required before launch |
| --- | --- | --- |
| Disposable synthetic demo | Ephemeral SQLite and uploads; default backend directory | Prominent synthetic-data/reset notice; verify startup recreates schema after reset; document cold starts |
| Persistent app | Paid backend with retained disk; CAREER_DATA_DIR points to its absolute mount path | User-approved cost, protected backups/retention, host restart/redeploy and recovery verification |

Render's free backend can sleep after 15 idle minutes, take about a minute to
wake, and lose local data on sleep/restart/redeploy. It cannot attach a persistent
disk. Its free offerings have usage limits; verify billing settings before
creation. These constraints make it a candidate for an explicitly disposable
demo, not a guarantee of durable or always-available service.

The app's current request timeout may finish before a sleeping backend wakes.
A demo runbook should first open the backend health URL and wait until healthy,
then open the frontend. Cold-start feedback needs host verification.

For persistent storage, keep a stable mount path: existing resume rows save PDF
paths. Start with new synthetic hosted data, not a copy of the personal local
database. Local same-path recovery evidence does not establish hosted recovery.

## Remaining deployment sequence

1. Completed locally: selected demo mode's notice, build command and browser checks.
2. Run applicable checks and review a Git checkpoint; preserve pending edits.
3. Select provider/plan and review any cost before provisioning. Determine the
   two actual service URLs, then set CORS and frontend API configuration to match.
4. Deploy the reviewed commit with fresh hosted secrets and the selected storage.
5. Verify HTTPS, health, registration/login, upload, text/skills/roles, ownership
   failures and logout in the actual hosted browser flow.
6. Restart/redeploy: verify documented reset for demo mode, or retained account,
   database rows and PDF bytes for persistent mode. Check logs without exposing
   secrets or personal resume contents.

Success is a verified public workflow with the chosen data behavior. A green CI
run alone does not mean the app has been deployed successfully.

## Sources reviewed

- [Render FastAPI setup](https://render.com/docs/deploy-fastapi)
- [Render static sites](https://render.com/docs/static-sites)
- [Free service limitations](https://render.com/docs/free)
- [Persistent disks](https://render.com/docs/disks)
- [Project deployment runbook](DEPLOYMENT.md)
- [Local recovery evidence](backend/tests/BACKUP_RECOVERY.md)
