# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user
# from app.auth.permissions import (
#     resolve_departments,
#     get_poc_message,
#     is_admin
# )

# from app.config import MAX_QUERY_LENGTH
# from app.schemas.response_models import RAGResponse, StandardResponse


# router = APIRouter(prefix="/api/v1")


# # ============================================================
# # DEPARTMENT DETECTION
# # ============================================================

# def detect_department(query: str):

#     q = query.lower()

#     if "leave" in q or "benefit" in q or "holiday" in q:
#         return "hr"

#     if "travel" in q or "reimbursement" in q:
#         return "sales"

#     return "general"


# # ============================================================
# # SYSTEM HEALTH
# # ============================================================

# @router.get("/health", response_model=StandardResponse, tags=["System"])
# def health_check():

#     return StandardResponse(
#         success=True,
#         message="Service is healthy",
#         data=None
#     )


# # ============================================================
# # LLM TEST
# # ============================================================

# @router.get("/test-llm", tags=["System"])
# def test_llm():

#     answer = generate_response(
#         "Explain what a vector database is in simple terms."
#     )

#     return {"response": answer}


# @router.get("/test-embedding", tags=["System"])
# def test_embedding():

#     vector = generate_embedding(
#         "This is a test sentence for AstraMind."
#     )

#     return {"vector_length": len(vector)}


# # ============================================================
# # VECTOR STORE
# # ============================================================

# @router.get("/init-collection", tags=["Vector Store"])
# def init_collection():

#     create_collection()

#     return {"status": "Collection created successfully"}


# @router.get("/add-sample", tags=["Vector Store"])
# def add_sample():

#     add_text(
#         text="AstraMind is an enterprise AI assistant.",
#         doc_id=1,
#         metadata={
#             "department": "general",
#             "source": "sample",
#             "type": "sample"
#         }
#     )

#     add_text(
#         text="Vector databases store embeddings for similarity search.",
#         doc_id=2,
#         metadata={
#             "department": "general",
#             "source": "sample",
#             "type": "sample"
#         }
#     )

#     return {"status": "Sample data added"}


# @router.get("/search", tags=["Vector Store"])
# def search(query: str):

#     if not query.strip():

#         raise HTTPException(
#             status_code=400,
#             detail="Query cannot be empty."
#         )

#     results = search_text(query)

#     return {"results": results}


# # ============================================================
# # RAG ENDPOINT
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = "default",
#     user=Depends(get_current_user)
# ):

#     if not query.strip():

#         raise HTTPException(
#             status_code=400,
#             detail="Query cannot be empty."
#         )

#     if len(query) > MAX_QUERY_LENGTH:

#         raise HTTPException(
#             status_code=400,
#             detail="Query exceeds maximum allowed length."
#         )

#     group_ids = user["group_ids"]

#     # Detect department automatically
#     department = detect_department(query)

#     # Admin bypass
#     if is_admin(group_ids):

#         return generate_rag_answer(
#             query=query,
#             department=department,
#             session_id=session_id
#         )

#     # Resolve user allowed departments
#     allowed_departments = resolve_departments(group_ids)

#     if department not in allowed_departments:

#         poc_message = get_poc_message(department)

#         return {
#             "question": query,
#             "answer": poc_message,
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Access restricted",
#             "context_used": [],
#             "session_id": session_id
#         }

#     return generate_rag_answer(
#         query=query,
#         department=department,
#         session_id=session_id
#     )


# # ============================================================
# # TOOLS
# # ============================================================

# @router.get("/calculate", tags=["Tools"])
# def calculate(expression: str):

#     tool = tool_registry.get_tool("calculator")

#     result = tool.run(expression)

#     return {
#         "expression": expression,
#         "result": result
#     }


# # ============================================================
# # ADMIN INGESTION
# # ============================================================

# @router.get("/admin/ingest-pdf", tags=["Admin"])
# def admin_ingest_pdf(
#     file_path: str,
#     department: str,
#     user=Depends(get_current_user)
# ):

#     return ingest_pdf(
#         file_path=file_path,
#         department=department
#     )


# @router.get("/admin/ingest-url", tags=["Admin"])
# def admin_ingest_url(
#     url: str,
#     department: str,
#     user=Depends(get_current_user)
# ):

#     return ingest_url(
#         url=url,
#         department=department
#     )


# @router.get("/admin/ingest-repo", tags=["Admin"])
# def admin_ingest_repo(
#     repo_url: str,
#     department: str,
#     user=Depends(get_current_user)
# ):

#     return ingest_repo(
#         repo_url=repo_url,
#         department=department
#     )


















# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user
# from app.auth.permissions import resolve_departments

# from app.config import MAX_QUERY_LENGTH
# from app.schemas.response_models import RAGResponse, StandardResponse


# router = APIRouter(prefix="/api/v1")


# # ============================================================
# # System Health
# # ============================================================

# @router.get("/health", response_model=StandardResponse, tags=["System"])
# def health_check():

#     return StandardResponse(
#         success=True,
#         message="Service is healthy",
#         data=None
#     )


# # ============================================================
# # LLM Tests
# # ============================================================

# @router.get("/test-llm", tags=["System"])
# def test_llm():

#     answer = generate_response("Explain what a vector database is in simple terms.")

#     return {"response": answer}


# @router.get("/test-embedding", tags=["System"])
# def test_embedding():

#     vector = generate_embedding("This is a test sentence for AstraMind.")

#     return {"vector_length": len(vector)}


# # ============================================================
# # Vector Store
# # ============================================================

# @router.get("/init-collection", tags=["Vector Store"])
# def init_collection():

#     create_collection()

#     return {"status": "Collection created successfully"}


# @router.get("/add-sample", tags=["Vector Store"])
# def add_sample():

#     add_text(
#         text="AstraMind is an enterprise AI assistant.",
#         doc_id=1,
#         metadata={
#             "department": "general",
#             "source": "sample",
#             "type": "sample"
#         }
#     )

#     add_text(
#         text="Vector databases store embeddings for similarity search.",
#         doc_id=2,
#         metadata={
#             "department": "general",
#             "source": "sample",
#             "type": "sample"
#         }
#     )

#     return {"status": "Sample data added"}


# @router.get("/search", tags=["Vector Store"])
# def search(query: str):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     results = search_text(query)

#     return {"results": results}


# # ============================================================
# # RAG Endpoint (PROTECTED + PERMISSION BASED)
# # ============================================================

# # @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# # def ask_question(
# #     request: Request,
# #     query: str,
# #     session_id: str = "default",
# #     user=Depends(get_current_user)
# # ):

# #     if not query.strip():
# #         raise HTTPException(status_code=400, detail="Query cannot be empty.")

# #     if len(query) > MAX_QUERY_LENGTH:
# #         raise HTTPException(
# #             status_code=400,
# #             detail="Query exceeds maximum allowed length."
# #         )

# #     # ------------------------------------------
# #     # Resolve allowed departments for this user
# #     # ------------------------------------------

# #     from app.auth.permissions import resolve_departments

# #     allowed_departments = resolve_departments(user["group_ids"])

# #     # ------------------------------------------
# #     # Call RAG pipeline
# #     # ------------------------------------------

# #     response = generate_rag_answer(
# #         query=query,
# #         session_id=session_id,
# #         departments=allowed_departments
# #     )

# #     return response



# @router.get("/ask", response_model=RAGResponse)
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = "default",
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication required")

#     try:

#         from app.auth.permissions import resolve_departments
#         from app.services.rag_service import generate_rag_answer

#         allowed_departments = resolve_departments(user["group_ids"])

#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             departments=allowed_departments
#         )

#         return response

#     except Exception as e:

#         logger.error(f"RAG pipeline failed: {str(e)}")

#         raise HTTPException(
#             status_code=500,
#             detail="Internal RAG pipeline error"
#         )





# # ============================================================
# # Tooling
# # ============================================================

# @router.get("/calculate", tags=["Tools"])
# def calculate(expression: str):

#     if not expression.strip():
#         raise HTTPException(status_code=400, detail="Expression cannot be empty.")

#     tool = tool_registry.get_tool("calculator")

#     result = tool.run(expression)

#     return {"expression": expression, "result": result}


# # ============================================================
# # Admin Ingestion (PROTECTED)
# # ============================================================

# @router.get("/admin/ingest-pdf", tags=["Admin"])
# def admin_ingest_pdf(
#     file_path: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):

#     if not file_path.strip():
#         raise HTTPException(status_code=400, detail="file_path required.")

#     if not department.strip():
#         raise HTTPException(status_code=400, detail="Department cannot be empty.")

#     return ingest_pdf(file_path=file_path, department=department)


# @router.get("/admin/ingest-url", tags=["Admin"])
# def admin_ingest_url(
#     url: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):

#     if not url.strip():
#         raise HTTPException(status_code=400, detail="URL required.")

#     if not department.strip():
#         raise HTTPException(status_code=400, detail="Department cannot be empty.")

#     return ingest_url(url=url, department=department)


# @router.get("/admin/ingest-repo", tags=["Admin"])
# def admin_ingest_repo(
#     repo_url: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):

