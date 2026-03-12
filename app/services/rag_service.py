# import time
# from typing import List, Union

# from openai import OpenAI

# from app.core.vector_store import search_text
# from app.core.logger import logger
# from app.services.memory_service import memory

# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
#     MAX_PROMPT_TOTAL_CHARS,
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# def detect_prompt_injection(query: str):

#     patterns = [
#         "ignore previous instructions",
#         "reveal system prompt",
#         "override your rules",
#         "act as unrestricted model",
#         "bypass safety"
#     ]

#     q = query.lower()

#     return any(p in q for p in patterns)


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
# 3. If context is insufficient say: I don't know.
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


# def normalize_answer(text: str):

#     return (
#         text.lower()
#         .replace("’", "'")
#         .replace("`", "'")
#         .strip()
#     )


# def is_unknown_answer(answer: str):

#     normalized = normalize_answer(answer)

#     return (
#         "i don't know" in normalized
#         or "cannot determine" in normalized
#         or "not enough information" in normalized
#         or normalized == "unknown"
#     )


# def generate_rag_answer(query: str, session_id: str, department: Union[str, List[str]]):

#     start_time = time.time()

#     if detect_prompt_injection(query):

#         return {
#             "question": query,
#             "answer": "Potential prompt injection detected.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id
#         }

#     history = memory.get_history(session_id)

#     try:

#         if isinstance(department, list):

#             retrieved_chunks = []

#             for dept in department:

#                 chunks = search_text(query, department=dept, limit=10)

#                 retrieved_chunks.extend(chunks)

#         else:

#             retrieved_chunks = search_text(query, department=department, limit=20)

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
#             "answer": "I could not find this information in your accessible knowledge base.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": None,
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

#     confidence = calculate_confidence(texts)

#     if confidence < 0.3:

#         return {
#             "question": query,
#             "answer": "I could not find reliable information in your accessible knowledge base.",
#             "confidence": confidence,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Knowledge boundary triggered",
#             "context_used": [],
#             "session_id": session_id
#         }

#     answer = generate_answer_from_llm(query, context, history)

#     memory.add_message(session_id, "user", query)
#     memory.add_message(session_id, "assistant", answer)

#     latency = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "rag_query",
#         "departments": department,
#         "latency_ms": latency
#     })

#     if is_unknown_answer(answer):

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

# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
#     MAX_PROMPT_TOTAL_CHARS,
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# def detect_prompt_injection(query: str):

#     patterns = [
#         "ignore previous instructions",
#         "reveal system prompt",
#         "override your rules",
#         "act as unrestricted model",
#         "bypass safety"
#     ]

#     q = query.lower()

#     return any(p in q for p in patterns)


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
# 3. If context is insufficient say: I don't know.
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


# def normalize_answer(text: str):

#     return (
#         text.lower()
#         .replace("’", "'")
#         .replace("`", "'")
#         .strip()
#     )


# def is_unknown_answer(answer: str):

#     normalized = normalize_answer(answer)

#     return (
#         "i don't know" in normalized
#         or "cannot determine" in normalized
#         or "not enough information" in normalized
#         or normalized == "unknown"
#     )


# def generate_rag_answer(query: str, session_id: str, departments: list):

#     start_time = time.time()

#     if detect_prompt_injection(query):

#         return {
#             "question": query,
#             "answer": "Potential prompt injection detected.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id
#         }

#     history = memory.get_history(session_id)

#     retrieved_chunks = []

#     try:

#         for dept in departments:

#             results = search_text(query, department=dept, limit=10)

#             retrieved_chunks.extend(results)

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

#     confidence = calculate_confidence(texts)

#     answer = generate_answer_from_llm(query, context, history)

#     memory.add_message(session_id, "user", query)
#     memory.add_message(session_id, "assistant", answer)

#     latency = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "rag_query",
#         "departments": departments,
#         "latency_ms": latency
#     })

#     if is_unknown_answer(answer):

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

# # FIXED IMPORT (matches your vector_store.py)
# from app.core.vector_store import search_text

# from app.core.logger import logger
# from app.services.memory_service import memory

# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
#     MAX_PROMPT_TOTAL_CHARS,
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # ---------------------------------------------------
# # PROMPT INJECTION DETECTION
# # ---------------------------------------------------

# def detect_prompt_injection(query: str):

#     patterns = [
#         "ignore previous instructions",
#         "reveal system prompt",
#         "override your rules",
#         "act as unrestricted model",
#         "bypass safety"
#     ]

#     q = query.lower()

#     return any(p in q for p in patterns)


# # ---------------------------------------------------
# # RERANK CHUNKS
# # ---------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     scored = []

#     query_words = set(query.lower().split())

#     for chunk in chunks:

#         text = chunk["text"].lower()

#         score = sum(1 for word in query_words if word in text)

#         scored.append((score, chunk))

#     scored.sort(reverse=True, key=lambda x: x[0])

#     return [c[1] for c in scored[:top_k]]


# # ---------------------------------------------------
# # BUILD CONTEXT
# # ---------------------------------------------------

