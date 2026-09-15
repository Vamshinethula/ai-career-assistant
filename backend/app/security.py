import bcrypt


def hash_password(password: str) -> str:
    encoded = password.encode('utf-8')
    if not encoded or len(encoded) > 72 or b'\x00' in encoded:
        raise ValueError('Password must be 1–72 UTF-8 bytes and contain no null characters')
    return bcrypt.hashpw(encoded, bcrypt.gensalt(rounds=12)).decode('ascii')


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    if len(plain_password) > 4096 or '\x00' in plain_password:
        return False
    try:
        # Legacy Passlib registrations truncated at 72 bytes. Preserve their login.
        encoded = plain_password.encode('utf-8')[:72]
        return bcrypt.checkpw(encoded, hashed_password.encode('ascii'))
    except (ValueError, UnicodeError):
        return False
