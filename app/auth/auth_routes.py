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