# def build_context(chunks: List[str]):

#     return "\n\n".join(chunks)


# # ---------------------------------------------------
# # CONFIDENCE CALCULATION
# # ---------------------------------------------------

# def calculate_confidence(chunks: List[str]):

#     total_chars = sum(len(c) for c in chunks)

#     if total_chars < 50:
#         return 0.2
#     if total_chars < 200:
#         return 0.5
#     if total_chars < 600:
#         return 0.75

#     return 0.9


# # ---------------------------------------------------
# # DEPARTMENT DETECTION
# # ---------------------------------------------------

# def detect_department(query: str):

#     q = query.lower()

#     if "leave" in q or "vacation" in q or "benefits" in q:
#         return "hr"

#     if "expense" in q or "reimbursement" in q or "invoice" in q:
#         return "finance"

#     if "deployment" in q or "code" in q:
#         return "engineering"

#     if "research" in q or "model" in q:
#         return "research"

#     return "general"


# # ---------------------------------------------------
# # LLM GENERATION
# # ---------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind, an enterprise knowledge assistant.

# Rules:
# 1. Answer ONLY using the provided context.
# 2. Do NOT use outside knowledge.
# 3. If context is insufficient say: I don't know.
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


# # ---------------------------------------------------
# # NORMALIZATION
# # ---------------------------------------------------

# def normalize_answer(text: str):

#     return (
#         text.lower()
#         .replace("’", "'")
#         .replace("`", "'")
#         .strip()
#     )


# def is_unknown_answer(answer: str):

#     normalized = normalize_answer(answer)

#     return (
#         "i don't know" in normalized
#         or "cannot determine" in normalized
#         or "not enough information" in normalized
#         or normalized == "unknown"
#     )


# # ---------------------------------------------------
# # MAIN RAG PIPELINE
# # ---------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, departments: list):

#     start_time = time.time()

#     # PROMPT INJECTION CHECK

#     if detect_prompt_injection(query):

#         return {
#             "question": query,
#             "answer": "Potential prompt injection detected.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id
#         }

#     history = memory.get_history(session_id)

#     detected_department = detect_department(query)

#     # ---------------------------------------------------
#     # DEPARTMENT ACCESS CONTROL
#     # ---------------------------------------------------

#     if detected_department not in departments:

#         return {
#             "question": query,
#             "answer": f"This question belongs to the {detected_department.upper()} department. Please contact the {detected_department.upper()} department POC.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Department access restricted",
#             "context_used": [],
#             "session_id": session_id
#         }

#     retrieved_chunks = []

#     try:

#         results = search_text(query, department=detected_department, limit=10)

#         retrieved_chunks.extend(results)

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

#     confidence = calculate_confidence(texts)

#     answer = generate_answer_from_llm(query, context, history)

#     memory.add_message(session_id, "user", query)
#     memory.add_message(session_id, "assistant", answer)

#     latency = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "rag_query",
#         "departments": departments,
#         "latency_ms": latency
#     })

#     if is_unknown_answer(answer):

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
from app.services.query_classifier import classify_query

from app.config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    MAX_CONTEXT_CHARS,
    MAX_PROMPT_TOTAL_CHARS,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

    scored = []
    query_words = set(query.lower().split())

    for chunk in chunks:

        text = chunk["text"].lower()

        score = sum(1 for word in query_words if word in text)

        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [c[1] for c in scored[:top_k]]


def build_context(chunks: List[str]):
    return "\n\n".join(chunks)


def calculate_confidence(chunks: List[str]):

    total_chars = sum(len(c) for c in chunks)

    if total_chars < 50:
        return 0.2
    if total_chars < 200:
        return 0.5
    if total_chars < 600:
        return 0.75

    return 0.9


def generate_answer_from_llm(query: str, context: str, history):

    system_prompt = """
You are AstraMind, an enterprise knowledge assistant.

Rules:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If context is insufficient say: I don't know.
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


def generate_rag_answer(query: str, session_id: str, user_group_ids: list):

    start_time = time.time()

    history = memory.get_history(session_id)

    # STEP 1 — Determine allowed departments
    allowed_departments = resolve_departments(user_group_ids)

    # STEP 2 — Classify query department
    predicted_department = classify_query(query)

    # STEP 3 — Permission check
    if predicted_department not in allowed_departments:

        return {
            "question": query,
            "answer": "You do not have permission to access this department. Please contact your administrator for access.",
            "confidence": 0,
            "grounded": False,
            "sources": [],
            "evaluation": "Permission denied",
            "context_used": [],
            "session_id": session_id
        }

    retrieved_chunks = []

    try:

        results = search_text(query, department=predicted_department, limit=10)

        retrieved_chunks.extend(results)

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

    confidence = calculate_confidence(texts)

    answer = generate_answer_from_llm(query, context, history)

    memory.add_message(session_id, "user", query)
    memory.add_message(session_id, "assistant", answer)

    latency = round((time.time() - start_time) * 1000, 2)

    logger.info({
        "event": "rag_query",
        "department": predicted_department,
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