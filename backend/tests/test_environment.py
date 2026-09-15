"""Test-only JWT key shared by unittest discovery modules."""
import os
import secrets

os.environ['JWT_SECRET_KEY'] = secrets.token_urlsafe(48)
