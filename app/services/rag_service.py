# import time
# from typing import List

# from openai import OpenAI

# from app.core.vector_store import search_text
# from app.core.logger import logger
# from app.services.memory_service import memory

# from app.auth.permissions import resolve_departments

# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
#     MAX_PROMPT_TOTAL_CHARS,
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     scored = []
#     query_words = set(query.lower().split())

#     for chunk in chunks:

#         text = chunk["text"].lower()

#         score = sum(1 for word in query_words if word in text)

#         scored.append((score, chunk))

#     scored.sort(reverse=True, key=lambda x: x[0])

#     return [c[1] for c in scored[:top_k]]


# def build_context(chunks: List[str]):
#     return "\n\n".join(chunks)


# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind, an enterprise knowledge assistant.

# STRICT RULES:

# 1. Use ONLY the provided context.
# 2. Do NOT use external knowledge.
# 3. If the answer cannot be found in the context,
#    respond EXACTLY with:

#    I don't know.

# 4. Keep answers concise and factual.
# """

#     history_text = ""

#     for msg in history:

#         role = msg["role"]
#         content = msg["content"]

#         if role == "user":
#             history_text += f"User: {content}\n"
#         else:
#             history_text += f"Assistant: {content}\n"

#     user_prompt = f"""
# Conversation:
# {history_text}

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     response = client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt.strip()},
#             {"role": "user", "content": user_prompt.strip()},
#         ],
#         temperature=0.2,
#         max_tokens=350
#     )

#     return response.choices[0].message.content.strip()


# def generate_rag_answer(query: str, session_id: str, user_group_ids: list):

#     start_time = time.time()

#     history = memory.get_history(session_id)

#     # Allowed departments
#     allowed_departments = resolve_departments(user_group_ids)

#     # Vector search ONLY inside allowed departments
#     try:

#         retrieved_chunks = search_text(
#             query=query,
#             department=allowed_departments,
#             limit=10
#         )

#     except Exception as e:

#         logger.error(f"Vector search failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Knowledge retrieval system unavailable.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id
#         }

#     if not retrieved_chunks:

#         return {
#             "question": query,
#             "answer": "I don't know.",
#             "confidence": 0.2,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Knowledge boundary triggered",
#             "context_used": [],
#             "session_id": session_id
#         }

#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]

#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
#         context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

#     answer = generate_answer_from_llm(query, context, history)

#     memory.add_message(session_id, "user", query)
#     memory.add_message(session_id, "assistant", answer)

#     latency = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "rag_query",
#         "departments": allowed_departments,
#         "latency_ms": latency
#     })

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": 0.9,
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Answer generated from knowledge base",
#         "context_used": texts,
#         "session_id": session_id
#     }























# import time
# from typing import List

# from openai import OpenAI

# from app.core.vector_store import search_text
# from app.core.logger import logger
# from app.services.memory_service import memory

# from app.auth.permissions import resolve_departments

# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
#     MAX_PROMPT_TOTAL_CHARS,
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     scored = []
#     query_words = set(query.lower().split())

#     for chunk in chunks:

#         text = chunk["text"].lower()

#         score = sum(1 for word in query_words if word in text)

#         scored.append((score, chunk))

#     scored.sort(reverse=True, key=lambda x: x[0])

#     return [c[1] for c in scored[:top_k]]


# def build_context(chunks: List[str]):
#     return "\n\n".join(chunks)


# def calculate_confidence(chunks: List[str]):

#     total_chars = sum(len(c) for c in chunks)

#     if total_chars < 50:
#         return 0.2
#     if total_chars < 200:
#         return 0.5
#     if total_chars < 600:
#         return 0.75

#     return 0.9


# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind, an enterprise knowledge assistant.

# Rules:
# 1. Answer ONLY using the provided context.
# 2. Do NOT use outside knowledge.
# 3. If the answer cannot be found in the context,
# respond exactly with: "I don't know."
# """

#     history_text = ""

#     for msg in history:

#         role = msg["role"]
#         content = msg["content"]

#         if role == "user":
#             history_text += f"User: {content}\n"
#         else:
#             history_text += f"Assistant: {content}\n"

#     user_prompt = f"""
# Previous Conversation:
# {history_text}

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     response = client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt.strip()},
#             {"role": "user", "content": user_prompt.strip()},
#         ],
#         temperature=0.2,
#     )

#     return response.choices[0].message.content.strip()


# def generate_rag_answer(query: str, session_id: str, user_group_ids: list):

#     start_time = time.time()

#     history = memory.get_history(session_id)

#     # STEP 1 — determine allowed departments
#     allowed_departments = resolve_departments(user_group_ids)
#     print("USER GROUP IDS:", user_group_ids)
#     print("ALLOWED DEPARTMENTS:", allowed_departments)

#     # STEP 2 — retrieve only from allowed departments
#     try:

#         retrieved_chunks = search_text(
#             query,
#             department=allowed_departments,
#             limit=10
#         )

