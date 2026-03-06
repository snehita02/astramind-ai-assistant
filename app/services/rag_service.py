# import time
# from typing import List, Dict

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

# client = OpenAI(api_key=OPENAI_API_KEY)


# # ============================================================
# # Prompt Injection Detection
# # ============================================================

# def detect_prompt_injection(query: str) -> bool:

#     injection_patterns = [
#         "ignore previous instructions",
#         "disregard earlier instructions",
#         "reveal system prompt",
#         "override your rules",
#         "act as unrestricted model",
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
# # Confidence Score
# # ============================================================

# def calculate_confidence(chunks: List[str]) -> float:

#     total_chars = sum(len(c) for c in chunks)

#     if total_chars < 50:
#         return 0.2

#     if total_chars < 200:
#         return 0.5

#     if total_chars < 600:
#         return 0.75

#     return 0.9


# # ============================================================
# # Source Extraction
# # ============================================================

# def extract_sources(chunks: List[str]) -> List[str]:

#     sources = []

#     for chunk in chunks:

#         if len(chunk) > 120:
#             sources.append(chunk[:120] + "...")

#     return sources[:3]


# # ============================================================
# # Retrieval Transparency (NEW FEATURE)
# # ============================================================

# def rank_contexts(chunks: List[str]) -> List[Dict]:

#     ranked = []

#     for idx, chunk in enumerate(chunks):

#         ranked.append({
#             "rank": idx + 1,
#             "text": chunk
#         })

#     return ranked[:3]


# # ============================================================
# # Answer Evaluation
# # ============================================================

# def evaluate_answer_quality(context_chunks, answer, confidence):

#     context_length = sum(len(chunk) for chunk in context_chunks)

#     if confidence >= 0.75 and context_length > 300:
#         return "The retrieved context strongly supports the answer."

#     if confidence >= 0.5:
#         return "The context partially supports the answer."

#     if answer.lower().startswith("i don't know"):
#         return "The system correctly avoided answering due to insufficient context."

#     return "The answer may be unreliable due to weak or limited context."


# # ============================================================
# # LLM Generation
# # ============================================================

# def generate_answer_from_llm(query: str, context: str):

#     system_prompt = """
# You are an enterprise AI assistant.

# Rules:
# 1. Answer ONLY using the provided context.
# 2. Do NOT use outside knowledge.
# 3. If context is insufficient say: I don't know.
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
# # MAIN RAG PIPELINE
# # ============================================================

# def generate_rag_answer(query: str, session_id: str, department: str):

#     start_time = time.time()

#     if detect_prompt_injection(query):

#         return {
#             "question": query,
#             "answer": "Potential prompt injection detected. Request rejected.",
#             "confidence": 0,
#             "sources": [],
#             "top_contexts": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id,
#             "tool_used": None,
#             "evaluation_enabled": ENABLE_EVALUATION
#         }

#     try:

#         retrieved_chunks = search_text(query, department=department)

#     except Exception as e:

#         logger.error(f"Vector search failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Knowledge retrieval system unavailable.",
#             "confidence": 0,
#             "sources": [],
#             "top_contexts": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id,
#             "tool_used": None,
#             "evaluation_enabled": ENABLE_EVALUATION
#         }

#     if not retrieved_chunks:

#         return {
#             "question": query,
#             "answer": "No relevant documents found for this department.",
#             "confidence": 0,
#             "sources": [],
#             "top_contexts": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id,
#             "tool_used": None,
#             "evaluation_enabled": ENABLE_EVALUATION
#         }

#     context = build_context(retrieved_chunks)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
#         context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

#     answer = generate_answer_from_llm(query, context)

#     confidence = calculate_confidence(retrieved_chunks)

#     sources = extract_sources(retrieved_chunks)

#     top_contexts = rank_contexts(retrieved_chunks)

#     evaluation = None

#     if ENABLE_EVALUATION:
#         evaluation = evaluate_answer_quality(
#             retrieved_chunks,
#             answer,
#             confidence
#         )

#     latency = round((time.time() - start_time) * 1000, 2)

#     logger.info({
#         "event": "rag_query",
#         "department": department,
#         "latency_ms": latency
#     })

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": confidence,
#         "sources": sources,
#         "top_contexts": top_contexts,
#         "evaluation": evaluation,
#         "context_used": retrieved_chunks,
#         "session_id": session_id,
#         "tool_used": None,
#         "evaluation_enabled": ENABLE_EVALUATION
#     }




