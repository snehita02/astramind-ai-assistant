from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AstraMind Enterprise AI Platform",
    description="Multi-source, department-aware, enterprise RAG system with guardrails and production hardening.",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "AstraMind API is running successfully"}