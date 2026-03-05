import os
from app.utils.chunking import chunk_text
from app.core.vector_store import add_text

def ingest_text_file(file_path: str, base_id: int = 1000):
    """
    Reads a text file, chunks it, and stores chunks in Qdrant.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_text(content)

    for i, chunk in enumerate(chunks):
        add_text(chunk, base_id + i)

    return len(chunks)