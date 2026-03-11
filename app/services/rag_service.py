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


# def detect_prompt_injection(query: str) -> bool:

#     patterns = [
#         "ignore previous instructions",
#         "reveal system prompt",
#         "override your rules",
#         "act as unrestricted model",
#         "bypass safety"
#     ]

#     q = query.lower()

#     return any(p in q for p in patterns)


# def build_context(chunks: List[str]) -> str:
#     return "\n\n".join(chunks)


# def calculate_confidence(chunks: List[str]) -> float:

#     total_chars = sum(len(c) for c in chunks)

#     if total_chars < 50:
#         return 0.2
#     if total_chars < 200:
#         return 0.5
#     if total_chars < 600:
#         return 0.75

#     return 0.9


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
#         return "The system is temporarily unavailable."


# def generate_rag_answer(query: str, session_id: str, department: str):

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

#     try:

#         retrieved_chunks = search_text(query, department=department)

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
#             "answer": "I could not find information about this in the knowledge base.",
#             "confidence": 0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": None,
#             "context_used": [],
#             "session_id": session_id
#         }

#     texts = [chunk["text"] for chunk in retrieved_chunks]

#     sources = list({chunk["source"] for chunk in retrieved_chunks})[:3]

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
#         context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

#     answer = generate_answer_from_llm(query, context)

#     confidence = calculate_confidence(texts)

#     grounded = confidence > 0.3

#     evaluation = None

#     if ENABLE_EVALUATION:

#         if confidence >= 0.75:
#             evaluation = "The context strongly supports the answer."
#         elif confidence >= 0.5:
#             evaluation = "The context partially supports the answer."
#         else:
#             evaluation = "The answer may be unreliable."

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
#         "grounded": grounded,
#         "sources": sources,
#         "evaluation": evaluation,
#         "context_used": texts,
#         "session_id": session_id
#     }


import time
from typing import List

from openai import OpenAI

from app.core.vector_store import search_text
from app.core.logger import logger
from app.services.memory_service import memory

from app.config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    MAX_CONTEXT_CHARS,
    MAX_PROMPT_TOTAL_CHARS,
    ENABLE_EVALUATION
)

client = OpenAI(api_key=OPENAI_API_KEY)


def detect_prompt_injection(query: str):

    patterns = [
        "ignore previous instructions",
        "reveal system prompt",
        "override your rules",
        "act as unrestricted model",
        "bypass safety"
    ]

    q = query.lower()

    return any(p in q for p in patterns)


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
You are an enterprise AI assistant.

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
        return "The system is temporarily unavailable."


def generate_rag_answer(query: str, session_id: str, department: str):

    start_time = time.time()

    if detect_prompt_injection(query):

        return {
            "question": query,
            "answer": "Potential prompt injection detected.",
            "confidence": 0,
            "grounded": False,
            "sources": [],
            "evaluation": None,
            "context_used": [],
            "session_id": session_id
        }

    history = memory.get_history(session_id)

    try:

        retrieved_chunks = search_text(query, department=department)

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
            "answer": "I could not find information about this in the knowledge base.",
            "confidence": 0,
            "grounded": False,
            "sources": [],
            "evaluation": None,
            "context_used": [],
            "session_id": session_id
        }

    # texts = [chunk["text"] for chunk in retrieved_chunks]

    # sources = list({chunk["source"] for chunk in retrieved_chunks})[:3]
    # Handle both string chunks and dictionary chunks
    texts = []
    sources = []

    for chunk in retrieved_chunks:

        if isinstance(chunk, dict):
            texts.append(chunk.get("text", ""))
            if "source" in chunk:
                sources.append(chunk["source"])

        else:
            texts.append(chunk)

    sources = list(set(sources))[:3]

    context = build_context(texts)

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS]

    if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
        context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

    answer = generate_answer_from_llm(query, context, history)

    confidence = calculate_confidence(texts)

    grounded = confidence > 0.3

    evaluation = None

    if ENABLE_EVALUATION:

        if confidence >= 0.75:
            evaluation = "The context strongly supports the answer."
        elif confidence >= 0.5:
            evaluation = "The context partially supports the answer."
        else:
            evaluation = "The answer may be unreliable."

    memory.add_message(session_id, "user", query)
    memory.add_message(session_id, "assistant", answer)

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
        "grounded": grounded,
        "sources": sources,
        "evaluation": evaluation,
        "context_used": texts,
        "session_id": session_id
    }