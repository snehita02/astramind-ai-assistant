# def smart_chunk_text(text: str, chunk_size: int = 500):

#     words = text.split()
#     chunks = []

#     current_chunk = []

#     for word in words:
#         current_chunk.append(word)

#         if len(current_chunk) >= chunk_size:
#             chunks.append(" ".join(current_chunk))
#             current_chunk = []

#     if current_chunk:
#         chunks.append(" ".join(current_chunk))

#     return chunks



import re


def approximate_token_count(text: str) -> int:
    # Rough estimate: 1 token ≈ 4 characters
    return len(text) // 4


def smart_chunk_text(
    text: str,
    max_tokens: int = 500,
    overlap_tokens: int = 50
):
    """
    Advanced chunking:
    - Token-aware splitting
    - Overlap support
    - Avoid cutting mid-sentence where possible
    """

    if not text or not text.strip():
        return []

    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        if approximate_token_count(current_chunk + sentence) <= max_tokens:
            current_chunk += " " + sentence
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # Add overlap from previous chunk
            if overlap_tokens > 0 and chunks:
                overlap_text = current_chunk[-(overlap_tokens * 4):]
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk = sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks