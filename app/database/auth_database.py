# import sqlite3
# import json
# from datetime import datetime
# from pathlib import Path

# from app.auth.password_utils import hash_password

# DB_PATH = Path("astramind_users.db")


# def get_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


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

#     # 🔑 Create default admin if not exists
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
#                 json.dumps([123456, 123457, 123458, 123459, 123460]),
#                 datetime.utcnow().isoformat()
#             )
#         )

#         conn.commit()

#     conn.close()


# def create_user(user_id: str, password_hash: str, group_ids):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         INSERT INTO users (user_id, password_hash, group_ids, created_at)
#         VALUES (?, ?, ?, ?)
#         """,
#         (
#             user_id,
#             password_hash,
#             json.dumps(group_ids),
#             datetime.utcnow().isoformat()
#         )
#     )

#     conn.commit()
#     conn.close()


# def get_user(user_id: str):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT * FROM users WHERE user_id=?",
#         (user_id,)
#     )

#     row = cursor.fetchone()

#     conn.close()

#     if row is None:
#         return None

#     return {
#         "user_id": row["user_id"],
#         "password_hash": row["password_hash"],
#         "group_ids": json.loads(row["group_ids"])
#     }

















import sqlite3
import json
from datetime import datetime
from pathlib import Path

from app.auth.password_utils import hash_password

DB_PATH = Path("astramind_users.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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

    # Create default admin if not exists
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
                json.dumps([123456, 123457, 123458, 123459, 123460]),
                datetime.utcnow().isoformat()
            )
        )

        conn.commit()

    conn.close()


def create_user(user_id: str, password_hash: str, group_ids):

    conn = get_connection()
    cursor = conn.cursor()

    # 🔍 Check if user already exists
    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        raise ValueError("User already exists")

    cursor.execute(
        """
        INSERT INTO users (user_id, password_hash, group_ids, created_at)
        VALUES (?, ?, ?, ?)
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


def get_user(user_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "user_id": row["user_id"],
        "password_hash": row["password_hash"],
        "group_ids": json.loads(row["group_ids"])
    }