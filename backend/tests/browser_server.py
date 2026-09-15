"""Isolated real application for browser_smoke.mjs; never uses the local DB."""

import os
import secrets
from pathlib import Path

import fitz
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app import database


def run():
    os.environ['JWT_SECRET_KEY'] = secrets.token_urlsafe(48)
    storage = Path(os.environ['CAREER_BROWSER_TEST_DIR'])
    database.engine = create_engine('sqlite://', poolclass=StaticPool,
                                    connect_args={'check_same_thread': False})
    database.SessionLocal.configure(bind=database.engine)
    # Import the actual app only after replacing its database configuration.
    from app.main import app
    from app.routers import resumes

    resumes.UPLOAD_DIRECTORY = storage / 'uploads'
    resumes.UPLOAD_DIRECTORY.mkdir()
    with fitz.open() as document:
        document.new_page().insert_text((72, 72), 'Python FastAPI SQL Git Docker')
        document.save(storage / 'sample.pdf')
    uvicorn.run(app, host='127.0.0.1', port=8001, log_level='error')


if __name__ == '__main__':
    run()
