# from fastapi import APIRouter, HTTPException, Depends, Form
# from pydantic import BaseModel
# from typing import List

# from app.auth.auth_service import authenticate_user, register_user
# from app.auth.jwt_handler import create_access_token
# from app.auth.auth_dependency import get_current_user


# router = APIRouter(prefix="/auth", tags=["Authentication"])


# # ------------------------------------------------------------
# # Request model for creating users
# # ------------------------------------------------------------

# class CreateUserRequest(BaseModel):
#     group_ids: List[int]


# # ------------------------------------------------------------
# # Login
# # ------------------------------------------------------------

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


# # ------------------------------------------------------------
# # Admin Create User
# # ------------------------------------------------------------

# @router.post("/admin/create-user")
# def admin_create_user(
#     request: CreateUserRequest,
#     user_id: str,
#     password: str,
#     user=Depends(get_current_user)
# ):

#     try:

#         register_user(
#             user_id=user_id,
#             password=password,
#             group_ids=request.group_ids
#         )

#         return {
#             "message": f"user {user_id} created successfully"
#         }

#     except ValueError as e:

#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )
















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
    role: str = "user"   # ⭐ NEW (default safe)


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
            "group_ids": user.get("group_ids", []),
            "role": user.get("role", "user")   # ⭐ NEW
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

    # 🔒 Step 38 (light check, full enforcement in Step 39)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    try:

        register_user(
            user_id=user_id,
            password=password,
            group_ids=request.group_ids,
            role=request.role   # ⭐ NEW
        )

        return {
            "message": f"user {user_id} created successfully",
            "role": request.role
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )























# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel
# from typing import List

# from app.auth.auth_service import authenticate_user, register_user
# from app.auth.jwt_handler import create_access_token
# from app.auth.auth_dependency import get_current_user

# router = APIRouter(prefix="/auth", tags=["Authentication"])


# # ------------------------------------------------------------
# # Request Models
# # ------------------------------------------------------------

# class LoginRequest(BaseModel):
#     user_id: str
#     password: str


# class CreateUserRequest(BaseModel):
#     user_id: str
#     password: str
#     group_ids: List[int]


# # ------------------------------------------------------------
# # Login (FIXED - JSON)
# # ------------------------------------------------------------

# @router.post("/login")
# def login(request: LoginRequest):

#     user = authenticate_user(request.user_id, request.password)

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


# # ------------------------------------------------------------
# # Admin Create User (FIXED - JSON)
# # ------------------------------------------------------------

# @router.post("/admin/create-user")
# def admin_create_user(
#     request: CreateUserRequest,
#     user=Depends(get_current_user)
# ):

#     try:

#         register_user(
#             user_id=request.user_id,
#             password=request.password,
#             group_ids=request.group_ids
#         )

#         return {
#             "message": f"user {request.user_id} created successfully"
#         }

#     except ValueError as e:

#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )