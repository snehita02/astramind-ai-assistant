# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.routes import router as api_router
# from app.auth.auth_routes import router as auth_router


# from app.database.auth_database import initialize_database


# app = FastAPI(
#     title="AstraMind Enterprise AI Platform",
#     version="1.0.0"
# )


# # --------------------------------------------------
# # CORS
# # --------------------------------------------------

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # --------------------------------------------------
# # Startup
# # --------------------------------------------------

# @app.on_event("startup")
# def startup_event():
#     initialize_database()


# # --------------------------------------------------
# # Routers
# # --------------------------------------------------

# app.include_router(auth_router)
# app.include_router(api_router)


# # --------------------------------------------------
# # Root endpoint
# # --------------------------------------------------

# @app.get("/")
# def root():
#     return {"message": "AstraMind API running"}


# @app.get("/health")
# def health():
#     return {"status": "ok"}











# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.routes import router as api_router
# from app.auth.auth_routes import router as auth_router
# from app.database.auth_database import initialize_database


# app = FastAPI(
#     title="AstraMind Enterprise AI Platform",
#     version="1.0.0"
# )


# # --------------------------------------------------
# # CORS
# # --------------------------------------------------

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # --------------------------------------------------
# # Startup
# # --------------------------------------------------

# @app.on_event("startup")
# def startup_event():
#     initialize_database()


# # --------------------------------------------------
# # Routers
# # --------------------------------------------------

# app.include_router(auth_router)
# app.include_router(api_router)


# # --------------------------------------------------
# # Root endpoint
# # --------------------------------------------------

# @app.get("/")
# def root():
#     return {"message": "AstraMind API running"}


# @app.get("/health")
# def health():
#     return {"status": "ok"}














from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.auth.auth_routes import router as auth_router
from app.database.auth_database import initialize_database

app = FastAPI(
    title="AstraMind Enterprise AI Platform",
    version="1.0.0"
)

# --------------------------------------------------
# CORS (FIXED)
# --------------------------------------------------

origins = [
    "http://localhost:3000",
    "https://astramind-frontend-git-main-snehita02s-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # ❌ NOT "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Startup
# --------------------------------------------------

@app.on_event("startup")
def startup_event():
    initialize_database()

# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(auth_router)
app.include_router(api_router)

# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {"message": "AstraMind API running"}

@app.get("/health")
def health():
    return {"status": "ok"}