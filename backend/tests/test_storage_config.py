import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.config import ENV_FILE, load_data_directory


class StorageConfigurationTests(unittest.TestCase):
    def test_default_file_and_environment_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = root / '.env'
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(load_data_directory(config), ENV_FILE.parent)
                config.write_text('CAREER_DATA_DIR=' + root.as_posix(), encoding='utf-8')
                self.assertEqual(load_data_directory(config), root)
            other = root / 'other'
            other.mkdir()
            with patch.dict(os.environ, {'CAREER_DATA_DIR': str(other)}):
                self.assertEqual(load_data_directory(config), other)

    def test_invalid_directory_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file = root / 'file'
            file.touch()
            for value in ('', 'relative', str(root / 'missing'), str(file)):
                with self.subTest(value=value), patch.dict(os.environ, {'CAREER_DATA_DIR': value}):
                    with self.assertRaises(RuntimeError):
                        load_data_directory()

    def test_migration_cli_and_app_share_storage_across_working_directories(self):
        backend = ENV_FILE.parent
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            # Percent/space ensure paths are not interpreted as URL/config escapes.
            data = root / 'data % space'
            data.mkdir()
            environment = dict(os.environ, CAREER_DATA_DIR=str(data), PYTHONPATH=str(backend))

            def run(*args):
                result = subprocess.run([sys.executable, *args], cwd=root, env=environment,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout

            run(str(backend / 'scripts/migrate_database.py'))
            self.assertIn('0002_saved_comparisons', run('-m', 'alembic', '-c', str(backend / 'alembic.ini'), 'current'))
            self.assertIn('No new upgrade operations', run('-m', 'alembic', '-c', str(backend / 'alembic.ini'), 'check'))
            run('-c', "from app.config import load_data_directory; from app.database import engine; from app.migrations import require_current_schema; from app.routers.resumes import UPLOAD_DIRECTORY; require_current_schema(engine); assert UPLOAD_DIRECTORY == load_data_directory() / 'uploads'; (UPLOAD_DIRECTORY / 'synthetic.txt').write_text('test')")
            run('-c', "from app.routers.resumes import UPLOAD_DIRECTORY; assert (UPLOAD_DIRECTORY / 'synthetic.txt').read_text() == 'test'")
            self.assertTrue((data / 'career_assistant.db').is_file())
            self.assertFalse((root / 'career_assistant.db').exists())
