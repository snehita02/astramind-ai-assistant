# import time
# import uuid
# import requests
# from bs4 import BeautifulSoup
# from fastapi import HTTPException

# from app.services.chunking_service import smart_chunk_text
# from app.core.vector_store import add_text
# from app.core.logger import logger


# def ingest_url(url: str, department: str = "general"):

#     start_time = time.time()

#     # -----------------------------
#     # Step 1 — Validate URL
#     # -----------------------------
#     if not url.startswith("http://") and not url.startswith("https://"):
#         raise HTTPException(status_code=400, detail="Invalid URL format")

#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

#     # -----------------------------
#     # Step 2 — Extract Clean Text
#     # -----------------------------
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Remove scripts and styles
#     for script in soup(["script", "style"]):
#         script.extract()

#     text = soup.get_text(separator="\n")

#     if not text.strip():
#         raise HTTPException(status_code=400, detail="No extractable text from URL")

#     # -----------------------------
#     # Step 3 — Chunking
#     # -----------------------------
#     chunks = smart_chunk_text(text)

#     stored_count = 0

#     for idx, chunk in enumerate(chunks):

#         if len(chunk.strip()) < 30:
#             continue

#         doc_id = str(uuid.uuid4())

#         try:
#             add_text(
#                 text=chunk,
#                 doc_id=doc_id,
#                 metadata={
#                     "department": department,
#                     "source": url,
#                     "chunk_index": idx,
#                     "type": "url"
#                 }
#             )
#             stored_count += 1

#         except Exception as e:
#             logger.error(f"URL ingestion store failed: {str(e)}")
#             continue

#     total_time = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "url_ingestion",
#         "url": url,
#         "department": department,
#         "chunks_stored": stored_count,
#         "latency_ms": total_time
#     })

#     return {
#         "status": "success",
#         "url": url,
#         "department": department,
#         "chunks_stored": stored_count,
#         "latency_ms": total_time
#     }



import time
import uuid
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

from app.services.chunking_service import smart_chunk_text
from app.core.vector_store import add_text
from app.core.logger import logger


def ingest_url(url: str, department: str = "general"):

    start_time = time.time()

    # -----------------------------
    # Step 1 — Validate URL
    # -----------------------------
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    headers = {
        "User-Agent": "Mozilla/5.0 (EnterpriseKnowledgeBot/1.0)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    # -----------------------------
    # Step 2 — Validate Content-Type
    # -----------------------------
    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type:
        raise HTTPException(
            status_code=400,
            detail="URL does not contain HTML content"
        )

    # -----------------------------
    # Step 3 — Extract Clean Text
    # -----------------------------
    soup = BeautifulSoup(response.text, "html.parser")

    for script in soup(["script", "style", "noscript"]):
        script.extract()

    text = soup.get_text(separator="\n")

    # Normalize whitespace
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)

    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text from URL")

    # -----------------------------
    # Step 4 — Chunking
    # -----------------------------
    chunks = smart_chunk_text(text)

    stored_count = 0

    for idx, chunk in enumerate(chunks):

        if len(chunk.strip()) < 50:
            continue

        doc_id = str(uuid.uuid4())

        try:
            add_text(
                text=chunk,
                doc_id=doc_id,
                metadata={
                    "department": department,
                    "source": url,
                    "chunk_index": idx,
                    "type": "url"
                }
            )
            stored_count += 1

        except Exception as e:
            logger.error(f"URL ingestion store failed: {str(e)}")
            continue

    if stored_count == 0:
        raise HTTPException(
            status_code=400,
            detail="No valid content chunks were stored from URL."
        )

    total_time = round((time.time() - start_time) * 1000, 2)

    logger.info({
        "event": "url_ingestion",
        "url": url,
        "department": department,
        "chunks_stored": stored_count,
        "latency_ms": total_time
    })

    return {
        "status": "success",
        "url": url,
        "department": department,
        "chunks_stored": stored_count,
        "latency_ms": total_time
    }