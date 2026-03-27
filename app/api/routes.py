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












































# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text
# from app.core.logger import logger

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user

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
# # RAG Endpoint (AUTH + PERMISSION + QUERY CLASSIFICATION)
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = "default",
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise HTTPException(
#             status_code=400,
#             detail="Query exceeds maximum allowed length."
#         )

#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Authentication required"
#         )

#     try:

#         # ------------------------------------------
#         # STEP 35
#         # Permission-based retrieval
#         # ------------------------------------------

#         user_group_ids = user["group_ids"]

#         # ------------------------------------------
#         # Call RAG pipeline
#         # ------------------------------------------

#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             user_group_ids=user_group_ids
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
#         raise HTTPException(
#             status_code=400,
#             detail="Expression cannot be empty."
#         )

#     tool = tool_registry.get_tool("calculator")

#     result = tool.run(expression)

#     return {
#         "expression": expression,
#         "result": result
#     }


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

#     return ingest_pdf(
#         file_path=file_path,
#         department=department
#     )


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

#     return ingest_url(
#         url=url,
#         department=department
#     )


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

#     return ingest_repo(
#         repo_url=repo_url,
#         department=department
#     )


























# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text
# from app.core.logger import logger

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user
# from app.database.auth_database import get_user

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
# # RAG Endpoint (AUTH + PERMISSION + SAFE USER FETCH)
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = "default",
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise HTTPException(
#             status_code=400,
#             detail="Query exceeds maximum allowed length."
#         )

#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Authentication required"
#         )

#     try:

#         # --------------------------------------------------
#         # SAFETY FIX: Always fetch latest user from database
#         # --------------------------------------------------

#         db_user = get_user(user["user_id"])

#         if db_user is None:
#             raise HTTPException(status_code=401, detail="User not found")

#         user_group_ids = db_user["group_ids"]

#         # --------------------------------------------------
#         # Call RAG pipeline
#         # --------------------------------------------------

#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             user_group_ids=user_group_ids
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
#         raise HTTPException(
#             status_code=400,
#             detail="Expression cannot be empty."
#         )

#     tool = tool_registry.get_tool("calculator")

#     result = tool.run(expression)

#     return {
#         "expression": expression,
#         "result": result
#     }


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

#     return ingest_pdf(
#         file_path=file_path,
#         department=department
#     )


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

#     return ingest_url(
#         url=url,
#         department=department
#     )


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

#     return ingest_repo(
#         repo_url=repo_url,
#         department=department
#     )














# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text
# from app.core.logger import logger

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user

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
# # RAG Endpoint (AUTH + PERMISSION)
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = "default",
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise HTTPException(
#             status_code=400,
#             detail="Query exceeds maximum allowed length."
#         )

#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Authentication required"
#         )

#     try:

#         user_group_ids = user["group_ids"]

#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             user_group_ids=user_group_ids
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
#         raise HTTPException(
#             status_code=400,
#             detail="Expression cannot be empty."
#         )

#     tool = tool_registry.get_tool("calculator")

#     result = tool.run(expression)

#     return {
#         "expression": expression,
#         "result": result
#     }


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

#     return ingest_pdf(
#         file_path=file_path,
#         department=department
#     )


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

#     return ingest_url(
#         url=url,
#         department=department
#     )


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

#     return ingest_repo(
#         repo_url=repo_url,
#         department=department
#     )































# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text
# from app.core.logger import logger

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user

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
# # RAG Endpoint (AUTH + PERMISSION)
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = "default",
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise HTTPException(
#             status_code=400,
#             detail="Query exceeds maximum allowed length."
#         )

#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Authentication required"
#         )

#     try:

#         user_group_ids = user["group_ids"]

#         # -------------------------------------------------
#         # Resolve departments from user groups
#         # -------------------------------------------------

#         allowed_departments = user.get("departments", ["general"])

#         logger.info(f"USER GROUP IDS: {user_group_ids}")
#         logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#         # -------------------------------------------------
#         # Generate RAG Answer
#         # -------------------------------------------------

#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             user_group_ids=user_group_ids,
#             allowed_departments=allowed_departments
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
#         raise HTTPException(
#             status_code=400,
#             detail="Expression cannot be empty."
#         )

#     tool = tool_registry.get_tool("calculator")

#     result = tool.run(expression)

#     return {
#         "expression": expression,
#         "result": result
#     }


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

#     return ingest_pdf(
#         file_path=file_path,
#         department=department
#     )


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

#     return ingest_url(
#         url=url,
#         department=department
#     )


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

#     return ingest_repo(
#         repo_url=repo_url,
#         department=department
#     )






















# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text
# from app.core.logger import logger

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

# # ✅ NEW IMPORTS (CHAT HISTORY)
# from app.database.chat_database import (
#     create_chat_session,
#     save_message,
#     get_chat_history
# )

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
# # RAG Endpoint (AUTH + PERMISSION + CHAT HISTORY ✅)
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = None,   # ✅ CHANGED (was "default")
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise HTTPException(
#             status_code=400,
#             detail="Query exceeds maximum allowed length."
#         )

#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Authentication required"
#         )

#     try:

#         user_group_ids = user["group_ids"]
#         user_id = user.get("user_id", "default_user")

#         # -------------------------------------------------
#         # SESSION HANDLING (NEW)
#         # -------------------------------------------------

#         if not session_id:
#             session_id = create_chat_session(user_id)

#         # SAVE USER MESSAGE
#         save_message(session_id, "user", query)

#         # -------------------------------------------------
#         # PERMISSIONS
#         # -------------------------------------------------

#         allowed_departments = resolve_departments(user_group_ids)

#         logger.info(f"USER GROUP IDS: {user_group_ids}")
#         logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#         # -------------------------------------------------
#         # RAG PIPELINE (UNCHANGED)
#         # -------------------------------------------------

#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             user_group_ids=user_group_ids,
#             allowed_departments=allowed_departments
#         )

#         # -------------------------------------------------
#         # SAVE BOT RESPONSE (NEW)
#         # -------------------------------------------------

#         try:
#             answer_text = response.answer if hasattr(response, "answer") else str(response)
#             save_message(session_id, "assistant", answer_text)
#         except Exception as e:
#             logger.warning(f"Failed to save assistant message: {e}")

#         return response

#     except Exception as e:

#         logger.error(f"RAG pipeline failed: {str(e)}")

#         raise HTTPException(
#             status_code=500,
#             detail="Internal RAG pipeline error"
#         )


# # ============================================================
# # CHAT HISTORY (NEW)
# # ============================================================

# @router.get("/chat/{session_id}", tags=["Chat"])
# def fetch_chat_history(
#     session_id: str,
#     user=Depends(get_current_user)
# ):

#     try:
#         history = get_chat_history(session_id)

#         return {
#             "session_id": session_id,
#             "messages": history
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # Tooling
# # ============================================================

# @router.get("/calculate", tags=["Tools"])
# def calculate(expression: str):

#     if not expression.strip():
#         raise HTTPException(
#             status_code=400,
#             detail="Expression cannot be empty."
#         )

#     tool = tool_registry.get_tool("calculator")

#     result = tool.run(expression)

#     return {
#         "expression": expression,
#         "result": result
#     }


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

#     return ingest_pdf(
#         file_path=file_path,
#         department=department
#     )


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

#     return ingest_url(
#         url=url,
#         department=department
#     )


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

#     return ingest_repo(
#         repo_url=repo_url,
#         department=department
#     )





















# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text
# from app.core.logger import logger

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user

# from app.config import MAX_QUERY_LENGTH
# from app.schemas.response_models import RAGResponse, StandardResponse

# from app.database.chat_database import (
#     create_chat_session,
#     save_message,
#     get_chat_history
# )

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
# # RAG Endpoint (UPDATED FOR STEP 39)
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = None,
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise HTTPException(
#             status_code=400,
#             detail="Query exceeds maximum allowed length."
#         )

#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Authentication required"
#         )

#     try:

#         user_id = user.get("user_id", "default_user")

#         # -------------------------------------------------
#         # SESSION
#         # -------------------------------------------------

#         if not session_id:
#             session_id = create_chat_session(user_id)

#         save_message(session_id, "user", query)

#         # -------------------------------------------------
#         # 🔥 STEP 39 CHANGE — PASS FULL USER
#         # -------------------------------------------------

#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             user=user   # ⭐ FULL USER PASSED
#         )

#         # -------------------------------------------------
#         # SAVE BOT RESPONSE
#         # -------------------------------------------------

#         try:
#             answer_text = response["answer"]
#             save_message(session_id, "assistant", answer_text)
#         except Exception as e:
#             logger.warning(f"Save error: {e}")

#         return response

#     except Exception as e:

#         logger.error(f"RAG pipeline failed: {str(e)}")

#         raise HTTPException(
#             status_code=500,
#             detail="Internal RAG pipeline error"
#         )























# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text
# from app.core.logger import logger

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user
# from app.auth.permissions import resolve_departments  # ✅ STEP 39

# from app.config import MAX_QUERY_LENGTH
# from app.schemas.response_models import RAGResponse, StandardResponse

# # ✅ CHAT HISTORY (STEP 36)
# from app.database.chat_database import (
#     create_chat_session,
#     save_message,
#     get_chat_history
# )

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
# # RAG Endpoint (STEP 36 + 39)
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = None,
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise HTTPException(status_code=400, detail="Query too long")

#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication required")

#     try:
#         user_id = user["user_id"]
#         group_ids = user["group_ids"]

#         # ---------------- SESSION ----------------
#         if not session_id:
#             session_id = create_chat_session(user_id)

#         save_message(session_id, "user", query)

#         # ---------------- PERMISSIONS ----------------
#         # allowed_departments = resolve_departments(group_ids)
#         allowed_departments = resolve_departments(group_ids)

#         # 🔥 FIX: FLATTEN HERE ALSO
#         if isinstance(allowed_departments, list):
#             allowed_departments = [
#                 d for item in allowed_departments
#                 for d in (item if isinstance(item, list) else [item])
#             ]

#         # ---------------- RAG ----------------
#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             user=user,   # ✅ STEP 39 FULL USER
#             allowed_departments=allowed_departments
#         )

#         # ---------------- SAVE BOT ----------------
#         try:
#             answer_text = response["answer"]
#             save_message(session_id, "assistant", answer_text)
#         except Exception as e:
#             logger.warning(f"Save error: {e}")

#         return response

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")
#         raise HTTPException(status_code=500, detail="RAG error")


# # ============================================================
# # CHAT HISTORY (STEP 36 RESTORED)
# # ============================================================

# @router.get("/chat/{session_id}", tags=["Chat"])
# def fetch_chat_history(
#     session_id: str,
#     user=Depends(get_current_user)
# ):
#     try:
#         history = get_chat_history(session_id)

#         return {
#             "session_id": session_id,
#             "messages": history
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # Tools
# # ============================================================

# @router.get("/calculate", tags=["Tools"])
# def calculate(expression: str):
#     if not expression.strip():
#         raise HTTPException(status_code=400, detail="Empty expression")

#     tool = tool_registry.get_tool("calculator")
#     result = tool.run(expression)

#     return {
#         "expression": expression,
#         "result": result
#     }


# # ============================================================
# # ADMIN INGESTION (NO BREAK — STEP 40 READY)
# # ============================================================

# @router.get("/admin/ingest-pdf", tags=["Admin"])
# def admin_ingest_pdf(
#     file_path: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):
#     return ingest_pdf(file_path=file_path, department=department)


# @router.get("/admin/ingest-url", tags=["Admin"])
# def admin_ingest_url(
#     url: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):
#     return ingest_url(url=url, department=department)


# @router.get("/admin/ingest-repo", tags=["Admin"])
# def admin_ingest_repo(
#     repo_url: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):
#     return ingest_repo(repo_url=repo_url, department=department)





















# from fastapi import APIRouter, HTTPException, Request, Depends

# from app.core.llm_provider import generate_response
# from app.core.embeddings import generate_embedding
# from app.core.vector_store import create_collection, add_text, search_text
# from app.core.logger import logger

# from app.services.document_service import ingest_text_file
# from app.services.rag_service import generate_rag_answer
# from app.services.tools.tool_registry import tool_registry
# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo

# from app.auth.auth_dependency import get_current_user
# from app.auth.permissions import resolve_departments  # ✅ STEP 39

# from app.config import MAX_QUERY_LENGTH
# from app.schemas.response_models import RAGResponse, StandardResponse

# # ✅ CHAT HISTORY (STEP 36)
# from app.database.chat_database import (
#     create_chat_session,
#     save_message,
#     get_chat_history
# )

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
# # RAG Endpoint (STEP 36 + 39)
# # ============================================================

# @router.get("/ask", response_model=RAGResponse, tags=["RAG"])
# def ask_question(
#     request: Request,
#     query: str,
#     session_id: str = None,
#     user=Depends(get_current_user)
# ):

#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise HTTPException(status_code=400, detail="Query too long")

#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication required")

#     try:
#         # 🔥 FIX: safely normalize user in case get_current_user returns a list
#         if isinstance(user, list):
#             user = user[0] if len(user) > 0 and isinstance(user[0], dict) else {}

#         user_id = user.get("user_id")
#         group_ids = user.get("group_ids", [])

#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid user data")

#         # ---------------- SESSION ----------------
#         if not session_id:
#             session_id = create_chat_session(user_id)

#         save_message(session_id, "user", query)

#         # ---------------- PERMISSIONS ----------------
#         allowed_departments = resolve_departments(group_ids)

#         # 🔥 FIX: FLATTEN HERE ALSO
#         if isinstance(allowed_departments, list):
#             allowed_departments = [
#                 d for item in allowed_departments
#                 for d in (item if isinstance(item, list) else [item])
#             ]

#         # ---------------- RAG ----------------
#         response = generate_rag_answer(
#             query=query,
#             session_id=session_id,
#             user=user,
#             allowed_departments=allowed_departments
#         )

#         # ---------------- SAVE BOT ----------------
#         try:
#             answer_text = response["answer"]
#             save_message(session_id, "assistant", answer_text)
#         except Exception as e:
#             logger.warning(f"Save error: {e}")

#         return response

#     except HTTPException:
#         raise

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")
#         raise HTTPException(status_code=500, detail="RAG error")


# # ============================================================
# # CHAT HISTORY (STEP 36 RESTORED)
# # ============================================================

# @router.get("/chat/{session_id}", tags=["Chat"])
# def fetch_chat_history(
#     session_id: str,
#     user=Depends(get_current_user)
# ):
#     try:
#         history = get_chat_history(session_id)

#         return {
#             "session_id": session_id,
#             "messages": history
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # Tools
# # ============================================================

# @router.get("/calculate", tags=["Tools"])
# def calculate(expression: str):
#     if not expression.strip():
#         raise HTTPException(status_code=400, detail="Empty expression")

#     tool = tool_registry.get_tool("calculator")
#     result = tool.run(expression)

#     return {
#         "expression": expression,
#         "result": result
#     }


# # ============================================================
# # ADMIN INGESTION (NO BREAK — STEP 40 READY)
# # ============================================================

# @router.get("/admin/ingest-pdf", tags=["Admin"])
# def admin_ingest_pdf(
#     file_path: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):
#     return ingest_pdf(file_path=file_path, department=department)


# @router.get("/admin/ingest-url", tags=["Admin"])
# def admin_ingest_url(
#     url: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):
#     return ingest_url(url=url, department=department)


# @router.get("/admin/ingest-repo", tags=["Admin"])
# def admin_ingest_repo(
#     repo_url: str,
#     department: str = "general",
#     user=Depends(get_current_user)
# ):
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
from app.auth.permissions import resolve_departments

from app.config import MAX_QUERY_LENGTH
from app.schemas.response_models import RAGResponse, StandardResponse

from app.database.chat_database import (
    create_chat_session,
    save_message,
    get_chat_history
)

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
# RAG Endpoint
# ============================================================

@router.get("/ask", response_model=RAGResponse, tags=["RAG"])
def ask_question(
    request: Request,
    query: str,
    session_id: str = None,
    user=Depends(get_current_user)
):

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if len(query) > MAX_QUERY_LENGTH:
        raise HTTPException(status_code=400, detail="Query too long")

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid user data")

        # ---------------- SESSION ----------------
        if not session_id:
            session_id = create_chat_session(user_id)

        save_message(session_id, "user", query)

        # ---------------- PERMISSIONS ----------------
        # 🔥 FIX: pass full user dict so resolve_departments can read role + group_ids
        allowed_departments = resolve_departments(user)

        # ---------------- RAG ----------------
        response = generate_rag_answer(
            query=query,
            session_id=session_id,
            user=user,
            allowed_departments=allowed_departments
        )

        # ---------------- SAVE BOT ----------------
        try:
            answer_text = response["answer"]
            save_message(session_id, "assistant", answer_text)
        except Exception as e:
            logger.warning(f"Save error: {e}")

        return response

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"RAG failed: {str(e)}")
        raise HTTPException(status_code=500, detail="RAG error")


# ============================================================
# CHAT HISTORY
# ============================================================

@router.get("/chat/{session_id}", tags=["Chat"])
def fetch_chat_history(
    session_id: str,
    user=Depends(get_current_user)
):
    try:
        history = get_chat_history(session_id)
        return {
            "session_id": session_id,
            "messages": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Tools
# ============================================================

@router.get("/calculate", tags=["Tools"])
def calculate(expression: str):
    if not expression.strip():
        raise HTTPException(status_code=400, detail="Empty expression")

    tool = tool_registry.get_tool("calculator")
    result = tool.run(expression)

    return {
        "expression": expression,
        "result": result
    }


# ============================================================
# ADMIN INGESTION
# ============================================================

@router.get("/admin/ingest-pdf", tags=["Admin"])
def admin_ingest_pdf(
    file_path: str,
    department: str = "general",
    user=Depends(get_current_user)
):
    return ingest_pdf(file_path=file_path, department=department)


@router.get("/admin/ingest-url", tags=["Admin"])
def admin_ingest_url(
    url: str,
    department: str = "general",
    user=Depends(get_current_user)
):
    return ingest_url(url=url, department=department)


@router.get("/admin/ingest-repo", tags=["Admin"])
def admin_ingest_repo(
    repo_url: str,
    department: str = "general",
    user=Depends(get_current_user)
):
    return ingest_repo(repo_url=repo_url, department=department)