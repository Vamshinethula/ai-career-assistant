import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import load_cors_origins


class CorsTests(unittest.IsolatedAsyncioTestCase):
    def test_defaults_file_and_environment_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / '.env'
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(len(load_cors_origins(path)), 2)
                path.write_text('CORS_ORIGINS=https://app.example.com', encoding='utf-8')
                self.assertEqual(load_cors_origins(path), ['https://app.example.com'])
            with patch.dict(os.environ, {'CORS_ORIGINS': ' https://other.example.com,https://other.example.com '}):
                self.assertEqual(load_cors_origins(path), ['https://other.example.com'])

    def test_invalid_origins_fail(self):
        for value in ('', '*', 'null', 'https://example.com/', 'https://example.com/path',
                      'https://user:pass@example.com', 'https://example.com?x=1',
                      'https://example.com#section', 'ftp://example.com', 'http://localhost:99999'):
            with self.subTest(value=value), patch.dict(os.environ, {'CORS_ORIGINS': value}):
                with self.assertRaises(RuntimeError):
                    load_cors_origins()

    async def test_custom_origin_preflight_allowed_and_foreign_origin_denied(self):
        with patch.dict(os.environ, {'CORS_ORIGINS': 'https://app.example.com'}):
            app = FastAPI()
            app.add_middleware(CORSMiddleware, allow_origins=load_cors_origins(),
                               allow_methods=['GET', 'POST'], allow_headers=['Content-Type', 'Authorization'])
        for origin, status in [('https://app.example.com', 200), ('https://other.example.com', 400)]:
            messages = []

            async def receive():
                return {'type': 'http.request', 'body': b'', 'more_body': False}

            async def send(message):
                messages.append(message)

            await app({'type': 'http', 'method': 'OPTIONS', 'path': '/resumes',
                       'headers': [(b'origin', origin.encode()),
                                   (b'access-control-request-method', b'GET'),
                                   (b'access-control-request-headers', b'Authorization')]}, receive, send)
            response = next(message for message in messages if message['type'] == 'http.response.start')
            self.assertEqual(response['status'], status)
            self.assertEqual(dict(response['headers']).get(b'access-control-allow-origin'),
                             origin.encode() if status == 200 else None)
