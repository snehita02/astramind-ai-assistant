# from fastapi import FastAPI
# from app.api.routes import router
# from app.auth.auth_routes import router as auth_router
# from fastapi.middleware.cors import CORSMiddleware

# from app.database.auth_database import initialize_database

# app = FastAPI(
#     title="AstraMind Enterprise AI Platform",
#     description="Enterprise RAG Knowledge Assistant",
#     version="1.0.0"
# )


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# initialize_database()

# app.include_router(router)
# app.include_router(auth_router)


# @app.get("/")
# def root():
#     return {"message": "AstraMind API is running successfully"}












from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.auth.auth_routes import router as auth_router

from app.database.auth_database import initialize_database

app = FastAPI(
    title="AstraMind Enterprise AI Platform",
    version="1.0.0",
    description="Multi-source, department-aware, enterprise RAG system with guardrails and production hardening."
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Initialize database
# --------------------------------------------------

initialize_database()

# --------------------------------------------------
# Register routers
# --------------------------------------------------

app.include_router(auth_router)
app.include_router(api_router)

# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "AstraMind Enterprise AI Platform",
        "status": "running"
    }