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
#     user_id: str = Form(...),
#     password: str = Form(...),
#     group_ids: List[int] = Form(...),
#     current_user=Depends(get_current_user)
# ):

#     if current_user["user_id"] != "admin":
#         raise HTTPException(
#             status_code=403,
#             detail="Only admin can create users"
#         )

#     register_user(
#         user_id=user_id,
#         password=password,
#         group_ids=group_ids
#     )

#     return {
#         "message": f"user {user_id} created successfully"
#     }






# from fastapi import APIRouter, HTTPException, Depends, Form
# from typing import List

# from app.auth.auth_service import authenticate_user, register_user
# from app.auth.auth_dependency import get_current_user

# router = APIRouter(prefix="/auth", tags=["Authentication"])


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
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }


# # ==========================================
# # ADMIN CREATE USER
# # ==========================================

# @router.post("/admin/create-user")
# def create_user(
#     user_id: str = Form(...),
#     password: str = Form(...),
#     group_ids: List[int] = Form(...),
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

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )







from fastapi import APIRouter, HTTPException, Depends, Form
from typing import List

from app.auth.auth_service import authenticate_user, register_user
from app.auth.auth_dependency import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =====================================================
# LOGIN
# =====================================================

@router.post("/login")
def login(
    user_id: str = Form(...),
    password: str = Form(...)
):

    token = authenticate_user(user_id, password)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =====================================================
# ADMIN CREATE USER
# =====================================================

@router.post("/admin/create-user")
def create_user(
    user_id: str = Form(...),
    password: str = Form(...),
    group_ids: List[int] = Form(...),
    user=Depends(get_current_user)
):

    try:

        register_user(
            user_id=user_id,
            password=password,
            group_ids=group_ids
        )

        return {
            "message": f"user '{user_id}' created successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )