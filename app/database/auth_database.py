# import os
# import psycopg2
# from psycopg2.extras import RealDictCursor

# DATABASE_URL = os.getenv("DATABASE_URL")

# def get_connection():
#     return psycopg2.connect(DATABASE_URL)


# def create_users_table():
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id TEXT PRIMARY KEY,
#         password_hash TEXT NOT NULL,
#         group_ids INTEGER[]
#     )
#     """)

#     conn.commit()
#     cur.close()
#     conn.close()


# def get_user(user_id: str):
#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)

#     cur.execute(
#         "SELECT * FROM users WHERE user_id = %s",
#         (user_id,)
#     )

#     user = cur.fetchone()

#     cur.close()
#     conn.close()

#     return user


# def create_user(user_id: str, password_hash: str, group_ids):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#     INSERT INTO users (user_id, password_hash, group_ids)
#     VALUES (%s, %s, %s)
#     ON CONFLICT (user_id) DO NOTHING
#     """, (user_id, password_hash, group_ids))

#     conn.commit()
#     cur.close()
#     conn.close()



















# import os
# import psycopg2
# from psycopg2.extras import RealDictCursor


# # --------------------------------------------------
# # DATABASE URL FIX (IMPORTANT)
# # --------------------------------------------------

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise Exception("DATABASE_URL not set")

# # Fix for Render postgres:// → postgresql://
# if DATABASE_URL.startswith("postgres://"):
#     DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


# # --------------------------------------------------
# # CONNECTION
# # --------------------------------------------------

# def get_connection():
#     return psycopg2.connect(DATABASE_URL)


# # --------------------------------------------------
# # INITIALIZE DATABASE (SAFE)
# # --------------------------------------------------

# def initialize_database():
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id TEXT PRIMARY KEY,
#         password_hash TEXT NOT NULL,
#         group_ids INTEGER[]
#     )
#     """)

#     conn.commit()
#     cur.close()
#     conn.close()


# # --------------------------------------------------
# # GET USER
# # --------------------------------------------------

# def get_user(user_id: str):
#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)

#     cur.execute(
#         "SELECT * FROM users WHERE user_id = %s",
#         (user_id,)
#     )

#     user = cur.fetchone()

#     cur.close()
#     conn.close()

#     return user


# # --------------------------------------------------
# # CREATE USER
# # --------------------------------------------------

# def create_user(user_id: str, password_hash: str, group_ids):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#     INSERT INTO users (user_id, password_hash, group_ids)
#     VALUES (%s, %s, %s)
#     ON CONFLICT (user_id) DO NOTHING
#     """, (user_id, password_hash, group_ids))

#     conn.commit()
#     cur.close()
#     conn.close()



















# import os
# import psycopg2
# from psycopg2.extras import RealDictCursor

# from app.auth.password_utils import hash_password

# DATABASE_URL = os.getenv("DATABASE_URL")


# def get_connection():
#     return psycopg2.connect(DATABASE_URL)


# # --------------------------------------------------
# # Initialize DB + create admin user
# # --------------------------------------------------

# def initialize_database():
#     conn = get_connection()
#     cur = conn.cursor()

#     # Create table
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id TEXT PRIMARY KEY,
#         password_hash TEXT NOT NULL,
#         group_ids INTEGER[]
#     )
#     """)

#     # Create default admin if not exists
#     cur.execute("SELECT * FROM users WHERE user_id = 'admin'")
#     admin = cur.fetchone()

#     if not admin:
#         print("⚡ Creating default admin user...")

#         password_hash = hash_password("admin123")

#         cur.execute("""
#         INSERT INTO users (user_id, password_hash, group_ids)
#         VALUES (%s, %s, %s)
#         """, ("admin", password_hash, [999999]))

#     conn.commit()
#     cur.close()
#     conn.close()


# # --------------------------------------------------
# # Get user
# # --------------------------------------------------

# def get_user(user_id: str):
#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)

#     cur.execute(
#         "SELECT * FROM users WHERE user_id = %s",
#         (user_id,)
#     )

#     user = cur.fetchone()

#     cur.close()
#     conn.close()

#     return user


# # --------------------------------------------------
# # Create user
# # --------------------------------------------------

# def create_user(user_id: str, password_hash: str, group_ids):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#     INSERT INTO users (user_id, password_hash, group_ids)
#     VALUES (%s, %s, %s)
#     ON CONFLICT (user_id) DO NOTHING
#     """, (user_id, password_hash, group_ids))

#     conn.commit()
#     cur.close()
#     conn.close()













from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./auth.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    password_hash = Column(String)
    group_ids = Column(JSON)
    role = Column(String, default="user")   # ⭐ NEW


def initialize_database():
    Base.metadata.create_all(bind=engine)


# ------------------------------------------------------------
# DB Operations
# ------------------------------------------------------------

def create_user(user_id: str, password_hash: str, group_ids: list, role: str = "user"):

    db = SessionLocal()

    user = User(
        user_id=user_id,
        password_hash=password_hash,
        group_ids=group_ids,
        role=role
    )

    db.add(user)
    db.commit()
    db.close()


def get_user(user_id: str):

    db = SessionLocal()

    user = db.query(User).filter(User.user_id == user_id).first()

    db.close()

    if not user:
        return None

    return {
        "user_id": user.user_id,
        "password_hash": user.password_hash,
        "group_ids": user.group_ids,
        "role": user.role   # ⭐ NEW
    }