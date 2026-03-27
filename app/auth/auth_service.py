# from app.auth.password_utils import hash_password, verify_password
# from app.database.auth_database import get_user, create_user


# def authenticate_user(user_id: str, password: str):

#     user = get_user(user_id)

#     # 🔍 Debug logs (safe placement)
#     print("DEBUG - fetched user:", user)

#     if not user:
#         print("DEBUG - user not found")
#         return None

#     is_valid = verify_password(password, user["password_hash"])

#     print("DEBUG - password valid:", is_valid)

#     if not is_valid:
#         return None

#     return user


# def register_user(user_id: str, password: str, group_ids):

#     password_hash = hash_password(password)

#     print("DEBUG - storing hashed password:", password_hash)

#     create_user(
#         user_id=user_id,
#         password_hash=password_hash,
#         group_ids=group_ids
#     )















# from datetime import datetime, timedelta
# from jose import jwt
# from passlib.context import CryptContext

# from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# # --------------------------------------------------
# # Mock User DB (Extend with role)
# # --------------------------------------------------

# fake_users_db = {
#     "user1": {
#         "user_id": "user1",
#         "password": pwd_context.hash("password"),
#         "group_ids": [123456],
#         "role": "user"
#     },
#     "admin1": {
#         "user_id": "admin1",
#         "password": pwd_context.hash("admin"),
#         "group_ids": [123456, 123457, 123458],
#         "role": "admin"
#     }
# }


# # --------------------------------------------------
# # Verify Password
# # --------------------------------------------------

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# # --------------------------------------------------
# # Authenticate User
# # --------------------------------------------------

# def authenticate_user(user_id: str, password: str):
#     user = fake_users_db.get(user_id)

#     if not user:
#         return None

#     if not verify_password(password, user["password"]):
#         return None

#     return user


# # --------------------------------------------------
# # Create JWT Token (UPDATED WITH ROLE)
# # --------------------------------------------------

# def create_access_token(data: dict, expires_delta: timedelta = None):

#     to_encode = data.copy()

#     expire = datetime.utcnow() + (
#         expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     )

#     to_encode.update({
#         "exp": expire
#     })

#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# # --------------------------------------------------
# # Login Helper
# # --------------------------------------------------

# def login_user(user_id: str, password: str):

#     user = authenticate_user(user_id, password)

#     if not user:
#         return None

#     token_data = {
#         "user_id": user["user_id"],
#         "group_ids": user["group_ids"],
#         "role": user["role"]  # ⭐ NEW
#     }

#     access_token = create_access_token(token_data)

#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#     }

















from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# 🔥 DB IMPORTS (REAL SOURCE OF TRUTH)
from app.database.auth_database import get_user, create_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --------------------------------------------------
# Password Hashing
# --------------------------------------------------

def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# --------------------------------------------------
# Authenticate User (🔥 DB BASED)
# --------------------------------------------------

def authenticate_user(user_id: str, password: str):

    user = get_user(user_id)

    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return user


# --------------------------------------------------
# Register User (🔥 DB BASED)
# --------------------------------------------------

def register_user(user_id: str, password: str, group_ids: list, role: str = "user"):

    existing_user = get_user(user_id)

    if existing_user:
        raise ValueError("User already exists")

    password_hash = get_password_hash(password)

    create_user(
        user_id=user_id,
        password_hash=password_hash,
        group_ids=group_ids,
        role=role
    )


# --------------------------------------------------
# Create JWT Token
# --------------------------------------------------

def create_access_token(data: dict, expires_delta: timedelta = None):

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --------------------------------------------------
# Login Helper
# --------------------------------------------------

def login_user(user_id: str, password: str):

    user = authenticate_user(user_id, password)

    if not user:
        return None

    token_data = {
        "user_id": user["user_id"],
        "group_ids": user.get("group_ids", []),
        "role": user.get("role", "user")
    }

    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }