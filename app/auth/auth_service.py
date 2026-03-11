# from app.auth.password_utils import hash_password, verify_password
# from app.database.auth_database import get_user, create_user


# def authenticate_user(user_id: str, password: str):

#     user = get_user(user_id)

#     if not user:
#         return None

#     if not verify_password(password, user["password_hash"]):
#         return None

#     token = create_access_token(
#         data={
#             "user_id": user["user_id"],
#             "group_ids": user["group_ids"]
#         }
#     )

#     return token


# def register_user(user_id: str, password: str, group_ids):

#     password_hash = hash_password(password)

#     create_user(
#         user_id=user_id,
#         password_hash=password_hash,
#         group_ids=group_ids
#     )






# from datetime import datetime, timedelta
# from jose import jwt
# from passlib.context import CryptContext

# from app.database.auth_database import get_user, create_user
# from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# # ==========================================
# # PASSWORD UTILITIES
# # ==========================================

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def hash_password(password):
#     return pwd_context.hash(password)


# # ==========================================
# # JWT TOKEN CREATION
# # ==========================================

# def create_access_token(data: dict):

#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     return encoded_jwt


# # ==========================================
# # AUTHENTICATE USER
# # ==========================================

# def authenticate_user(user_id: str, password: str):

#     user = get_user(user_id)

#     if not user:
#         return None

#     if not verify_password(password, user["password_hash"]):
#         return None

#     token = create_access_token(
#         data={
#             "user_id": user["user_id"],
#             "group_ids": user["group_ids"]
#         }
#     )

#     return token


# # ==========================================
# # REGISTER USER
# # ==========================================

# def register_user(user_id: str, password: str, group_ids):

#     password_hash = hash_password(password)

#     create_user(
#         user_id=user_id,
#         password_hash=password_hash,
#         group_ids=group_ids
#     )






from passlib.context import CryptContext

from app.database.auth_database import get_user, create_user
from app.auth.jwt_handler import create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =====================================================
# PASSWORD HELPERS
# =====================================================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


# =====================================================
# LOGIN
# =====================================================

def authenticate_user(user_id: str, password: str):

    user = get_user(user_id)

    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    token = create_access_token(
        {
            "user_id": user["user_id"],
            "group_ids": user["group_ids"]
        }
    )

    return token


# =====================================================
# CREATE USER
# =====================================================

def register_user(user_id: str, password: str, group_ids):

    password_hash = hash_password(password)

    create_user(
        user_id=user_id,
        password_hash=password_hash,
        group_ids=group_ids
    )