# from app.auth.password_utils import hash_password, verify_password
# from app.database.auth_database import get_user, create_user


# def authenticate_user(user_id: str, password: str):

#     user = get_user(user_id)

#     if not user:
#         return None

#     if not verify_password(password, user["password_hash"]):
#         return None

#     return user


# def register_user(user_id: str, password: str, group_ids):

#     password_hash = hash_password(password)

#     create_user(
#         user_id=user_id,
#         password_hash=password_hash,
#         group_ids=group_ids
#     )


















from app.auth.password_utils import hash_password, verify_password
from app.database.auth_database import get_user, create_user


def authenticate_user(user_id: str, password: str):

    user = get_user(user_id)

    # 🔍 Debug logs (safe placement)
    print("DEBUG - fetched user:", user)

    if not user:
        print("DEBUG - user not found")
        return None

    is_valid = verify_password(password, user["password_hash"])

    print("DEBUG - password valid:", is_valid)

    if not is_valid:
        return None

    return user


def register_user(user_id: str, password: str, group_ids):

    password_hash = hash_password(password)

    print("DEBUG - storing hashed password:", password_hash)

    create_user(
        user_id=user_id,
        password_hash=password_hash,
        group_ids=group_ids
    )











