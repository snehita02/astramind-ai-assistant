# import os
# import time
# from pypdf import PdfReader
# from fastapi import HTTPException
# import uuid

# from app.core.vector_store import add_text
# from app.services.chunking_service import smart_chunk_text
# from app.core.logger import logger


# def ingest_pdf(file_path: str, department: str = "general"):

#     start_time = time.time()

#     # ✅ Validate file path
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=400, detail="File does not exist")

#     if not file_path.lower().endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only PDF files allowed")

#     try:
#         reader = PdfReader(file_path)
#     except Exception as e:
#         logger.error(f"PDF read error: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to read PDF")

#     full_text = ""

#     for page in reader.pages:
#         text = page.extract_text()
#         if text:
#             full_text += text + "\n"

#     if not full_text.strip():
#         raise HTTPException(status_code=400, detail="PDF contains no extractable text")

#     # ✅ Chunking
#     chunks = smart_chunk_text(full_text)

#     stored_count = 0

#     for idx, chunk in enumerate(chunks):

#         if len(chunk.strip()) < 20:
#             continue  # skip useless chunks


#         doc_id = str(uuid.uuid4())

#         try:
#             add_text(
#                 text=chunk,
#                 doc_id=doc_id,
#                 metadata={
#                     "department": department,
#                     "source": file_path,
#                     "chunk_index": idx,
#                     "type": "pdf"
#                 }
#             )
#             stored_count += 1

#         except Exception as e:
#             logger.error(f"Embedding/store failed: {str(e)}")
#             continue

#     total_time = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "pdf_ingestion",
#         "file": file_path,
#         "department": department,
#         "chunks_stored": stored_count,
#         "latency_ms": total_time
#     })

#     return {
#         "status": "success",
#         "file": file_path,
#         "department": department,
#         "chunks_stored": stored_count,
#         "latency_ms": total_time
#     }



import os
import time
import uuid
from pypdf import PdfReader
from fastapi import HTTPException

from app.core.vector_store import add_text
from app.services.chunking_service import smart_chunk_text
from app.core.logger import logger


def ingest_pdf(file_path: str, department: str = "general"):

    start_time = time.time()

    # ✅ Validate file path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File does not exist")

    if not file_path.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    # ✅ Read PDF
    try:
        reader = PdfReader(file_path)
    except Exception as e:
        logger.error(f"PDF read error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to read PDF")

    full_text = ""

    # ✅ Extract text page by page
    for page_number, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                full_text += text.strip() + "\n"
        except Exception as e:
            logger.warning(f"Text extraction failed on page {page_number}: {str(e)}")
            continue

    # ✅ Validate extracted text
    if not full_text.strip():
        raise HTTPException(status_code=400, detail="PDF contains no extractable text")

    logger.info({
        "event": "pdf_text_extracted",
        "file": file_path,
        "characters_extracted": len(full_text)
    })

    # ✅ Chunking
    try:
        chunks = smart_chunk_text(full_text)
    except Exception as e:
        logger.error(f"Chunking failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Chunking failed")

    if not chunks:
        raise HTTPException(status_code=500, detail="Chunking produced no chunks")

    logger.info({
        "event": "pdf_chunking_complete",
        "file": file_path,
        "chunks_generated": len(chunks)
    })

    stored_count = 0

    for idx, chunk in enumerate(chunks):

        chunk = chunk.strip()

        # Skip extremely small chunks
        if len(chunk) < 30:
            continue

        doc_id = str(uuid.uuid4())

        try:
            add_text(
                text=chunk,
                doc_id=doc_id,
                metadata={
                    "department": department,
                    "source": file_path,
                    "chunk_index": idx,
                    "type": "pdf"
                }
            )
            stored_count += 1

        except Exception as e:
            logger.error(f"Embedding/store failed for chunk {idx}: {str(e)}")
            continue

    # ❌ If nothing stored, do NOT pretend success
    if stored_count == 0:
        raise HTTPException(
            status_code=500,
            detail="No chunks were stored. Check chunking or vector store."
        )

    total_time = round((time.time() - start_time) * 1000, 2)

    logger.info({
        "event": "pdf_ingestion_complete",
        "file": file_path,
        "department": department,
        "chunks_stored": stored_count,
        "latency_ms": total_time
    })

    return {
        "status": "success",
        "file": file_path,
        "department": department,
        "chunks_stored": stored_count,
        "latency_ms": total_time
    }