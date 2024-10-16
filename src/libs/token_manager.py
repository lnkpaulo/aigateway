# # token_manager.py
import sqlite3
import secrets
from datetime import datetime, timezone
import uuid


from models import Settings
settings = Settings()

class TokenManager:
    def __init__(self, db_file=f"{settings.TOKEN_DB_PATH}"):
        self.db_file = db_file
        self.create_tokens_table()

    def create_tokens_table(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    user TEXT NOT NULL,
                    api_name TEXT NOT NULL,
                    token TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT,
                    UNIQUE(user, api_name),
                    UNIQUE(user_id)
                )
            ''')
            conn.commit()

    def generate_token(self, user: str, api_name: str, expires_at: str = None):
        token = secrets.token_hex(32)  # Generate a secure, unique token
        user_id = str(uuid.uuid4())  # Generate a unique user_id using UUID
        created_at = datetime.now(timezone.utc).isoformat()  # Get current UTC time in ISO 8601 format
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO tokens (user_id, user, api_name, token, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)',
                    (user_id, user, api_name, token, created_at, expires_at)
                )
                conn.commit()
                return token
            except sqlite3.IntegrityError:
                raise ValueError(f"User {user} with API {api_name} already exists.")

    def validate_token(self, provided_token: str) -> bool:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM tokens WHERE token = ?', (provided_token,))
            return cursor.fetchone() is not None

    def get_user_by_token(self, provided_token: str) -> str:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user FROM tokens WHERE token = ?', (provided_token,))
            row = cursor.fetchone()
            return row[0] if row else None

    def list_users(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_id, user, api_name, created_at, expires_at FROM tokens')
            return cursor.fetchall()


    def revoke_token(self, user: str, api_name: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tokens WHERE user = ? AND api_name = ?', (user, api_name))
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError(f"No such pair: User {user} with API {api_name}")
