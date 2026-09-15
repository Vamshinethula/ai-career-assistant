import os
import secrets
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_environment
from jose import JWTError, jwt

from app.config import load_jwt_secret
from app.jwt_handler import ALGORITHM, SECRET_KEY, create_access_token


class ConfigurationTests(unittest.TestCase):
    def test_env_file_loads_and_environment_wins(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / '.env'
            file_key, environment_key = secrets.token_urlsafe(48), secrets.token_urlsafe(48)
            path.write_text('JWT_SECRET_KEY=' + file_key, encoding='utf-8')
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(load_jwt_secret(path), file_key)
            with patch.dict(os.environ, {'JWT_SECRET_KEY': environment_key}):
                self.assertEqual(load_jwt_secret(path), environment_key)
            with patch.dict(os.environ, {'JWT_SECRET_KEY': ''}):
                with self.assertRaises(RuntimeError):
                    load_jwt_secret(path)

    def test_missing_and_short_keys_fail_without_disclosure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'absent.env'
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(RuntimeError):
                    load_jwt_secret(path)
            for key in ('', 'short-test-key', ' ' * 64):
                with patch.dict(os.environ, {'JWT_SECRET_KEY': key}):
                    with self.assertRaises(RuntimeError) as raised:
                        load_jwt_secret(path)
                    if key.strip():
                        self.assertNotIn(key, str(raised.exception))

    def test_startup_rejects_invalid_environment_key(self):
        environment = dict(os.environ, JWT_SECRET_KEY='')
        result = subprocess.run([sys.executable, '-c', 'import app.jwt_handler'],
                                env=environment, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('JWT_SECRET_KEY must contain at least 32 bytes', result.stderr)

    def test_tokens_use_configured_key_and_expire(self):
        token = create_access_token({'sub': '1'})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(payload['sub'], '1')
        self.assertIn('exp', payload)
        with self.assertRaises(JWTError):
            jwt.decode(token, secrets.token_urlsafe(48), algorithms=[ALGORITHM])
        expired = jwt.encode({'sub': '1', 'exp': 0}, SECRET_KEY, algorithm=ALGORITHM)
        with self.assertRaises(JWTError):
            jwt.decode(expired, SECRET_KEY, algorithms=[ALGORITHM])