#     except Exception as e:

#         logger.error(f"Vector search failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Knowledge retrieval system unavailable.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id
#         }

#     if not retrieved_chunks:

#         return {
#             "question": query,
#             "answer": "I don't know.",
#             "confidence": 0.2,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Knowledge boundary triggered",
#             "context_used": [],
#             "session_id": session_id
#         }

#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]

#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
#         context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

#     answer = generate_answer_from_llm(query, context, history)

#     # FIX: if LLM says "I don't know"
#     if answer.strip().lower() == "i don't know.":

#         return {
#             "question": query,
#             "answer": "I don't know.",
#             "confidence": 0.2,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Knowledge boundary triggered",
#             "context_used": [],
#             "session_id": session_id
#         }

#     confidence = calculate_confidence(texts)

#     memory.add_message(session_id, "user", query)
#     memory.add_message(session_id, "assistant", answer)

#     latency = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "rag_query",
#         "latency_ms": latency
#     })

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": confidence,
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Answer generated from knowledge base",
#         "context_used": texts,
#         "session_id": session_id
#     }
























# import time
# from typing import List

# from openai import OpenAI

# from app.core.vector_store import search_text
# from app.core.logger import logger
# from app.services.memory_service import memory
# from app.auth.permissions import resolve_departments

# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
#     MAX_PROMPT_TOTAL_CHARS,
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # Query Rewriting
# # --------------------------------------------------

# def rewrite_query(query: str):

#     try:

#         prompt = f"""
# Rewrite the following enterprise search query to improve semantic retrieval.

# User Question:
# {query}

# Improved Query:
# """

#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )

#         rewritten = response.choices[0].message.content.strip()

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # Rerank
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     scored = []
#     query_words = set(query.lower().split())

#     for chunk in chunks:

#         text = chunk["text"].lower()

#         score = sum(1 for word in query_words if word in text)

#         scored.append((score, chunk))

#     scored.sort(reverse=True, key=lambda x: x[0])

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # Build Context
# # --------------------------------------------------

# def build_context(chunks: List[str]):
#     return "\n\n".join(chunks)


# # --------------------------------------------------
# # Confidence
# # --------------------------------------------------

# def calculate_confidence(chunks: List[str]):

#     total_chars = sum(len(c) for c in chunks)

#     if total_chars < 50:
#         return 0.2
#     if total_chars < 200:
#         return 0.5
#     if total_chars < 600:
#         return 0.75

#     return 0.9


# # --------------------------------------------------
# # LLM Answer
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind, an enterprise knowledge assistant.

# Rules:
# 1. Answer ONLY using the provided context.
# 2. Do NOT use outside knowledge.
# 3. If the answer cannot be found in the context,
# respond exactly with: "I don't know."
# """

#     history_text = ""

#     for msg in history:

#         role = msg["role"]
#         content = msg["content"]

#         if role == "user":
#             history_text += f"User: {content}\n"
#         else:
#             history_text += f"Assistant: {content}\n"

#     user_prompt = f"""
# Previous Conversation:
# {history_text}

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     response = client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt.strip()},
#             {"role": "user", "content": user_prompt.strip()},
#         ],
#         temperature=0.2,
#     )

#     return response.choices[0].message.content.strip()


# # --------------------------------------------------
# # RAG Pipeline
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list):

#     start_time = time.time()

#     history = memory.get_history(session_id)

#     allowed_departments = resolve_departments(user_group_ids)

#     print("USER GROUP IDS:", user_group_ids)
#     print("ALLOWED DEPARTMENTS:", allowed_departments)

#     rewritten_query = rewrite_query(query)

#     print("REWRITTEN QUERY:", rewritten_query)

#     try:

#         retrieved_chunks = search_text(
#             rewritten_query,
#             department=allowed_departments,
#             limit=10
#         )

#         # fallback if rewrite failed
#         if not retrieved_chunks:

#             print("Rewrite returned nothing → fallback to original query")

#             retrieved_chunks = search_text(
#                 query,
#                 department=allowed_departments,
#                 limit=10
#             )

#     except Exception as e:

#         logger.error(f"Vector search failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Knowledge retrieval system unavailable.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id
#         }

#     if not retrieved_chunks:

#         return {
#             "question": query,
#             "answer": "I don't know.",
#             "confidence": 0.2,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Knowledge boundary triggered",
#             "context_used": [],
#             "session_id": session_id
#         }

#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]

#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
#         context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

#     answer = generate_answer_from_llm(query, context, history)

#     if answer.strip().lower() == "i don't know.":

#         return {
#             "question": query,
#             "answer": "I don't know.",
#             "confidence": 0.2,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Knowledge boundary triggered",
#             "context_used": [],
#             "session_id": session_id
#         }

#     confidence = calculate_confidence(texts)

#     memory.add_message(session_id, "user", query)
#     memory.add_message(session_id, "assistant", answer)

