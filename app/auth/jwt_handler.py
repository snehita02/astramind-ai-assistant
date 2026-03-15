# from datetime import datetime, timedelta
# from jose import jwt

# SECRET_KEY = "astramind_super_secret_key"
# ALGORITHM = "HS256"

# ACCESS_TOKEN_EXPIRE_MINUTES = 120


# def create_access_token(data: dict):

#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     return encoded_jwt


# def verify_token(token: str):

#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#     return payload








# from datetime import datetime, timedelta
# from jose import jwt, JWTError

# SECRET_KEY = "astramind_super_secret_key"
# ALGORITHM = "HS256"

# ACCESS_TOKEN_EXPIRE_MINUTES = 120


# def create_access_token(data: dict):

#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     return encoded_jwt


# def verify_token(token: str):

#     try:

#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         return payload

#     except JWTError:

#         raise Exception("Token verification failed")












# from datetime import datetime, timedelta
# from jose import jwt, JWTError


# SECRET_KEY = "astramind_super_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 120


# def create_access_token(data: dict):

#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(
#         minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#     )

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM
#     )

#     return encoded_jwt


# def verify_token(token: str):

#     try:

#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )

#         return payload

#     except JWTError:

#         raise Exception("Token verification failed")







# from datetime import datetime, timedelta
# from jose import jwt, JWTError


# SECRET_KEY = "astramind_super_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 120


# # =====================================================
# # CREATE TOKEN
# # =====================================================

# def create_access_token(data: dict):

#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(
#         minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#     )

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM
#     )

#     return encoded_jwt


# # =====================================================
# # VERIFY TOKEN
# # =====================================================

# def verify_token(token: str):

#     try:

#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )

#         return payload

#     except JWTError:
#         raise Exception("Token verification failed")


















# from datetime import datetime, timedelta
# from jose import jwt, JWTError

# SECRET_KEY = "astramind_super_secret_key"
# ALGORITHM = "HS256"

# # Token valid for 8 hours
# ACCESS_TOKEN_EXPIRE_MINUTES = 480


# def create_access_token(data: dict):

#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(
#         minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#     )

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM
#     )

#     return encoded_jwt


# def verify_token(token: str):

#     try:

#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )

#         return payload

#     except JWTError:

#         raise Exception("Token verification failed")














from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# --------------------------------------------------
# Create JWT Token
# --------------------------------------------------

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# --------------------------------------------------
# Verify Token
# --------------------------------------------------

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise Exception("Token verification failed")
