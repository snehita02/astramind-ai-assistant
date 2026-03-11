# import time
# from typing import List

# from openai import OpenAI

# from app.core.vector_store import search_text
# from app.core.logger import logger
# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
#     MAX_PROMPT_TOTAL_CHARS,
#     ENABLE_EVALUATION,
#     HALLUCINATION_STRICT_MODE
# )

# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)


# # ============================================================
# # Prompt Injection Detection
# # ============================================================

# def detect_prompt_injection(query: str) -> bool:
#     injection_patterns = [
#         "ignore previous instructions",
#         "disregard earlier instructions",
#         "you are no longer restricted",
#         "reveal system prompt",
#         "show hidden instructions",
#         "override your rules",
#         "act as an unrestricted model",
#         "bypass safety"
#     ]

#     query_lower = query.lower()
#     return any(pattern in query_lower for pattern in injection_patterns)


# # ============================================================
# # Context Builder
# # ============================================================

# def build_context(chunks: List[str]) -> str:
#     return "\n\n".join(chunks)


# # ============================================================
# # LLM Answer Generation (Protected)
# # ============================================================

# def generate_answer_from_llm(query: str, context: str) -> str:

#     system_prompt = """
# You are an enterprise AI assistant.

# Rules:
# 1. Answer ONLY using the provided context.
# 2. You may summarize or reasonably infer from the context.
# 3. Do NOT use external knowledge.
# 4. If the context does not contain enough information to answer, respond with:
#    "I don't know."
# """

#     user_prompt = f"""
# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=[
#                 {"role": "system", "content": system_prompt.strip()},
#                 {"role": "user", "content": user_prompt.strip()},
#             ],
#             temperature=0.2,
#         )

#         return response.choices[0].message.content.strip()

#     except Exception as e:
#         logger.error(f"LLM failure: {str(e)}")
#         return "The system is temporarily unavailable. Please try again later."


# # ============================================================
# # Main RAG Pipeline
# # ============================================================

# def generate_rag_answer(query: str, session_id: str, department: str):

#     start_time = time.time()

#     # ------------------------------------------------------------
#     # Step 1 — Prompt Injection Guard
#     # ------------------------------------------------------------
#     if detect_prompt_injection(query):
#         return {
#             "question": query,
#             "answer": "Potential prompt injection detected. Request rejected.",
#             "context_used": [],
#             "session_id": session_id,
#             "tool_used": None,
#             "evaluation_enabled": ENABLE_EVALUATION
#         }

#     # ------------------------------------------------------------
#     # Step 2 — Vector Retrieval (Protected)
#     # ------------------------------------------------------------
#     try:
#         retrieved_chunks = search_text(query, department=department)
#     except Exception as e:
#         logger.error(f"Vector store failure: {str(e)}")
#         return {
#             "question": query,
#             "answer": "Knowledge retrieval system unavailable.",
#             "context_used": [],
#             "session_id": session_id,
#             "tool_used": None,
#             "evaluation_enabled": ENABLE_EVALUATION
#         }

#     # ------------------------------------------------------------
#     # Step 3 — Empty Context Guard
#     # ------------------------------------------------------------
#     if not retrieved_chunks:
#         return {
#             "question": query,
#             "answer": "No relevant documents found for this department.",
#             "context_used": [],
#             "session_id": session_id,
#             "tool_used": None,
#             "evaluation_enabled": ENABLE_EVALUATION
#         }

#     # ------------------------------------------------------------
#     # Step 4 — Build Context
#     # ------------------------------------------------------------
#     context = build_context(retrieved_chunks)

#     # Context Size Cap
#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     # Total Prompt Size Cap
#     total_prompt_size = len(context) + len(query)
#     if total_prompt_size > MAX_PROMPT_TOTAL_CHARS:
#         allowed_context_size = MAX_PROMPT_TOTAL_CHARS - len(query)
#         context = context[:max(0, allowed_context_size)]

#     # ------------------------------------------------------------
#     # Step 5 — Weak Context Hallucination Guard
#     # ------------------------------------------------------------
#     combined_context_length = sum(len(chunk) for chunk in retrieved_chunks)

#     # Allow small factual answers
#     if combined_context_length < 20:
#         return {
#             "question": query,
#             "answer": "I don't know.",
#             "context_used": retrieved_chunks,
#             "session_id": session_id,
#             "tool_used": None,
#             "evaluation_enabled": ENABLE_EVALUATION
#         }

#     # ------------------------------------------------------------
#     # Step 6 — LLM Answer Generation
#     # ------------------------------------------------------------
#     answer = generate_answer_from_llm(query, context)

