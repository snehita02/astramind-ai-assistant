from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import uuid

# SQLite DB (safe + simple for now)
DATABASE_URL = "sqlite:///./chat_history.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# -------------------------------
# TABLE: Chat Sessions
# -------------------------------
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# -------------------------------
# TABLE: Messages
# -------------------------------
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user / assistant
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


# -------------------------------
# INIT DB
# -------------------------------
def initialize_chat_db():
    Base.metadata.create_all(bind=engine)


# -------------------------------
# CREATE SESSION
# -------------------------------
def create_chat_session(user_id: str):
    db = SessionLocal()
    session_id = str(uuid.uuid4())

    new_session = ChatSession(
        id=session_id,
        user_id=user_id
    )

    db.add(new_session)
    db.commit()
    db.close()

    return session_id


# -------------------------------
# SAVE MESSAGE
# -------------------------------
def save_message(session_id: str, role: str, content: str):
    db = SessionLocal()

    msg = Message(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(msg)
    db.commit()
    db.close()


# -------------------------------
# GET CHAT HISTORY
# -------------------------------
def get_chat_history(session_id: str):
    db = SessionLocal()

    messages = db.query(Message)\
        .filter(Message.session_id == session_id)\
        .order_by(Message.timestamp.asc())\
        .all()

    db.close()

    return [
        {
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp
        }
        for m in messages
    ]