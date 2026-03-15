# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from app.auth.jwt_handler import verify_token

# security = HTTPBearer()


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security)
# ):

#     token = credentials.credentials

#     try:

#         payload = verify_token(token)

#         user = {
#             "user_id": payload.get("user_id"),
#             "group_ids": payload.get("group_ids", [])
#         }

#         if user["user_id"] is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication token"
#             )

#         return user

#     except Exception:

#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token"
#         )









# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from app.auth.jwt_handler import verify_token


# security = HTTPBearer()


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security)
# ):

#     token = credentials.credentials

#     try:

#         payload = verify_token(token)

#         user = {
#             "user_id": payload.get("user_id"),
#             "group_ids": payload.get("group_ids", [])
#         }

#         if user["user_id"] is None:

#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication token"
#             )

#         return user

#     except Exception:

#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token"
#         )















# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from typing import Optional

# from app.auth.jwt_handler import verify_token


# # Disable automatic 401 errors
# security = HTTPBearer(auto_error=False)


# def get_current_user(
#     credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
# ):

#     # No token provided
#     if credentials is None:
#         return None

#     token = credentials.credentials

#     try:

#         payload = verify_token(token)

#         user = {
#             "user_id": payload.get("user_id"),
#             "group_ids": payload.get("group_ids", [])
#         }

#         if user["user_id"] is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication token"
#             )

#         return user

#     except Exception:

#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token"
#         )




















# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jwt, JWTError

# from app.config import SECRET_KEY, ALGORITHM


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
#         group_ids = payload.get("group_ids")

#         if user_id is None or group_ids is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token payload"
#             )

#         return {
#             "user_id": user_id,
#             "group_ids": group_ids
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
        group_ids = payload.get("group_ids")

        if user_id is None or group_ids is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return {
            "user_id": user_id,
            "group_ids": group_ids
        }

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
