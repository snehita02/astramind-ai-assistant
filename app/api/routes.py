from fastapi import APIRouter, HTTPException, Request

from app.core.llm_provider import generate_response
from app.core.embeddings import generate_embedding
from app.core.vector_store import create_collection, add_text, search_text

from app.services.document_service import ingest_text_file
from app.services.rag_service import generate_rag_answer
from app.services.tools.tool_registry import tool_registry
from app.services.ingestion_service import ingest_pdf
from app.services.url_ingestion_service import ingest_url
from app.services.repo_ingestion_service import ingest_repo

from app.config import MAX_QUERY_LENGTH
from app.schemas.response_models import RAGResponse, StandardResponse


# Versioned API Router
router = APIRouter(prefix="/api/v1")


# ============================================================
# System Health & Basic Tests
# ============================================================

@router.get("/health", response_model=StandardResponse, tags=["System"])
def health_check():
    """
    Health check endpoint for monitoring systems.
    """
    return StandardResponse(
        success=True,
        message="Service is healthy",
        data=None
    )


@router.get("/test-llm", tags=["System"])
def test_llm():
    """
    Test LLM connectivity.
    """
    answer = generate_response("Explain what a vector database is in simple terms.")
    return {"response": answer}


@router.get("/test-embedding", tags=["System"])
def test_embedding():
    """
    Test embedding generation.
    """
    vector = generate_embedding("This is a test sentence for AstraMind.")
    return {"vector_length": len(vector)}


# ============================================================
# Vector Store Setup & Debug
# ============================================================

@router.get("/init-collection", tags=["Vector Store"])
def init_collection():
    """
    Initialize vector database collection.
    """
    create_collection()
    return {"status": "Collection created successfully"}


# @router.get("/add-sample", tags=["Vector Store"])
# def add_sample():
#     """
#     Add sample records to vector store.
#     """
#     add_text("AstraMind is an enterprise AI assistant.", 1)
#     add_text("Vector databases store embeddings for similarity search.", 2)
#     return {"status": "Sample data added"}
@router.get("/add-sample", tags=["Vector Store"])
def add_sample():
    """
    Add sample records to vector store.
    """

    add_text(
        text="AstraMind is an enterprise AI assistant.",
        doc_id=1,
        metadata={
            "department": "general",
            "source": "sample",
            "type": "sample"
        }
    )

    add_text(
        text="Vector databases store embeddings for similarity search.",
        doc_id=2,
        metadata={
            "department": "general",
            "source": "sample",
            "type": "sample"
        }
    )

    return {"status": "Sample data added"}


@router.get("/search", tags=["Vector Store"])
def search(query: str):
    """
    Perform similarity search in vector store.
    """
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    results = search_text(query)
    return {"results": results}


# ============================================================
# Text Ingestion
# ============================================================

@router.get("/ingest-text", tags=["Ingestion"])
def ingest_text(file_path: str):
    """
    Ingest plain text file into vector store.
    """
    if not file_path.strip():
        raise HTTPException(status_code=400, detail="file_path required.")

    chunk_count = ingest_text_file(file_path)
    return {"chunks_stored": chunk_count}


# ============================================================
# RAG Endpoint (Production Hardened)
# ============================================================

@router.get("/ask", response_model=RAGResponse, tags=["RAG"])
def ask_question(
    request: Request,
    query: str,
    department: str,
    session_id: str = "default"
):
    """
    Enterprise RAG endpoint.
    Performs guarded retrieval-augmented generation.
    """

    # 🔐 Step 20 — Empty validation
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if not department.strip():
        raise HTTPException(status_code=400, detail="Department cannot be empty.")

    # 🔐 Step 19 — Query length validation
    if len(query) > MAX_QUERY_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="Query exceeds maximum allowed length."
        )

    # 🔐 Step 21.6 — Rate limiting placeholder
    # Future improvement:
    # - Track IP via request.client.host
    # - Apply per-minute request cap
    # - Integrate Redis-based limiter in production

    response = generate_rag_answer(
        query=query,
        department=department,
        session_id=session_id
    )

    return response


# ============================================================
# Tooling
# ============================================================

@router.get("/calculate", tags=["Tools"])
def calculate(expression: str):
    """
    Calculator tool endpoint.
    """
    if not expression.strip():
        raise HTTPException(status_code=400, detail="Expression cannot be empty.")

    tool = tool_registry.get_tool("calculator")
    result = tool.run(expression)
    return {"expression": expression, "result": result}


# ============================================================
# Admin Ingestion Routes
# ============================================================

@router.get("/admin/ingest-pdf", tags=["Admin"])
def admin_ingest_pdf(file_path: str, department: str = "general"):
    """
    Ingest PDF document into a specific department.
    """
    if not file_path.strip():
        raise HTTPException(status_code=400, detail="file_path required.")

    if not department.strip():
        raise HTTPException(status_code=400, detail="Department cannot be empty.")

    return ingest_pdf(file_path=file_path, department=department)


@router.get("/admin/ingest-url", tags=["Admin"])
def admin_ingest_url(url: str, department: str = "general"):
    """
    Ingest webpage content into a department.
    """
    if not url.strip():
        raise HTTPException(status_code=400, detail="URL required.")

    if not department.strip():
        raise HTTPException(status_code=400, detail="Department cannot be empty.")

    return ingest_url(url=url, department=department)


@router.get("/admin/ingest-repo", tags=["Admin"])
def admin_ingest_repo(repo_url: str, department: str = "general"):
    """
    Ingest GitHub repository into a department.
    """
    if not repo_url.strip():
        raise HTTPException(status_code=400, detail="repo_url required.")

    if not department.strip():
        raise HTTPException(status_code=400, detail="Department cannot be empty.")

    return ingest_repo(repo_url=repo_url, department=department)