# import os
# import time
# import uuid
# from pypdf import PdfReader
# from fastapi import HTTPException
# import requests
# from bs4 import BeautifulSoup
# import git
# import tempfile

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

#     # ✅ Read PDF
#     try:
#         reader = PdfReader(file_path)
#     except Exception as e:
#         logger.error(f"PDF read error: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to read PDF")

#     full_text = ""

#     # ✅ Extract text page by page
#     for page_number, page in enumerate(reader.pages):
#         try:
#             text = page.extract_text()
#             if text:
#                 full_text += text.strip() + "\n"
#         except Exception as e:
#             logger.warning(f"Text extraction failed on page {page_number}: {str(e)}")
#             continue

#     # ✅ Validate extracted text
#     if not full_text.strip():
#         raise HTTPException(status_code=400, detail="PDF contains no extractable text")

#     logger.info({
#         "event": "pdf_text_extracted",
#         "file": file_path,
#         "characters_extracted": len(full_text)
#     })

#     # ✅ Chunking
#     try:
#         chunks = smart_chunk_text(full_text)
#     except Exception as e:
#         logger.error(f"Chunking failed: {str(e)}")
#         raise HTTPException(status_code=500, detail="Chunking failed")

#     if not chunks:
#         raise HTTPException(status_code=500, detail="Chunking produced no chunks")

#     logger.info({
#         "event": "pdf_chunking_complete",
#         "file": file_path,
#         "chunks_generated": len(chunks)
#     })

#     stored_count = 0

#     for idx, chunk in enumerate(chunks):

#         chunk = chunk.strip()

#         # Skip extremely small chunks
#         if len(chunk) < 30:
#             continue

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
#             logger.error(f"Embedding/store failed for chunk {idx}: {str(e)}")
#             continue

#     # ❌ If nothing stored, do NOT pretend success
#     if stored_count == 0:
#         raise HTTPException(
#             status_code=500,
#             detail="No chunks were stored. Check chunking or vector store."
#         )

#     total_time = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "pdf_ingestion_complete",
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



# def ingest_url(url: str, department: str = "general"):

#     start_time = time.time()

#     try:
#         response = requests.get(url, timeout=15)
#         response.raise_for_status()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"URL fetch failed: {str(e)}")

#     soup = BeautifulSoup(response.text, "html.parser")

#     text = soup.get_text(separator="\n")

#     if not text.strip():
#         raise HTTPException(status_code=400, detail="URL contains no readable text")

#     chunks = smart_chunk_text(text)

#     stored_count = 0

#     for idx, chunk in enumerate(chunks):

#         if len(chunk.strip()) < 30:
#             continue

#         doc_id = str(uuid.uuid4())

#         add_text(
#             text=chunk,
#             doc_id=doc_id,
#             metadata={
#                 "department": department,
#                 "source": url,
#                 "chunk_index": idx,
#                 "type": "url"
#             }
#         )

#         stored_count += 1

#     latency = round((time.time() - start_time) * 1000, 2)

#     return {
#         "status": "success",
#         "source": url,
#         "chunks_stored": stored_count,
#         "latency_ms": latency
#     }



# def ingest_repo(repo_url: str, department: str = "engineering"):

#     start_time = time.time()

#     temp_dir = tempfile.mkdtemp()

#     try:
#         git.Repo.clone_from(repo_url, temp_dir)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Repo clone failed: {str(e)}")

#     collected_text = ""

#     for root, dirs, files in os.walk(temp_dir):

#         for file in files:

#             if file.lower().endswith((".md", ".txt")):

#                 try:
#                     with open(os.path.join(root, file), "r", encoding="utf-8") as f:
#                         collected_text += f.read() + "\n"
#                 except:
#                     continue

#     if not collected_text.strip():
#         raise HTTPException(status_code=400, detail="Repository contained no readable documentation")

#     chunks = smart_chunk_text(collected_text)

#     stored_count = 0

#     for idx, chunk in enumerate(chunks):

#         if len(chunk.strip()) < 30:
#             continue

#         doc_id = str(uuid.uuid4())

#         add_text(
#             text=chunk,
#             doc_id=doc_id,
#             metadata={
#                 "department": department,
#                 "source": repo_url,
#                 "chunk_index": idx,
#                 "type": "repository"
#             }
#         )

#         stored_count += 1

#     latency = round((time.time() - start_time) * 1000, 2)

#     return {
#         "status": "success",
#         "source": repo_url,
#         "chunks_stored": stored_count,
#         "latency_ms": latency
#     }



import os
import time
import uuid
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from fastapi import HTTPException
from git import Repo
import tempfile

from app.core.vector_store import add_text
from app.services.chunking_service import smart_chunk_text
from app.core.logger import logger


MAX_REPO_FILE_SIZE = 6000


def clean_text(text):

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    return " ".join(text.split())


# ----------------------------
# PDF INGESTION
# ----------------------------

def ingest_pdf(file_path: str, department: str = "general"):

    start_time = time.time()

    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File does not exist")

    reader = PdfReader(file_path)

    full_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            full_text += text + "\n"

    full_text = clean_text(full_text)

    chunks = smart_chunk_text(full_text)

    stored = 0

    for idx, chunk in enumerate(chunks):

        if len(chunk) < 40:
            continue

        add_text(
            text=chunk,
            doc_id=str(uuid.uuid4()),
            metadata={
                "department": department,
                "source": os.path.basename(file_path),
                "type": "pdf",
                "chunk_index": idx
            }
        )

        stored += 1

    logger.info(
        {
            "event": "pdf_ingestion_complete",
            "file": file_path,
            "department": department,
            "chunks_stored": stored,
        }
    )

    return stored


# ----------------------------
# URL INGESTION
# ----------------------------

def ingest_url(url: str, department: str):

    try:

        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text()

        text = clean_text(text)

        chunks = smart_chunk_text(text)

        for idx, chunk in enumerate(chunks):

            add_text(
                text=chunk,
                doc_id=str(uuid.uuid4()),
                metadata={
                    "department": department,
                    "source": url,
                    "type": "url",
                    "chunk_index": idx
                }
            )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"URL fetch failed: {str(e)}"
        )


# ----------------------------
# REPO INGESTION
# ----------------------------

def ingest_repo(repo_url: str, department: str):

    with tempfile.TemporaryDirectory() as temp_dir:

        Repo.clone_from(repo_url, temp_dir)

        for root, dirs, files in os.walk(temp_dir):

            for file in files:

                if file.endswith((".py", ".md", ".txt")):

                    file_path = os.path.join(root, file)

                    try:

                        with open(file_path, "r", encoding="utf-8") as f:

                            text = f.read()

                            text = clean_text(text)

                            text = text[:MAX_REPO_FILE_SIZE]

                            chunks = smart_chunk_text(text)

                            for idx, chunk in enumerate(chunks):

                                add_text(
                                    text=chunk,
                                    doc_id=str(uuid.uuid4()),
                                    metadata={
                                        "department": department,
                                        "source": repo_url,
                                        "file": file,
                                        "type": "repo",
                                        "chunk_index": idx
                                    }
                                )

                    except:
                        continue