#     # ------------------------------------------------------------
#     # Step 7 — Strict Hallucination Mode
#     # ------------------------------------------------------------
#     if HALLUCINATION_STRICT_MODE:
#         if not answer.lower().startswith("i don't know") and combined_context_length < 150:
#             answer = "I don't know."

#     # ------------------------------------------------------------
#     # Step 8 — Logging
#     # ------------------------------------------------------------
#     total_time = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "rag_query",
#         "department": department,
#         "session_id": session_id,
#         "latency_ms": total_time
#     })

#     # ------------------------------------------------------------
#     # Step 9 — Final Response
#     # ------------------------------------------------------------
#     return {
#         "question": query,
#         "answer": answer,
#         "context_used": retrieved_chunks,
#         "session_id": session_id,
#         "tool_used": None,
#         "evaluation_enabled": ENABLE_EVALUATION
#     }





import time
from typing import List

from openai import OpenAI

from app.core.vector_store import search_text
from app.core.logger import logger
from app.config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    MAX_CONTEXT_CHARS,
    MAX_PROMPT_TOTAL_CHARS,
    ENABLE_EVALUATION,
    HALLUCINATION_STRICT_MODE
)

client = OpenAI(api_key=OPENAI_API_KEY)


# ============================================================
# Prompt Injection Detection
# ============================================================

def detect_prompt_injection(query: str) -> bool:

    injection_patterns = [
        "ignore previous instructions",
        "disregard earlier instructions",
        "reveal system prompt",
        "override your rules",
        "act as unrestricted model",
        "bypass safety"
    ]

    query_lower = query.lower()

    return any(pattern in query_lower for pattern in injection_patterns)


# ============================================================
# Context Builder
# ============================================================

def build_context(chunks: List[str]) -> str:
    return "\n\n".join(chunks)


# ============================================================
# Confidence Score Calculation
# ============================================================

def calculate_confidence(chunks: List[str]) -> float:

    total_chars = sum(len(c) for c in chunks)

    if total_chars < 50:
        return 0.2

    if total_chars < 200:
        return 0.5

    if total_chars < 600:
        return 0.75

    return 0.9


# ============================================================
# Source Extraction
# ============================================================

def extract_sources(chunks: List[str]) -> List[str]:

    sources = []

    for chunk in chunks:
        if len(chunk) > 120:
            sources.append(chunk[:120] + "...")

    return sources[:3]


# ============================================================
# LLM Generation
# ============================================================

def generate_answer_from_llm(query: str, context: str):

    system_prompt = """
You are an enterprise AI assistant.

Rules:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If context is insufficient say: I don't know.
"""

    user_prompt = f"""
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


# ============================================================
# MAIN RAG PIPELINE
# ============================================================

def generate_rag_answer(query: str, session_id: str, department: str):

    start_time = time.time()

    if detect_prompt_injection(query):

        return {
            "question": query,
            "answer": "Potential prompt injection detected. Request rejected.",
            "context_used": [],
            "confidence": 0,
            "sources": [],
            "session_id": session_id,
            "tool_used": None,
            "evaluation_enabled": ENABLE_EVALUATION
        }

    try:

        retrieved_chunks = search_text(query, department=department)

    except Exception as e:

        logger.error(f"Vector search failed: {str(e)}")

        return {
            "question": query,
            "answer": "Knowledge retrieval system unavailable.",
            "context_used": [],
            "confidence": 0,
            "sources": [],
            "session_id": session_id,
            "tool_used": None,
            "evaluation_enabled": ENABLE_EVALUATION
        }

    if not retrieved_chunks:

        return {
            "question": query,
            "answer": "No relevant documents found for this department.",
            "context_used": [],
            "confidence": 0,
            "sources": [],
            "session_id": session_id,
            "tool_used": None,
            "evaluation_enabled": ENABLE_EVALUATION
        }

    context = build_context(retrieved_chunks)

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS]

    if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
        context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

    answer = generate_answer_from_llm(query, context)

    confidence = calculate_confidence(retrieved_chunks)

    sources = extract_sources(retrieved_chunks)

    latency = round((time.time() - start_time) * 1000, 2)

    logger.info({
        "event": "rag_query",
        "department": department,
        "latency_ms": latency
    })

    return {
        "question": query,
        "answer": answer,
        "confidence": confidence,
        "sources": sources,
        "context_used": retrieved_chunks,
        "session_id": session_id,
        "tool_used": None,
        "evaluation_enabled": ENABLE_EVALUATION
    }