#     latency = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "rag_query",
#         "latency_ms": latency
#     })

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": confidence,
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Answer generated from knowledge base",
#         "context_used": texts,
#         "session_id": session_id
#     }

































import time
from typing import List

from openai import OpenAI

from app.core.vector_store import search_text
from app.core.logger import logger
from app.services.memory_service import memory
from app.auth.permissions import resolve_departments

from app.config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    MAX_CONTEXT_CHARS,
    MAX_PROMPT_TOTAL_CHARS,
)

client = OpenAI(api_key=OPENAI_API_KEY)


# --------------------------------------------------
# Query Rewriting
# --------------------------------------------------

def rewrite_query(query: str):

    try:

        prompt = f"""
Rewrite the following enterprise search query to improve semantic retrieval.

User Question:
{query}

Improved Query:
"""

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        rewritten = response.choices[0].message.content.strip()

        return rewritten if rewritten else query

    except Exception:
        return query


# --------------------------------------------------
# Rerank
# --------------------------------------------------

def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

    scored = []
    query_words = set(query.lower().split())

    for chunk in chunks:

        text = chunk["text"].lower()

        score = sum(1 for word in query_words if word in text)

        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [c[1] for c in scored[:top_k]]


# --------------------------------------------------
# Build Context
# --------------------------------------------------

def build_context(chunks: List[str]):
    return "\n\n".join(chunks)


# --------------------------------------------------
# Confidence
# --------------------------------------------------

def calculate_confidence(chunks: List[str]):

    total_chars = sum(len(c) for c in chunks)

    if total_chars < 50:
        return 0.2
    if total_chars < 200:
        return 0.5
    if total_chars < 600:
        return 0.75

    return 0.9


# --------------------------------------------------
# LLM Answer
# --------------------------------------------------

def generate_answer_from_llm(query: str, context: str, history):

    system_prompt = """
You are AstraMind, an enterprise knowledge assistant.

Rules:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If the answer cannot be found in the context,
respond exactly with: "I don't know."
"""

    history_text = ""

    for msg in history:

        role = msg["role"]
        content = msg["content"]

        if role == "user":
            history_text += f"User: {content}\n"
        else:
            history_text += f"Assistant: {content}\n"

    user_prompt = f"""
Previous Conversation:
{history_text}

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


# --------------------------------------------------
# RAG Pipeline
# --------------------------------------------------

def generate_rag_answer(query: str, session_id: str, user_group_ids: list):

    start_time = time.time()

    allowed_departments = resolve_departments(user_group_ids)

    print("USER GROUP IDS:", user_group_ids)
    print("ALLOWED DEPARTMENTS:", allowed_departments)

    # --------------------------------------------------
    # FIX: isolate memory per user
    # --------------------------------------------------

    session_key = f"{session_id}_{'_'.join(map(str,user_group_ids))}"

    history = memory.get_history(session_key)

    rewritten_query = rewrite_query(query)

    print("REWRITTEN QUERY:", rewritten_query)

    try:

        retrieved_chunks = search_text(
            rewritten_query,
            department=allowed_departments,
            limit=10
        )

        if not retrieved_chunks:

            print("Rewrite returned nothing → fallback to original query")

            retrieved_chunks = search_text(
                query,
                department=allowed_departments,
                limit=10
            )

    except Exception as e:

        logger.error(f"Vector search failed: {str(e)}")

        return {
            "question": query,
            "answer": "Knowledge retrieval system unavailable.",
            "confidence": 0,
            "grounded": False,
            "sources": [],
            "evaluation": None,
            "context_used": [],
            "session_id": session_id
        }

    if not retrieved_chunks:

        return {
            "question": query,
            "answer": "I don't know.",
            "confidence": 0.2,
            "grounded": False,
            "sources": [],
            "evaluation": "Knowledge boundary triggered",
            "context_used": [],
            "session_id": session_id
        }

    reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

    texts = [chunk["text"] for chunk in reranked_chunks]

    sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

    context = build_context(texts)

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS]

    if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
        context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

    answer = generate_answer_from_llm(query, context, history)

    if answer.strip().lower() == "i don't know.":

        return {
            "question": query,
            "answer": "I don't know.",
            "confidence": 0.2,
            "grounded": False,
            "sources": [],
            "evaluation": "Knowledge boundary triggered",
            "context_used": [],
            "session_id": session_id
        }

    confidence = calculate_confidence(texts)

    memory.add_message(session_key, "user", query)
    memory.add_message(session_key, "assistant", answer)

    latency = round((time.time() - start_time) * 1000, 2)

    logger.info({
        "event": "rag_query",
        "latency_ms": latency
    })

    return {
        "question": query,
        "answer": answer,
        "confidence": confidence,
        "grounded": True,
        "sources": sources,
        "evaluation": "Answer generated from knowledge base",
        "context_used": texts,
        "session_id": session_id
    }
