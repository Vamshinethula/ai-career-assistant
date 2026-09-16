"""Create fresh schemas or adopt an exactly matching unversioned baseline."""
from pathlib import Path

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import MetaData, create_engine, inspect


BASELINE = '0001_initial'


def migration_config(connection):
    config = Config(str(Path(__file__).resolve().parents[1] / 'alembic.ini'))
    config.attributes['connection'] = connection
    return config


def migrate_database(engine):
    with engine.begin() as connection:
        config = migration_config(connection)
        tables = set(inspect(connection).get_table_names())
        version = MigrationContext.configure(connection).get_current_revision()
        if tables - {'alembic_version'} and version is None:
            # Reflect the frozen revision, not today's possibly changed models.
            baseline_engine = create_engine('sqlite://')
            try:
                with baseline_engine.begin() as baseline_connection:
                    command.upgrade(migration_config(baseline_connection), BASELINE)
                    expected = MetaData()
                    expected.reflect(bind=baseline_connection, only=['users', 'resumes'])
                differences = compare_metadata(
                    MigrationContext.configure(connection, opts={'compare_type': True}), expected)
                if differences:
                    raise RuntimeError('Existing schema differs from the baseline. No version was recorded; inspect it before migrating.')
                command.stamp(config, BASELINE)
            finally:
                baseline_engine.dispose()
        command.upgrade(config, 'head')


def require_current_schema(engine):
    with engine.connect() as connection:
        current = MigrationContext.configure(connection).get_current_revision()
        head = ScriptDirectory.from_config(migration_config(connection)).get_current_head()
        if current != head:
            raise RuntimeError('Database needs migration. From backend run: .venv/Scripts/python.exe scripts/migrate_database.py')
