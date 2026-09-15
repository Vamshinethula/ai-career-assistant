"""Local .env support; deployment environment variables take precedence."""
import os
from pathlib import Path

from dotenv import dotenv_values


ENV_FILE = Path(__file__).resolve().parents[1] / '.env'


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
