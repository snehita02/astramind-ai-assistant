import sqlite3
import json
from datetime import datetime
from pathlib import Path

from app.auth.password_utils import hash_password


# --------------------------------------------------
# Database Location (Render-safe)
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "astramind_users.db"


# --------------------------------------------------
# Connection
# --------------------------------------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------------------------------
# Initialize DB
# --------------------------------------------------

# def initialize_database():

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id TEXT PRIMARY KEY,
#         password_hash TEXT NOT NULL,
#         group_ids TEXT NOT NULL,
#         created_at TEXT NOT NULL
#     )
#     """)

#     conn.commit()

#     # Create admin user if missing
#     cursor.execute("SELECT * FROM users WHERE user_id='admin'")
#     admin = cursor.fetchone()

#     if not admin:

#         password_hash = hash_password("admin123")

#         cursor.execute(
#             """
#             INSERT INTO users (user_id, password_hash, group_ids, created_at)
#             VALUES (?, ?, ?, ?)
#             """,
#             (
#                 "admin",
#                 password_hash,
#                 json.dumps([123456,123457,123458,123459,123460]),
#                 datetime.utcnow().isoformat()
#             )
#         )

#         conn.commit()

#     conn.close()
def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL,
        group_ids TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()

    # 🔥 TEMP FIX: Reset users (ONLY RUN ONCE)
    cursor.execute("DELETE FROM users")
    conn.commit()

    # Create admin user if missing
    cursor.execute("SELECT * FROM users WHERE user_id='admin'")
    admin = cursor.fetchone()

    if not admin:

        password_hash = hash_password("admin123")

        cursor.execute(
            """
            INSERT INTO users (user_id, password_hash, group_ids, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                "admin",
                password_hash,
                json.dumps([123456,123457,123458,123459,123460]),
                datetime.utcnow().isoformat()
            )
        )

        conn.commit()

    conn.close()


# --------------------------------------------------
# Create User
# --------------------------------------------------

def create_user(user_id: str, password_hash: str, group_ids):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    if cursor.fetchone():
        conn.close()
        raise ValueError("User already exists")

    cursor.execute(
        """
        INSERT INTO users (user_id,password_hash,group_ids,created_at)
        VALUES (?,?,?,?)
        """,
        (
            user_id,
            password_hash,
            json.dumps(group_ids),
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()


# --------------------------------------------------
# Get User
# --------------------------------------------------

def get_user(user_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "user_id": row["user_id"],
        "password_hash": row["password_hash"],
        "group_ids": json.loads(row["group_ids"])
    }