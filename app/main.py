# from fastapi import FastAPI
# from app.api.routes import router
# from app.auth.auth_routes import router as auth_router
# from fastapi.middleware.cors import CORSMiddleware

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

# # Main API
# app.include_router(router)

# # Authentication API
# app.include_router(auth_router)


# @app.get("/")
# def root():
#     return {"message": "AstraMind API is running successfully"}









from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.auth.auth_routes import router as auth_router


app = FastAPI(
    title="AstraMind Enterprise AI Platform",
    description="Multi-source, department-aware enterprise RAG system",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REGISTER ROUTERS
# =========================================================

# Authentication routes
app.include_router(auth_router)

# Main API routes
app.include_router(api_router)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {"message": "AstraMind API running"}