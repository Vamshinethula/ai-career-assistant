"""Run from backend after backing up an existing database."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import engine
from app.migrations import migrate_database

if __name__ == '__main__':
    migrate_database(engine)
    print('Database migrations are up to date.')