#     if not repo_url.strip():
#         raise HTTPException(status_code=400, detail="repo_url required.")

#     if not department.strip():
#         raise HTTPException(status_code=400, detail="Department cannot be empty.")

#     return ingest_repo(repo_url=repo_url, department=department)












































from fastapi import APIRouter, HTTPException, Request, Depends

from app.core.llm_provider import generate_response
from app.core.embeddings import generate_embedding
from app.core.vector_store import create_collection, add_text, search_text
from app.core.logger import logger

from app.services.document_service import ingest_text_file
from app.services.rag_service import generate_rag_answer
from app.services.tools.tool_registry import tool_registry
from app.services.ingestion_service import ingest_pdf
from app.services.url_ingestion_service import ingest_url
from app.services.repo_ingestion_service import ingest_repo

from app.auth.auth_dependency import get_current_user

from app.config import MAX_QUERY_LENGTH
from app.schemas.response_models import RAGResponse, StandardResponse


router = APIRouter(prefix="/api/v1")


# ============================================================
# System Health
# ============================================================

@router.get("/health", response_model=StandardResponse, tags=["System"])
def health_check():

    return StandardResponse(
        success=True,
        message="Service is healthy",
        data=None
    )


# ============================================================
# LLM Tests
# ============================================================

@router.get("/test-llm", tags=["System"])
def test_llm():

    answer = generate_response(
        "Explain what a vector database is in simple terms."
    )

    return {"response": answer}


@router.get("/test-embedding", tags=["System"])
def test_embedding():

    vector = generate_embedding(
        "This is a test sentence for AstraMind."
    )

    return {"vector_length": len(vector)}


# ============================================================
# Vector Store
# ============================================================

@router.get("/init-collection", tags=["Vector Store"])
def init_collection():

    create_collection()

    return {"status": "Collection created successfully"}


@router.get("/add-sample", tags=["Vector Store"])
def add_sample():

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

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    results = search_text(query)

    return {"results": results}


# ============================================================
# RAG Endpoint (AUTH + PERMISSION + QUERY CLASSIFICATION)
# ============================================================

@router.get("/ask", response_model=RAGResponse, tags=["RAG"])
def ask_question(
    request: Request,
    query: str,
    session_id: str = "default",
    user=Depends(get_current_user)
):

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if len(query) > MAX_QUERY_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="Query exceeds maximum allowed length."
        )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    try:

        # ------------------------------------------
        # STEP 35
        # Permission-based retrieval
        # ------------------------------------------

        user_group_ids = user["group_ids"]

        # ------------------------------------------
        # Call RAG pipeline
        # ------------------------------------------

        response = generate_rag_answer(
            query=query,
            session_id=session_id,
            user_group_ids=user_group_ids
        )

        return response

    except Exception as e:

        logger.error(f"RAG pipeline failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal RAG pipeline error"
        )


# ============================================================
# Tooling
# ============================================================

@router.get("/calculate", tags=["Tools"])
def calculate(expression: str):

    if not expression.strip():
        raise HTTPException(
            status_code=400,
            detail="Expression cannot be empty."
        )

    tool = tool_registry.get_tool("calculator")

    result = tool.run(expression)

    return {
        "expression": expression,
        "result": result
    }


# ============================================================
# Admin Ingestion (PROTECTED)
# ============================================================

@router.get("/admin/ingest-pdf", tags=["Admin"])
def admin_ingest_pdf(
    file_path: str,
    department: str = "general",
    user=Depends(get_current_user)
):

    if not file_path.strip():
        raise HTTPException(status_code=400, detail="file_path required.")

    if not department.strip():
        raise HTTPException(status_code=400, detail="Department cannot be empty.")

    return ingest_pdf(
        file_path=file_path,
        department=department
    )


@router.get("/admin/ingest-url", tags=["Admin"])
def admin_ingest_url(
    url: str,
    department: str = "general",
    user=Depends(get_current_user)
):

    if not url.strip():
        raise HTTPException(status_code=400, detail="URL required.")

    if not department.strip():
        raise HTTPException(status_code=400, detail="Department cannot be empty.")

    return ingest_url(
        url=url,
        department=department
    )


@router.get("/admin/ingest-repo", tags=["Admin"])
def admin_ingest_repo(
    repo_url: str,
    department: str = "general",
    user=Depends(get_current_user)
):

    if not repo_url.strip():
        raise HTTPException(status_code=400, detail="repo_url required.")

    if not department.strip():
        raise HTTPException(status_code=400, detail="Department cannot be empty.")

    return ingest_repo(
        repo_url=repo_url,
        department=department
    )