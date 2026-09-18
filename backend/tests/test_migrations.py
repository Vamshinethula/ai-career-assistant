import unittest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, text
from app import models
from app.database import Base
from app.migrations import BASELINE, migrate_database, require_current_schema
from app.migrations import migration_config
from alembic import command

HEAD = '0002_saved_comparisons'


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        self.addCleanup(self.engine.dispose)

    def test_fresh_database_matches_models_and_repeat_is_safe(self):
        migrate_database(self.engine)
        migrate_database(self.engine)
        with self.engine.connect() as connection:
            self.assertEqual(MigrationContext.configure(connection).get_current_revision(), HEAD)
            self.assertEqual(compare_metadata(MigrationContext.configure(connection), Base.metadata), [])

    def test_adopt_existing_schema_preserves_rows(self):
        with self.engine.begin() as connection:
            command.upgrade(migration_config(connection), BASELINE)
            connection.execute(text('DELETE FROM alembic_version'))
        with self.engine.begin() as connection:
            connection.execute(text("INSERT INTO users VALUES (1, 'Synthetic User', 'test@example.com', 'synthetic-hash', 1)"))
            connection.execute(text("INSERT INTO resumes VALUES (1, 'sample.pdf', 'stored.pdf', 'unused', 'Python', 1, '2026-09-16 00:00:00')"))
        migrate_database(self.engine)
        with self.engine.connect() as connection:
            self.assertEqual(connection.execute(text('SELECT hashed_password FROM users')).scalar(), 'synthetic-hash')
            self.assertEqual(connection.execute(text('SELECT resume_text FROM resumes')).scalar(), 'Python')
            self.assertEqual(MigrationContext.configure(connection).get_current_revision(), HEAD)

    def test_mismatched_schema_is_not_stamped(self):
        with self.engine.begin() as connection:
            connection.execute(text('CREATE TABLE users (id INTEGER PRIMARY KEY)'))
        with self.assertRaisesRegex(RuntimeError, 'differs from the baseline'):
            migrate_database(self.engine)
        with self.engine.connect() as connection:
            self.assertIsNone(MigrationContext.configure(connection).get_current_revision())

    def test_versioned_baseline_upgrade_preserves_data(self):
        with self.engine.begin() as connection:
            command.upgrade(migration_config(connection), BASELINE)
            connection.execute(text("INSERT INTO users VALUES (1, 'Test', 'upgrade@example.com', 'synthetic-hash', 1)"))
        migrate_database(self.engine)
        require_current_schema(self.engine)
        with self.engine.connect() as connection:
            self.assertEqual(connection.execute(text('SELECT count(*) FROM users')).scalar(), 1)
            self.assertEqual(connection.execute(text('SELECT count(*) FROM saved_comparisons')).scalar(), 0)

    def test_startup_requires_migrations(self):
        with self.assertRaisesRegex(RuntimeError, 'needs migration'):
            require_current_schema(self.engine)
        migrate_database(self.engine)
        require_current_schema(self.engine)
