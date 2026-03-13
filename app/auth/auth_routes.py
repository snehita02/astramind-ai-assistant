from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from typing import List

from app.auth.auth_service import authenticate_user, register_user
from app.auth.jwt_handler import create_access_token
from app.auth.auth_dependency import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


# ------------------------------------------------------------
# Request model for creating users
# ------------------------------------------------------------

class CreateUserRequest(BaseModel):
    group_ids: List[int]


# ------------------------------------------------------------
# Login
# ------------------------------------------------------------

@router.post("/login")
def login(
    user_id: str = Form(...),
    password: str = Form(...)
):

    user = authenticate_user(user_id, password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {
            "user_id": user["user_id"],
            "group_ids": user["group_ids"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ------------------------------------------------------------
# Admin Create User
# ------------------------------------------------------------

@router.post("/admin/create-user")
def admin_create_user(
    request: CreateUserRequest,
    user_id: str,
    password: str,
    user=Depends(get_current_user)
):

    try:

        register_user(
            user_id=user_id,
            password=password,
            group_ids=request.group_ids
        )

        return {
            "message": f"user {user_id} created successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


        





















# from fastapi import APIRouter, HTTPException, Depends, Form
# from typing import List

# from app.auth.auth_service import authenticate_user, register_user
# from app.auth.jwt_handler import create_access_token
# from app.auth.auth_dependency import get_current_user

# router = APIRouter(prefix="/auth", tags=["Authentication"])


# @router.post("/login")
# def login(
#     user_id: str = Form(...),
#     password: str = Form(...)
# ):

#     user = authenticate_user(user_id, password)

#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token(
#         {
#             "user_id": user["user_id"],
#             "group_ids": user["group_ids"]
#         }
#     )

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }


# @router.post("/admin/create-user")
# def admin_create_user(
#     user_id: str,
#     password: str,
#     group_ids: list[int],
#     user=Depends(get_current_user)
# ):

#     try:

#         register_user(
#             user_id=user_id,
#             password=password,
#             group_ids=group_ids
#         )

#         return {
#             "message": f"user {user_id} created successfully"
#         }

#     except ValueError as e:

#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )
















# from fastapi import APIRouter, HTTPException, Depends, Form
# from typing import List, Optional

# from app.auth.auth_service import authenticate_user, register_user
# from app.auth.auth_dependency import get_current_user
# from app.database.auth_database import get_user


# router = APIRouter(
#     prefix="/auth",
#     tags=["Authentication"]
# )


# # ==========================================
# # LOGIN
# # ==========================================

# @router.post("/login")
# def login(
#     user_id: str = Form(...),
#     password: str = Form(...)
# ):

#     token = authenticate_user(user_id, password)

#     if not token:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials"
#         )

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }


# # ==========================================
# # CREATE USER
# # ==========================================

# @router.post("/admin/create-user")
# def create_user(
#     user_id: str = Form(...),
#     password: str = Form(...),
#     group_ids: List[int] = Form(...),
#     user: Optional[dict] = Depends(get_current_user)
# ):

#     # Check if admin already exists
#     admin_exists = get_user("admin")

#     # If admin exists → require admin privileges
#     if admin_exists:

#         if user is None:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Authentication required"
#             )

#         if 999999 not in user["group_ids"]:
#             raise HTTPException(
#                 status_code=403,
#                 detail="Admin privileges required"
#             )

#     # Create user
#     register_user(
#         user_id=user_id,
#         password=password,
#         group_ids=group_ids
#     )

#     return {
#         "message": f"user '{user_id}' created successfully"
#     }