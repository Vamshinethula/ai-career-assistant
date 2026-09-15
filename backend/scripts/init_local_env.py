"""Create a private local signing key without printing it or overwriting files."""
import secrets
from pathlib import Path


def main():
    target = Path(__file__).resolve().parents[1] / '.env'
    try:
        with target.open('x', encoding='utf-8') as file:
            file.write('JWT_SECRET_KEY=' + secrets.token_urlsafe(48) + '\n')
    except FileExistsError:
        print('backend/.env already exists; left unchanged.')
    else:
        print('Created backend/.env with a random signing key. Keep this file private.')


if __name__ == '__main__':
    main()
