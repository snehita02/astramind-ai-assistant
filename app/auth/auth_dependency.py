# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jwt, JWTError

# from app.config import SECRET_KEY, ALGORITHM
# from app.database.auth_database import get_user  # 🔥 NEW


# security = HTTPBearer()


# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

#     token = credentials.credentials

#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Authentication token missing"
#         )

#     try:

#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )

#         user_id = payload.get("user_id")

#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token payload"
#             )

#         # 🔥🔥🔥 CRITICAL FIX
#         # Always fetch latest user from DB
#         user = get_user(user_id)

#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="User not found"
#             )

#         return {
#             "user_id": user["user_id"],
#             "group_ids": user["group_ids"]   # ✅ ALWAYS CORRECT
#         }

#     except JWTError:

#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication token"
#         )






















from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.config import SECRET_KEY, ALGORITHM
from app.database.auth_database import get_user  # DB source of truth


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token missing"
        )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        # 🔥 Always fetch latest user from DB (SOURCE OF TRUTH)
        user = get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return {
            "user_id": user["user_id"],
            "group_ids": user.get("group_ids", []),
            "role": user.get("role", "user")   # ⭐ NEW (SAFE DEFAULT)
        }

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )