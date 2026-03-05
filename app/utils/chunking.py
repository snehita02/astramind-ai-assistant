# def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
#     """
#     Splits text into chunks with overlap.
#     """
#     chunks = []
#     start = 0
#     text_length = len(text)

#     while start < text_length:
#         end = start + chunk_size
#         chunk = text[start:end]
#         chunks.append(chunk)
#         start += chunk_size - overlap

#     return chunks




import re

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150):
    """
    Smarter chunking:
    - Splits by paragraphs first
    - Preserves semantic structure
    - Adds overlap between chunks
    """

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Split by sentence boundaries
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Add overlap
    overlapped_chunks = []
    for i in range(len(chunks)):
        if i == 0:
            overlapped_chunks.append(chunks[i])
        else:
            overlap_text = chunks[i-1][-overlap:]
            overlapped_chunks.append(overlap_text + " " + chunks[i])

    return overlapped_chunks