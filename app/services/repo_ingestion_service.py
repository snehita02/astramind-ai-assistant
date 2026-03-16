# import os
# import time
# import uuid
# import shutil
# from git import Repo
# from fastapi import HTTPException

# from app.core.vector_store import add_text
# from app.services.chunking_service import smart_chunk_text
# from app.core.logger import logger


# ALLOWED_EXTENSIONS = {
#     ".py", ".js", ".ts", ".java", ".cpp",
#     ".md", ".txt", ".json", ".yaml", ".yml"
# }

# IGNORED_DIRECTORIES = {
#     ".git", "node_modules", "build", "dist",
#     "__pycache__", "venv", ".idea", ".vscode"
# }


# def ingest_repo(repo_url: str, department: str = "general"):

#     start_time = time.time()

#     if not repo_url.startswith("https://github.com/"):
#         raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

#     temp_dir = f"temp_repo_{uuid.uuid4().hex}"

#     try:
#         Repo.clone_from(repo_url, temp_dir)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to clone repository: {str(e)}")

#     stored_count = 0

#     try:
#         for root, dirs, files in os.walk(temp_dir):

#             dirs[:] = [d for d in dirs if d not in IGNORED_DIRECTORIES]

#             for file in files:

#                 extension = os.path.splitext(file)[1].lower()

#                 if extension not in ALLOWED_EXTENSIONS:
#                     continue

#                 file_path = os.path.join(root, file)

#                 try:
#                     if os.path.getsize(file_path) > 300_000:
#                         continue

#                     with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
#                         content = f.read()

#                 except Exception:
#                     continue

#                 if not content.strip():
#                     continue

#                 chunks = smart_chunk_text(content)

#                 relative_path = os.path.relpath(file_path, temp_dir)

#                 for idx, chunk in enumerate(chunks):

#                     if len(chunk.strip()) < 50:
#                         continue

#                     doc_id = str(uuid.uuid4())

#                     try:
#                         add_text(
#                             text=chunk,
#                             doc_id=doc_id,
#                             metadata={
#                                 "department": department,
#                                 "source": repo_url,
#                                 "file_path": relative_path,
#                                 "file_type": extension,
#                                 "chunk_index": idx,
#                                 "type": "repo"
#                             }
#                         )
#                         stored_count += 1

#                     except Exception as e:
#                         logger.error(f"Repo store failed: {str(e)}")
#                         continue

#     finally:
#         shutil.rmtree(temp_dir, ignore_errors=True)

#     if stored_count == 0:
#         raise HTTPException(
#             status_code=400,
#             detail="No valid text files were ingested from repository."
#         )

#     total_time = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "repo_ingestion",
#         "repo_url": repo_url,
#         "department": department,
#         "chunks_stored": stored_count,
#         "latency_ms": total_time
#     })

#     return {
#         "status": "success",
#         "repo_url": repo_url,
#         "department": department,
#         "chunks_stored": stored_count,
#         "latency_ms": total_time
#     }
















# import os
# import time
# import uuid
# import shutil
# from git import Repo
# from fastapi import HTTPException

# from app.core.vector_store import add_text
# from app.services.chunking_service import smart_chunk_text
# from app.core.logger import logger


# ALLOWED_EXTENSIONS = {
#     ".py", ".js", ".ts", ".java", ".cpp",
#     ".md", ".txt", ".json", ".yaml", ".yml"
# }

# IGNORED_DIRECTORIES = {
#     ".git", "node_modules", "build", "dist",
#     "__pycache__", "venv", ".idea", ".vscode"
# }


# def ingest_repo(repo_url: str, department: str = "general"):

#     start_time = time.time()

#     if not repo_url.startswith("https://github.com/"):
#         raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

#     temp_dir = f"temp_repo_{uuid.uuid4().hex}"

#     try:
#         Repo.clone_from(repo_url, temp_dir)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to clone repository: {str(e)}")

#     stored_count = 0

#     try:
#         for root, dirs, files in os.walk(temp_dir):

#             dirs[:] = [d for d in dirs if d not in IGNORED_DIRECTORIES]

#             for file in files:

#                 extension = os.path.splitext(file)[1].lower()

#                 if extension not in ALLOWED_EXTENSIONS:
#                     continue

#                 file_path = os.path.join(root, file)

#                 try:
#                     if os.path.getsize(file_path) > 300_000:
#                         continue

#                     with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
#                         content = f.read()

#                 except Exception:
#                     continue

#                 if not content.strip():
#                     continue

#                 chunks = smart_chunk_text(content)

#                 relative_path = os.path.relpath(file_path, temp_dir)

#                 # 🔥 PRIORITY FLAG
#                 is_priority_doc = file.lower().startswith("readme")

#                 for idx, chunk in enumerate(chunks):

#                     if len(chunk.strip()) < 50:
#                         continue

#                     doc_id = str(uuid.uuid4())

#                     try:
#                         add_text(
#                             text=chunk,
#                             doc_id=doc_id,
#                             metadata={
#                                 "department": department,
#                                 "source": repo_url,
#                                 "file_path": relative_path,
#                                 "file_type": extension,
#                                 "chunk_index": idx,
#                                 "type": "repo",
#                                 "is_priority_doc": is_priority_doc,
#                                 "is_primary_chunk": True if is_priority_doc and idx == 0 else False
#                             }
#                         )
#                         stored_count += 1

#                     except Exception as e:
#                         logger.error(f"Repo store failed: {str(e)}")
#                         continue

#     finally:
#         shutil.rmtree(temp_dir, ignore_errors=True)

#     if stored_count == 0:
#         raise HTTPException(
#             status_code=400,
#             detail="No valid text files were ingested from repository."
#         )

#     total_time = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "repo_ingestion",
#         "repo_url": repo_url,
#         "department": department,
#         "chunks_stored": stored_count,
#         "latency_ms": total_time
#     })

#     return {
#         "status": "success",
#         "repo_url": repo_url,
#         "department": department,
#         "chunks_stored": stored_count,
#         "latency_ms": total_time
#     }



















# import tempfile
# import shutil
# import os
# import uuid

# from git import Repo

# from app.core.vector_store import add_text
# from app.core.logger import logger


# CHUNK_SIZE = 1000
# CHUNK_OVERLAP = 200


# def chunk_text(text):

#     chunks = []
#     start = 0

#     while start < len(text):

#         end = start + CHUNK_SIZE
#         chunk = text[start:end]

#         chunks.append(chunk)

#         start += CHUNK_SIZE - CHUNK_OVERLAP

#     return chunks


# def ingest_repo(repo_url, department):

#     temp_dir = tempfile.mkdtemp()

#     try:

#         Repo.clone_from(repo_url, temp_dir)

#         stored_chunks = 0

#         for root, _, files in os.walk(temp_dir):

#             for file in files:

#                 if not file.endswith((".py", ".md", ".txt", ".js", ".ts")):
#                     continue

#                 file_path = os.path.join(root, file)

#                 try:

#                     with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
#                         content = f.read()

#                 except:
#                     continue

#                 chunks = chunk_text(content)

#                 for chunk in chunks:

#                     add_text(
#                         text=chunk,
#                         doc_id=str(uuid.uuid4()),
#                         metadata={
#                             "department": department,
#                             "source": repo_url,
#                             "type": "repo"
#                         }
#                     )

#                     stored_chunks += 1

#         logger.info(
#             "repo_ingestion_complete",
#             repo=repo_url,
#             department=department,
#             chunks_stored=stored_chunks
#         )

#     except Exception as e:

#         logger.error(f"Repo store failed: {str(e)}")

#     finally:

#         shutil.rmtree(temp_dir)




















import tempfile
import shutil
import os
import uuid
import time

from git import Repo

from app.core.vector_store import add_text
from app.core.logger import logger


# -------------------------------
# SETTINGS
# -------------------------------

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

MAX_FILE_SIZE = 200000  # 200KB safety limit

# Only useful text/code files
ALLOWED_EXTENSIONS = (
    ".py",
    ".md",
    ".txt",
    ".ipynb"
)

# Skip heavy folders
IGNORE_DIRS = {
    ".git",
    "tests",
    "test",
    "examples",
    "build",
    "dist",
    "__pycache__",
    "node_modules",
    ".venv",
    ".idea",
    ".vscode",
    "site-packages",
    "docs/_build"
}

# Slow down embedding requests slightly
EMBEDDING_DELAY = 0.05


# -------------------------------
# TEXT CHUNKING
# -------------------------------

def chunk_text(text):

    chunks = []
    start = 0

    text_length = len(text)

    while start < text_length:

        end = start + CHUNK_SIZE
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# -------------------------------
# REPO INGESTION
# -------------------------------

def ingest_repo(repo_url, department):

    temp_dir = tempfile.mkdtemp()

    try:

        logger.info(f"Cloning repo: {repo_url}")

        # shallow clone for speed
        Repo.clone_from(repo_url, temp_dir, depth=1)

        stored_chunks = 0

        for root, dirs, files in os.walk(temp_dir, topdown=True):

            # filter unwanted directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:

                if not file.endswith(ALLOWED_EXTENSIONS):
                    continue

                file_path = os.path.join(root, file)

                # Skip files that disappear during traversal
                if not os.path.exists(file_path):
                    continue

                try:

                    # Skip large files
                    if os.path.getsize(file_path) > MAX_FILE_SIZE:
                        continue

                except Exception:
                    continue

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        content = f.read()

                except Exception:
                    continue

                chunks = chunk_text(content)

                for chunk in chunks:

                    try:

                        add_text(
                            text=chunk,
                            doc_id=str(uuid.uuid4()),
                            metadata={
                                "department": department,
                                "source": repo_url,
                                "type": "repo"
                            }
                        )

                        stored_chunks += 1

                        # Prevent API overload
                        time.sleep(EMBEDDING_DELAY)

                    except Exception as e:

                        logger.error(f"Embedding failed: {str(e)}")

        logger.info(
            f"repo_ingestion_complete | repo={repo_url} | department={department} | chunks={stored_chunks}"
        )

    except Exception as e:

        logger.error(f"Repo store failed: {str(e)}")

    finally:

        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass
