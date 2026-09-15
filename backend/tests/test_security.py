"""Synthetic legacy fixtures were generated with Passlib before its removal."""
import json
import unittest
from pathlib import Path
from pydantic import ValidationError
from app.schemas import UserCreate
from app.security import hash_password, verify_password


class PasswordTests(unittest.TestCase):
    def test_legacy_hashes_still_verify(self):
        fixtures = json.loads(Path(__file__).with_name('fixtures').joinpath('legacy_bcrypt.json').read_text())
        for fixture in fixtures:
            with self.subTest(case=fixture['label']):
                self.assertTrue(verify_password(fixture['password'], fixture['hash']))
                self.assertFalse(verify_password('incorrect-password', fixture['hash']))

    def test_new_hashes_have_random_salts_and_verify(self):
        password = 'Synthetic-caf\u00e9'
        first, second = hash_password(password), hash_password(password)
        self.assertNotEqual(first, second)
        self.assertTrue(first.startswith('$2b$12$'))
        self.assertTrue(verify_password(password, first))
        self.assertFalse(verify_password('wrong', first))

    def test_new_password_limits_use_bytes(self):
        for password in ('a' * 72, '\u00e9' * 36):
            self.assertTrue(verify_password(password, hash_password(password)))
        for password in ('', 'a' * 73, '\u00e9' * 37, 'abc\x00def'):
            with self.subTest(length=len(password)):
                with self.assertRaises(ValueError):
                    hash_password(password)
                with self.assertRaises(ValidationError):
                    UserCreate(full_name='Test', email='test@example.com', password=password)

    def test_invalid_login_fails_safely(self):
        self.assertFalse(verify_password('test', 'invalid hash'))
        self.assertFalse(verify_password('test', '\u00e9'))
        self.assertFalse(verify_password('x' * 4097, 'invalid'))
        self.assertFalse(verify_password('abc\x00def', 'invalid'))
