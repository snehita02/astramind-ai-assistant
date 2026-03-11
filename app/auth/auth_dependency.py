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




from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt_handler import verify_token


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = verify_token(token)

        user = {
            "user_id": payload.get("user_id"),
            "group_ids": payload.get("group_ids", [])
        }

        if user["user_id"] is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        return user

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )