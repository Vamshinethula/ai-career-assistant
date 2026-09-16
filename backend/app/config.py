"""Local .env support; deployment environment variables take precedence."""
import os
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import dotenv_values


ENV_FILE = Path(__file__).resolve().parents[1] / '.env'
MAX_RESUME_BYTES = 5 * 1024 * 1024
MAX_RESUME_PAGES = 10


def load_data_directory(env_file: Path = ENV_FILE) -> Path:
    value = os.environ.get('CAREER_DATA_DIR')
    if value is None:
        value = dotenv_values(env_file, interpolate=False).get('CAREER_DATA_DIR')
    if value is None:
        return ENV_FILE.parent
    directory = Path(value.strip())
    if not value.strip() or not directory.is_absolute() or not directory.is_dir():
        raise RuntimeError('CAREER_DATA_DIR must be an existing absolute directory.')
    return directory.resolve()


def load_cors_origins(env_file: Path = ENV_FILE) -> list[str]:
    value = os.environ.get('CORS_ORIGINS')
    if value is None:
        value = dotenv_values(env_file, interpolate=False).get('CORS_ORIGINS')
    if value is None:
        return ['http://127.0.0.1:5173', 'http://localhost:5173']
    origins = [item.strip() for item in value.split(',')]
    for origin in origins:
        try:
            parsed = urlsplit(origin)
            valid = (parsed.scheme in ('http', 'https') and parsed.hostname
                     and not parsed.username and not parsed.password
                     and not parsed.path and not parsed.query and not parsed.fragment
                     and '*' not in origin and not any(char.isspace() for char in origin))
            parsed.port  # Validate malformed/out-of-range port numbers.
        except ValueError:
            valid = False
        if not valid:
            raise RuntimeError('CORS_ORIGINS must be comma-separated HTTP(S) origins without paths or wildcards.')
    return list(dict.fromkeys(origins))


def load_jwt_secret(env_file: Path = ENV_FILE) -> str:
    secret = os.environ.get('JWT_SECRET_KEY')
    if secret is None:
        secret = dotenv_values(env_file, interpolate=False).get('JWT_SECRET_KEY')
    if not secret or len(secret.strip().encode('utf-8')) < 32:
        raise RuntimeError(
            'JWT_SECRET_KEY must contain at least 32 bytes. '
            'Set it in the environment or run scripts/init_local_env.py from backend.'
        )
    return secret