import time
from typing import List, Dict

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
# Confidence Score
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
# Retrieval Transparency
# ============================================================

def rank_contexts(chunks: List[str]) -> List[Dict]:

    ranked = []

    for idx, chunk in enumerate(chunks):

        ranked.append({
            "rank": idx + 1,
            "text": chunk
        })

    return ranked[:3]


# ============================================================
# Answer Evaluation
# ============================================================

def evaluate_answer_quality(context_chunks, answer, confidence):

    context_length = sum(len(chunk) for chunk in context_chunks)

    if confidence >= 0.75 and context_length > 300:
        return "The retrieved context strongly supports the answer."

    if confidence >= 0.5:
        return "The context partially supports the answer."

    if answer.lower().startswith("i don't know"):
        return "The system correctly avoided answering due to insufficient context."

    return "The answer may be unreliable due to weak or limited context."


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

    try:

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        logger.error(f"LLM failure: {str(e)}")
        return "The system is temporarily unavailable. Please try again later."


# ============================================================
# MAIN RAG PIPELINE
# ============================================================

def generate_rag_answer(query: str, session_id: str, department: str):

    start_time = time.time()

    # ------------------------------------------------------------
    # Prompt Injection Guard
    # ------------------------------------------------------------

    if detect_prompt_injection(query):

        return {
            "question": query,
            "answer": "Potential prompt injection detected. Request rejected.",
            "confidence": 0,
            "sources": [],
            "top_contexts": [],
            "evaluation": None,
            "context_used": [],
            "session_id": session_id,
            "tool_used": None,
            "evaluation_enabled": True if ENABLE_EVALUATION else False
        }

    # ------------------------------------------------------------
    # Vector Retrieval
    # ------------------------------------------------------------

    try:

        retrieved_chunks = search_text(query, department=department)

    except Exception as e:

        logger.error(f"Vector search failed: {str(e)}")

        return {
            "question": query,
            "answer": "Knowledge retrieval system unavailable.",
            "confidence": 0,
            "sources": [],
            "top_contexts": [],
            "evaluation": None,
            "context_used": [],
            "session_id": session_id,
            "tool_used": None,
            "evaluation_enabled": True if ENABLE_EVALUATION else False
        }

    # ------------------------------------------------------------
    # Empty Context Guard
    # ------------------------------------------------------------

    if not retrieved_chunks:

        return {
            "question": query,
            "answer": "No relevant documents found for this department.",
            "confidence": 0,
            "sources": [],
            "top_contexts": [],
            "evaluation": None,
            "context_used": [],
            "session_id": session_id,
            "tool_used": None,
            "evaluation_enabled": True if ENABLE_EVALUATION else False
        }

    # ------------------------------------------------------------
    # Build Context
    # ------------------------------------------------------------

    context = build_context(retrieved_chunks)

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS]

    total_prompt_size = len(context) + len(query)

    if total_prompt_size > MAX_PROMPT_TOTAL_CHARS:

        allowed_context_size = MAX_PROMPT_TOTAL_CHARS - len(query)

        if allowed_context_size > 0:
            context = context[:allowed_context_size]
        else:
            context = ""

    # ------------------------------------------------------------
    # LLM Answer
    # ------------------------------------------------------------

    answer = generate_answer_from_llm(query, context)

    # ------------------------------------------------------------
    # Confidence + Sources
    # ------------------------------------------------------------

    confidence = calculate_confidence(retrieved_chunks)

    sources = extract_sources(retrieved_chunks)

    top_contexts = rank_contexts(retrieved_chunks)

    # ------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------

    evaluation = None

    if ENABLE_EVALUATION:

        evaluation = evaluate_answer_quality(
            retrieved_chunks,
            answer,
            confidence
        )

    # ------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------

    latency = round((time.time() - start_time) * 1000, 2)

    logger.info({
        "event": "rag_query",
        "department": department,
        "latency_ms": latency
    })

    # ------------------------------------------------------------
    # Final Response
    # ------------------------------------------------------------

    return {
        "question": query,
        "answer": answer,
        "confidence": confidence,
        "sources": sources,
        "top_contexts": top_contexts,
        "evaluation": evaluation,
        "context_used": retrieved_chunks,
        "session_id": session_id,
        "tool_used": None,
        "evaluation_enabled": True if ENABLE_EVALUATION else False
    }