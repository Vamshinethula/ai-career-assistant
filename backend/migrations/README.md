# Database migrations

Run commands from `backend/`. The app and migration CLI share CAREER_DATA_DIR;
when omitted, storage is anchored to backend/. For custom storage, set the same
value for every command and use its database path in the backup example below.
Install `requirements.txt` before using Alembic.

## Preserve existing data

Stop the application before database maintenance. For an existing database,
create a SQLite snapshot first (this does not overwrite an earlier backup):

```powershell
@'
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
source_path = Path('career_assistant.db').resolve()
backup_dir = Path('backups')
backup_dir.mkdir(exist_ok=True)
backup_path = backup_dir / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.db')
with sqlite3.connect(source_path.as_uri() + '?mode=ro', uri=True) as source:
    with sqlite3.connect(backup_path) as target:
        source.backup(target)
print('Database backup created in backups/.')
'@ | ./.venv/Scripts/python.exe -
```

Backups contain private account and resume data; `backups/` is ignored by Git.
Keep uploaded files separately as part of any complete application backup.
The migration command does not automatically back up data.

## Apply and check

```powershell
./.venv/Scripts/python.exe scripts/migrate_database.py
./.venv/Scripts/python.exe -m alembic current
./.venv/Scripts/python.exe -m alembic check
```

Expected current revision: `0001_initial (head)`. Check should report no new
upgrade operations. A fresh database receives the baseline tables. For an
unversioned database, the helper compares its schema with the frozen baseline
before recording the version. A detected mismatch raises an error; inspect it
without deleting the database or forcing `alembic stamp`. Alembic comparison
does not detect every possible schema difference, so review unusual old schemas.

Start FastAPI normally afterward. Its startup checks the recorded revision and
provides the migration command when behind. This is not a full schema drift audit.
Repeating the migration command at head is safe. The initial downgrade refuses
to delete account/resume tables; restoring backups is a separate maintenance task.

## Future schema changes

Update models, then generate a new revision:

```powershell
./.venv/Scripts/python.exe -m alembic revision --autogenerate -m "Describe the schema change"
```

Review the generated upgrade and downgrade, especially data loss, new required
columns and SQLite batch operations. Test on a disposable database and an existing
schema with synthetic data. Back up valuable data, apply the migration command,
and verify results before restarting. Never edit an already applied revision to
represent a new change. Commit reviewed migration files with the model changes.
