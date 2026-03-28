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

#     allowed_departments = resolve_departments(user_group_ids)

#     print("USER GROUP IDS:", user_group_ids)
#     print("ALLOWED DEPARTMENTS:", allowed_departments)

#     # --------------------------------------------------
#     # FIX: isolate memory per user
#     # --------------------------------------------------

#     session_key = f"{session_id}_{'_'.join(map(str,user_group_ids))}"

#     history = memory.get_history(session_key)

#     rewritten_query = rewrite_query(query)

#     print("REWRITTEN QUERY:", rewritten_query)

#     try:

#         retrieved_chunks = search_text(
#             rewritten_query,
#             department=allowed_departments,
#             limit=10
#         )

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

#     memory.add_message(session_key, "user", query)
#     memory.add_message(session_key, "assistant", answer)

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

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()

#         keyword_score = sum(1 for w in query_words if w in text)

#         semantic_score = chunk.get("score", 0)

#         final_score = semantic_score + (keyword_score * 0.05)

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# 1. Use ONLY the information in the provided context.
# 2. You may summarize or paraphrase the context to answer the question.
# 3. If relevant information exists in the context, provide the answer clearly.
# 4. Only respond "I don't know." if the context truly contains no relevant information.
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

# Answer clearly using the context above.
# """

#     response = client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt.strip()},
#             {"role": "user", "content": user_prompt.strip()},
#         ],
#         temperature=0.1,
#     )

#     return response.choices[0].message.content.strip()


# # --------------------------------------------------
# # RAG Pipeline
# # --------------------------------------------------

# def generate_rag_answer(
#     query: str,
#     session_id: str,
#     user_group_ids: list,
#     allowed_departments=None
# ):

#     start_time = time.time()

#     # Resolve departments if not provided
#     if allowed_departments is None:
#         allowed_departments = resolve_departments(user_group_ids)

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     session_key = f"{session_id}_{'_'.join(map(str,user_group_ids))}"

#     history = memory.get_history(session_key)

#     rewritten_query = rewrite_query(query)

#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # --------------------------------------------------
#     # Retrieval
#     # --------------------------------------------------

#     try:

#         retrieved_chunks = search_text(
#             rewritten_query,
#             department=allowed_departments,
#             limit=10
#         )

#         # Fallback to original query
#         if not retrieved_chunks:

#             logger.info("Rewrite returned nothing → fallback to original query")

#             retrieved_chunks = search_text(
#                 query,
#                 department=allowed_departments,
#                 limit=10
#             )

#         # FINAL fallback → global search
#         if not retrieved_chunks:

#             logger.info("Department search empty → fallback to global search")

#             retrieved_chunks = search_text(
#                 query,
#                 department=None,
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
#             "sources": sources,              # ✅ keep sources
#             "evaluation": "LLM could not answer from context",
#             "context_used": texts,           # ✅ KEEP CONTEXT (CRITICAL)
#             "session_id": session_id
#         }

#     confidence = calculate_confidence(texts)

#     memory.add_message(session_key, "user", query)
#     memory.add_message(session_key, "assistant", answer)

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

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()

#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         # --------------------------------------------------
#         # TYPE PRIORITY (🔥 KEY FIX)
#         # --------------------------------------------------

#         chunk_type = chunk.get("type", "")

#         if chunk_type == "pdf":
#             type_boost = 0.5
#         elif chunk_type == "url":
#             type_boost = 0.3
#         elif chunk_type == "repo":
#             type_boost = -0.2   # 🔥 penalize repos
#         else:
#             type_boost = 0

#         # --------------------------------------------------
#         # FINAL SCORE
#         # --------------------------------------------------

#         final_score = semantic_score + (keyword_score * 0.05) + type_boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# 1. Answer using ONLY the provided context.
# 2. Extract the exact answer from the context if present.
# 3. Be concise and direct.
# 4. If the answer is clearly present, DO NOT say "I don't know".
# 5. Only say "I don't know." if absolutely no relevant information exists.
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

# # def generate_rag_answer(
# #     query: str,
# #     session_id: str,
# #     user_group_ids: list,
# #     allowed_departments=None
# # ):

# #     start_time = time.time()

# #     if allowed_departments is None:
# #         allowed_departments = resolve_departments(user_group_ids)

# #     logger.info(f"USER GROUP IDS: {user_group_ids}")
# #     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

# #     session_key = f"{session_id}_{'_'.join(map(str,user_group_ids))}"

# #     history = memory.get_history(session_key)

# #     rewritten_query = rewrite_query(query)

# #     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

# #     # --------------------------------------------------
# #     # 🔥 INTENT DETECTION (KEY FIX)
# #     # --------------------------------------------------

# #     business_keywords = [
# #         "leave", "policy", "benefits", "salary", "vacation",
# #         "sick", "employee", "hr", "rules", "guidelines"
# #     ]

# #     is_business_query = any(k in query.lower() for k in business_keywords)

# #     try:

# #         retrieved_chunks = search_text(
# #             rewritten_query,
# #             department=allowed_departments,
# #             limit=20   # increase pool
# #         )

# #         if not retrieved_chunks:

# #             retrieved_chunks = search_text(
# #                 query,
# #                 department=allowed_departments,
# #                 limit=20
# #             )

# #         if not retrieved_chunks:

# #             retrieved_chunks = search_text(
# #                 query,
# #                 department=None,
# #                 limit=20
# #             )

# #     except Exception as e:

# #         logger.error(f"Vector search failed: {str(e)}")

# #         return {
# #             "question": query,
# #             "answer": "Knowledge retrieval system unavailable.",
# #             "confidence": 0,
# #             "grounded": False,
# #             "sources": [],
# #             "evaluation": None,
# #             "context_used": [],
# #             "session_id": session_id
# #         }

# #     if not retrieved_chunks:

# #         return {
# #             "question": query,
# #             "answer": "I don't know.",
# #             "confidence": 0.2,
# #             "grounded": False,
# #             "sources": [],
# #             "evaluation": "Knowledge boundary triggered",
# #             "context_used": [],
# #             "session_id": session_id
# #         }

# #     # --------------------------------------------------
# #     # 🔥 FILTER OUT REPOS FOR BUSINESS QUESTIONS
# #     # --------------------------------------------------

# #     if is_business_query:

# #         filtered = [c for c in retrieved_chunks if c.get("type") != "repo"]

# #         # fallback if everything removed
# #         if filtered:
# #             retrieved_chunks = filtered

# #     # --------------------------------------------------
# #     # RERANK
# #     # --------------------------------------------------

# #     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

# #     texts = [chunk["text"] for chunk in reranked_chunks]

# #     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

# #     context = build_context(texts)

# #     # DEBUG
# #     print("\n========= RAG DEBUG =========")
# #     for i, t in enumerate(texts):
# #         print(f"\nChunk {i+1}:\n{t[:300]}")
# #     print("================================\n")

# #     # TRIM
# #     if len(context) > MAX_CONTEXT_CHARS:
# #         context = context[:MAX_CONTEXT_CHARS]

# #     if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
# #         context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

# #     # LLM
# #     answer = generate_answer_from_llm(query, context, history)

# #     if answer.strip().lower() == "i don't know.":

# #         return {
# #             "question": query,
# #             "answer": "I don't know.",
# #             "confidence": 0.2,
# #             "grounded": False,
# #             "sources": sources,
# #             "evaluation": "LLM could not answer from context",
# #             "context_used": texts,
# #             "session_id": session_id
# #         }

# #     confidence = calculate_confidence(texts)

# #     memory.add_message(session_key, "user", query)
# #     memory.add_message(session_key, "assistant", answer)

# #     latency = round((time.time() - start_time) * 1000, 2)

# #     logger.info({
# #         "event": "rag_query",
# #         "latency_ms": latency
# #     })

# #     return {
# #         "question": query,
# #         "answer": answer,
# #         "confidence": confidence,
# #         "grounded": True,
# #         "sources": sources,
# #         "evaluation": "Answer generated from knowledge base",
# #         "context_used": texts,
# #         "session_id": session_id
# #     }

# def generate_rag_answer(
#     query: str,
#     session_id: str,
#     user_group_ids: list,
#     allowed_departments=None
# ):

#     start_time = time.time()

#     if allowed_departments is None:
#         allowed_departments = resolve_departments(user_group_ids)

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     session_key = f"{session_id}_{'_'.join(map(str,user_group_ids))}"
#     history = memory.get_history(session_key)

#     rewritten_query = rewrite_query(query)

#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # --------------------------------------------------
#     # STAGE 1 → SEARCH ONLY PDF + URL
#     # --------------------------------------------------

#     try:

#         all_chunks = search_text(
#             rewritten_query,
#             department=allowed_departments,
#             limit=20
#         )

#         # Filter only business docs
#         stage1_chunks = [
#             c for c in all_chunks
#             if c.get("type") in ["pdf", "url"]
#         ]

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

#     # --------------------------------------------------
#     # IF STAGE 1 HAS RESULTS → USE IT
#     # --------------------------------------------------

#     if stage1_chunks:

#         logger.info("Using Stage 1 (PDF + URL)")

#         reranked_chunks = rerank_chunks(query, stage1_chunks, top_k=5)

#     else:

#         # --------------------------------------------------
#         # STAGE 2 → FALLBACK TO REPO
#         # --------------------------------------------------

#         logger.info("Fallback to Stage 2 (REPO)")

#         reranked_chunks = rerank_chunks(query, all_chunks, top_k=5)

#     # --------------------------------------------------
#     # BUILD CONTEXT
#     # --------------------------------------------------

#     texts = [chunk["text"] for chunk in reranked_chunks]
#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]
#     context = build_context(texts)

#     # DEBUG
#     print("\n========= RAG DEBUG =========")
#     for i, t in enumerate(texts):
#         print(f"\nChunk {i+1}:\n{t[:300]}")
#     print("================================\n")

#     # TRIM
#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     if len(context) + len(query) > MAX_PROMPT_TOTAL_CHARS:
#         context = context[:MAX_PROMPT_TOTAL_CHARS - len(query)]

#     # --------------------------------------------------
#     # GENERATE ANSWER
#     # --------------------------------------------------

#     answer = generate_answer_from_llm(query, context, history)

#     if answer.strip().lower() == "i don't know.":

#         return {
#             "question": query,
#             "answer": "I don't know.",
#             "confidence": 0.2,
#             "grounded": False,
#             "sources": sources,
#             "evaluation": "LLM could not answer from context",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     confidence = calculate_confidence(texts)

#     memory.add_message(session_key, "user", query)
#     memory.add_message(session_key, "assistant", answer)

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

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         # 🔥 SOURCE-BASED BOOST (FINAL FIX)
#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# 1. Answer using ONLY the provided context.
# 2. Extract the exact answer if present.
# 3. Be direct.
# 4. Do NOT say "I don't know" if answer exists.
# """

#     history_text = ""
#     for msg in history:
#         role = msg["role"]
#         content = msg["content"]
#         history_text += f"{role}: {content}\n"

#     user_prompt = f"""
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

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     # if allowed_departments is None:
#     #     allowed_departments = resolve_departments(user_group_ids)
#     allowed_departments = None

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     history = memory.get_history(session_id)

#     rewritten_query = rewrite_query(query)

#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # 🔥 GET MORE RESULTS (IMPORTANT)
#     retrieved_chunks = search_text(
#         rewritten_query,
#         department=allowed_departments,
#         limit=30
#     )

#     # 🔥 FORCE REMOVE GITHUB FIRST (CRITICAL FIX)
#     non_repo_chunks = [
#         c for c in retrieved_chunks
#         if "github" not in c.get("source", "").lower()
#     ]

#     if non_repo_chunks:
#         retrieved_chunks = non_repo_chunks

#     # RERANK
#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]
#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     # DEBUG
#     print("\n===== FINAL CONTEXT =====")
#     for i, t in enumerate(texts):
#         print(f"\nChunk {i+1}:\n{t[:300]}")
#     print("========================\n")

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     answer = generate_answer_from_llm(query, context, history)

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": calculate_confidence(texts),
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Final fixed pipeline",
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

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         # Source-based weighting
#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# 1. Answer using ONLY the provided context.
# 2. Extract the exact answer if present.
# 3. Be direct.
# 4. Do NOT say "I don't know" if answer exists.
# """

#     history_text = ""
#     for msg in history:
#         role = msg["role"]
#         content = msg["content"]
#         history_text += f"{role}: {content}\n"

#     user_prompt = f"""
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

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     # ✅ PROPER DEPARTMENT RESOLUTION
#     if allowed_departments is None:
#         allowed_departments = resolve_departments(user_group_ids)

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     history = memory.get_history(session_id)

#     rewritten_query = rewrite_query(query)

#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # 🔍 Retrieve chunks based on department access
#     retrieved_chunks = search_text(
#         rewritten_query,
#         department=allowed_departments,
#         limit=30
#     )

#     # 🚫 Remove GitHub repo noise
#     non_repo_chunks = [
#         c for c in retrieved_chunks
#         if "github" not in c.get("source", "").lower()
#     ]

#     if non_repo_chunks:
#         retrieved_chunks = non_repo_chunks

#     # 📊 Rerank
#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]
#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     # DEBUG LOG
#     print("\n===== FINAL CONTEXT =====")
#     for i, t in enumerate(texts):
#         print(f"\nChunk {i+1}:\n{t[:300]}")
#     print("========================\n")

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     answer = generate_answer_from_llm(query, context, history)

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": calculate_confidence(texts),
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Department-filtered pipeline",
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

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         # Source-based weighting
#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# 1. Answer using ONLY the provided context.
# 2. Extract the exact answer if present.
# 3. Be direct.
# 4. Do NOT say "I don't know" if answer exists.
# """

#     history_text = ""
#     for msg in history:
#         role = msg["role"]
#         content = msg["content"]
#         history_text += f"{role}: {content}\n"

#     user_prompt = f"""
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

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     # ✅ Resolve allowed departments
#     if allowed_departments is None:
#         allowed_departments = resolve_departments(user_group_ids)

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     history = memory.get_history(session_id)

#     rewritten_query = rewrite_query(query)

#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # 🔍 Retrieve chunks
#     retrieved_chunks = search_text(
#         rewritten_query,
#         department=allowed_departments,
#         limit=30
#     )

#     # 🔒 DOUBLE SAFETY FILTER (CRITICAL)
#     retrieved_chunks = [
#         c for c in retrieved_chunks
#         if c.get("department") in allowed_departments
#     ]

#     # 🚫 HARD ACCESS DENIAL (STEP 35 FIX)
#     if not retrieved_chunks:
#         logger.warning("ACCESS DENIED: No data found for allowed departments")

#         return {
#             "question": query,
#             "answer": "You do not have access to this department. Contact your administrator.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Access denied",
#             "context_used": [],
#             "session_id": session_id
#         }

#     # 🚫 Remove GitHub noise
#     non_repo_chunks = [
#         c for c in retrieved_chunks
#         if "github" not in c.get("source", "").lower()
#     ]

#     if non_repo_chunks:
#         retrieved_chunks = non_repo_chunks

#     # 📊 Rerank
#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]
#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     # DEBUG LOG
#     print("\n===== FINAL CONTEXT =====")
#     for i, t in enumerate(texts):
#         print(f"\nChunk {i+1}:\n{t[:300]}")
#     print("========================\n")

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     answer = generate_answer_from_llm(query, context, history)

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": calculate_confidence(texts),
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Department-filtered pipeline",
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

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         # Source-based weighting
#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# 1. Answer using ONLY the provided context.
# 2. Extract the exact answer if present.
# 3. Be direct.
# 4. Do NOT say "I don't know" if answer exists.
# """

#     history_text = ""
#     for msg in history:
#         role = msg["role"]
#         content = msg["content"]
#         history_text += f"{role}: {content}\n"

#     user_prompt = f"""
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

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     # ✅ Resolve allowed departments
#     if allowed_departments is None:
#         allowed_departments = resolve_departments(user_group_ids)

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     history = memory.get_history(session_id)

#     rewritten_query = rewrite_query(query)

#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # 🔍 Retrieve chunks
#     retrieved_chunks = search_text(
#         rewritten_query,
#         department=allowed_departments,
#         limit=30
#     )

#     # 🔒 DOUBLE SAFETY FILTER (CRITICAL)
#     retrieved_chunks = [
#         c for c in retrieved_chunks
#         if c.get("department") in allowed_departments
#     ]

#     # 🚫 HARD ACCESS DENIAL (STEP 35 FIX)
#     if not retrieved_chunks:
#         logger.warning("ACCESS DENIED: No data found for allowed departments")

#         return {
#             "question": query,
#             "answer": "You do not have access to this department. Contact your administrator.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Access denied",
#             "context_used": [],
#             "session_id": session_id
#         }

#     # 🚫 Remove GitHub noise
#     non_repo_chunks = [
#         c for c in retrieved_chunks
#         if "github" not in c.get("source", "").lower()
#     ]

#     if non_repo_chunks:
#         retrieved_chunks = non_repo_chunks

#     # 📊 Rerank
#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]
#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     # DEBUG LOG
#     print("\n===== FINAL CONTEXT =====")
#     for i, t in enumerate(texts):
#         print(f"\nChunk {i+1}:\n{t[:300]}")
#     print("========================\n")

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     answer = generate_answer_from_llm(query, context, history)

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": calculate_confidence(texts),
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Department-filtered pipeline",
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
# # 🔒 Query Intent Detection (NEW - CRITICAL FIX)
# # --------------------------------------------------

# def detect_query_department(query: str):

#     query = query.lower()

#     # HR detection
#     if any(word in query for word in [
#         "leave", "vacation", "employee", "benefits", "hr",
#         "payroll", "hiring", "recruitment", "policy"
#     ]):
#         return "hr"

#     # Finance detection
#     if any(word in query for word in [
#         "expense", "reimbursement", "finance", "budget",
#         "cost", "payment", "invoice", "travel"
#     ]):
#         return "finance"

#     # Engineering detection
#     if any(word in query for word in [
#         "code", "engineering", "api", "system",
#         "architecture", "backend", "frontend", "deployment"
#     ]):
#         return "engineering"

#     return "general"


# # --------------------------------------------------
# # Rerank
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         # Source-based weighting
#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# 1. Answer using ONLY the provided context.
# 2. Extract the exact answer if present.
# 3. Be direct.
# 4. Do NOT hallucinate or infer outside the context.
# """

#     history_text = ""
#     for msg in history:
#         role = msg["role"]
#         content = msg["content"]
#         history_text += f"{role}: {content}\n"

#     user_prompt = f"""
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

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     # ✅ Resolve allowed departments
#     if allowed_departments is None:
#         allowed_departments = resolve_departments(user_group_ids)

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     # 🔒 STEP 35 FIX: Intent-based Access Control
#     detected_department = detect_query_department(query)

#     logger.info(f"DETECTED QUERY DEPARTMENT: {detected_department}")

#     if detected_department not in allowed_departments:
#         logger.warning("ACCESS DENIED: Query intent outside allowed departments")

#         return {
#             "question": query,
#             "answer": "You do not have access to this department. Contact your administrator.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Access denied (intent-based)",
#             "context_used": [],
#             "session_id": session_id
#         }

#     history = memory.get_history(session_id)

#     rewritten_query = rewrite_query(query)

#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # 🔍 Retrieve chunks
#     retrieved_chunks = search_text(
#         rewritten_query,
#         department=allowed_departments,
#         limit=30
#     )

#     # 🔒 Double Safety Filter
#     retrieved_chunks = [
#         c for c in retrieved_chunks
#         if c.get("department") in allowed_departments
#     ]

#     # ⚠️ NO DATA FOUND (NOT ACCESS ISSUE)
#     if not retrieved_chunks:
#         logger.warning("NO DATA FOUND FOR ALLOWED DEPARTMENTS")

#         return {
#             "question": query,
#             "answer": "I could not find information about this in your accessible knowledge base.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "No data found",
#             "context_used": [],
#             "session_id": session_id
#         }

#     # 🚫 Remove GitHub noise
#     non_repo_chunks = [
#         c for c in retrieved_chunks
#         if "github" not in c.get("source", "").lower()
#     ]

#     if non_repo_chunks:
#         retrieved_chunks = non_repo_chunks

#     # 📊 Rerank
#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]
#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     answer = generate_answer_from_llm(query, context, history)

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": calculate_confidence(texts),
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Department-filtered pipeline + intent guard",
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
# # Query Intent Detection (ONLY for logging)
# # --------------------------------------------------

# def detect_query_department(query: str):

#     query = query.lower()

#     if any(word in query for word in [
#         "leave", "vacation", "employee", "benefits", "hr",
#         "payroll", "hiring", "recruitment", "policy"
#     ]):
#         return "hr"

#     if any(word in query for word in [
#         "expense", "reimbursement", "finance", "budget",
#         "cost", "payment", "invoice", "travel"
#     ]):
#         return "finance"

#     if any(word in query for word in [
#         "code", "engineering", "api", "system",
#         "architecture", "backend", "frontend", "deployment"
#     ]):
#         return "engineering"

#     return "general"


# # --------------------------------------------------
# # Rerank
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# 1. Answer using ONLY the provided context.
# 2. Use chat history if needed to understand follow-up questions.
# 3. Be direct.
# 4. Do NOT hallucinate.
# """

#     # ✅ FORMAT HISTORY PROPERLY
#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     # Limit history (avoid token overflow)
#     recent_history = history[-6:]

#     for msg in recent_history:
#         messages.append({
#             "role": msg["role"],
#             "content": msg["content"]
#         })

#     # ✅ ADD CURRENT QUESTION WITH CONTEXT
#     user_prompt = f"""
# Context:
# {context}

# Question:
# {query}
# """

#     messages.append({
#         "role": "user",
#         "content": user_prompt.strip()
#     })

#     response = client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=messages,
#         temperature=0,
#     )

#     return response.choices[0].message.content.strip()




# # --------------------------------------------------
# # RAG Pipeline (FINAL PRODUCTION VERSION)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     # ✅ Resolve allowed departments
#     if allowed_departments is None:
#         allowed_departments = resolve_departments(user_group_ids)

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     # (Only for debug visibility — not used for blocking)
#     detected_department = detect_query_department(query)
#     logger.info(f"DETECTED QUERY DEPARTMENT: {detected_department}")

#     history = memory.get_history(session_id)

#     rewritten_query = rewrite_query(query)
#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # 🔍 Retrieval (THIS is your real access control)
#     retrieved_chunks = search_text(
#         rewritten_query,
#         department=allowed_departments,
#         limit=30
#     )

#     # 🔒 Strict safety filter
#     retrieved_chunks = [
#         c for c in retrieved_chunks
#         if c.get("department") in allowed_departments
#     ]

#     logger.info(f"RETRIEVED CHUNKS COUNT: {len(retrieved_chunks)}")

#     # ⚠️ No data found (NOT access issue)
#     if not retrieved_chunks:
#         logger.warning("NO DATA FOUND FOR ALLOWED DEPARTMENTS")

#         return {
#             "question": query,
#             "answer": "I could not find information about this in your accessible knowledge base.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "No data found",
#             "context_used": [],
#             "session_id": session_id
#         }

#     # 🚫 Remove GitHub noise
#     non_repo_chunks = [
#         c for c in retrieved_chunks
#         if "github" not in c.get("source", "").lower()
#     ]

#     if non_repo_chunks:
#         retrieved_chunks = non_repo_chunks

#     # 📊 Rerank
#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]
#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     answer = generate_answer_from_llm(query, context, history)

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": calculate_confidence(texts),
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Department-filtered pipeline (retrieval-only access control)",
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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # Query Rewriting (ENHANCED WITH HISTORY)
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):
#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the user query for better semantic retrieval.

# IMPORTANT:
# - If this is a follow-up question, use chat history to understand context
# - Keep topic consistent with previous discussion
# - Do NOT change meaning

# Chat History:
# {history_text}

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
# # Query Intent Detection (ONLY for logging)
# # --------------------------------------------------

# def detect_query_department(query: str):

#     query = query.lower()

#     if any(word in query for word in [
#         "leave", "vacation", "employee", "benefits", "hr",
#         "payroll", "hiring", "recruitment", "policy"
#     ]):
#         return "hr"

#     if any(word in query for word in [
#         "expense", "reimbursement", "finance", "budget",
#         "cost", "payment", "invoice", "travel"
#     ]):
#         return "finance"

#     if any(word in query for word in [
#         "code", "engineering", "api", "system",
#         "architecture", "backend", "frontend", "deployment"
#     ]):
#         return "engineering"

#     return "general"


# # --------------------------------------------------
# # Rerank
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

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
# # LLM Answer (STRICT FOLLOW-UP CONTROL)
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind, an enterprise knowledge assistant.

# STRICT RULES:
# 1. Answer ONLY using provided context
# 2. Use chat history to understand follow-up questions
# 3. DO NOT change topic from previous discussion
# 4. If user asks follow-up (e.g., "how long", "how many"), refer to previous topic
# 5. DO NOT introduce unrelated concepts (like FMLA if topic is maternity leave)
# 6. Be precise and grounded
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     recent_history = history[-6:]

#     for msg in recent_history:
#         messages.append({
#             "role": msg["role"],
#             "content": msg["content"]
#         })

#     user_prompt = f"""
# Context:
# {context}

# Question:
# {query}

# IMPORTANT:
# Stay consistent with previous topic.
# """

#     messages.append({
#         "role": "user",
#         "content": user_prompt.strip()
#     })

#     response = client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=messages,
#         temperature=0,
#     )

#     return response.choices[0].message.content.strip()


# # --------------------------------------------------
# # RAG Pipeline (UPDATED)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     if allowed_departments is None:
#         allowed_departments = resolve_departments(user_group_ids)

#     logger.info(f"USER GROUP IDS: {user_group_ids}")
#     logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#     detected_department = detect_query_department(query)
#     logger.info(f"DETECTED QUERY DEPARTMENT: {detected_department}")

#     # ✅ GET HISTORY FIRST
#     history = memory.get_history(session_id)

#     # ✅ ENHANCED QUERY WITH HISTORY
#     rewritten_query = rewrite_query(query, history)
#     logger.info(f"REWRITTEN QUERY: {rewritten_query}")

#     # 🔍 Retrieval
#     retrieved_chunks = search_text(
#         rewritten_query,
#         department=allowed_departments,
#         limit=30
#     )

#     retrieved_chunks = [
#         c for c in retrieved_chunks
#         if c.get("department") in allowed_departments
#     ]

#     logger.info(f"RETRIEVED CHUNKS COUNT: {len(retrieved_chunks)}")

#     if not retrieved_chunks:
#         return {
#             "question": query,
#             "answer": "I could not find information about this in your accessible knowledge base.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "No data found",
#             "context_used": [],
#             "session_id": session_id
#         }

#     # 🚫 Remove GitHub noise
#     non_repo_chunks = [
#         c for c in retrieved_chunks
#         if "github" not in c.get("source", "").lower()
#     ]

#     if non_repo_chunks:
#         retrieved_chunks = non_repo_chunks

#     # 📊 Rerank
#     reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

#     texts = [chunk["text"] for chunk in reranked_chunks]
#     sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

#     context = build_context(texts)

#     if len(context) > MAX_CONTEXT_CHARS:
#         context = context[:MAX_CONTEXT_CHARS]

#     # 🤖 LLM
#     answer = generate_answer_from_llm(query, context, history)

#     return {
#         "question": query,
#         "answer": answer,
#         "confidence": calculate_confidence(texts),
#         "grounded": True,
#         "sources": sources,
#         "evaluation": "Department-filtered pipeline (retrieval-only access control)",
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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM CALL WRAPPER (🔥 FIX)
# # --------------------------------------------------

# def safe_llm_call(messages):

#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )

#         return response.choices[0].message.content.strip()

#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # Query Rewriting
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the user query for better semantic retrieval.

# IMPORTANT:
# - If this is a follow-up question, use chat history
# - Keep topic consistent

# Chat History:
# {history_text}

# User Question:
# {query}

# Improved Query:
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception as e:
#         logger.error(f"Rewrite error: {str(e)}")
#         return query


# # --------------------------------------------------
# # Department Detection
# # --------------------------------------------------

# def detect_query_department(query: str):

#     query = query.lower()

#     if any(word in query for word in ["leave", "policy", "employee", "benefits"]):
#         return "hr"

#     if any(word in query for word in ["expense", "budget", "finance"]):
#         return "finance"

#     if any(word in query for word in ["code", "api", "system"]):
#         return "engineering"

#     return "general"


# # --------------------------------------------------
# # Rerank
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost
#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # Context
# # --------------------------------------------------

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


# # --------------------------------------------------
# # Answer Generation (🔥 FIXED)
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind, an enterprise knowledge assistant.

# STRICT RULES:
# - Answer ONLY from context
# - Use chat history for follow-ups
# - Stay on same topic
# - Do NOT hallucinate
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}
# """
#     })

#     answer = safe_llm_call(messages)

#     return answer if answer else "I could not generate a response."


# # --------------------------------------------------
# # MAIN RAG
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     try:

#         if allowed_departments is None:
#             allowed_departments = resolve_departments(user_group_ids)

#         history = memory.get_history(session_id)

#         rewritten_query = rewrite_query(query, history)

#         retrieved_chunks = search_text(
#             rewritten_query,
#             department=allowed_departments,
#             limit=30
#         )

#         retrieved_chunks = [
#             c for c in retrieved_chunks
#             if c.get("department") in allowed_departments
#         ]

#         if not retrieved_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No data",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(query, retrieved_chunks)

#         texts = [c["text"] for c in reranked]
#         sources = list({c["source"] for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Department-filtered pipeline",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG ERROR: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Something went wrong while processing your request.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }

















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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM CALL
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# # def generate_answer_from_llm(query: str, context: str, history):

# #     system_prompt = """
# # You are AstraMind.

# # STRICT:
# # - Stay on same topic as previous question
# # - Use context only
# # - No hallucination
# # """

# #     messages = [{"role": "system", "content": system_prompt}]

# #     for msg in history[-6:]:
# #         messages.append(msg)

# #     messages.append({
# #         "role": "user",
# #         "content": f"Context:\n{context}\n\nQuestion:\n{query}"
# #     })

# #     return safe_llm_call(messages) or "I could not generate a response."



# def generate_answer_from_llm(query: str, context: str, history):

#     # 🔥 Get primary topic again (important!)
#     primary_topic = ""
#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             primary_topic = msg["content"]
#             break

#     system_prompt = f"""
# You are AstraMind.

# STRICT RULES:
# - User is asking a FOLLOW-UP question
# - The topic is: "{primary_topic}"

# YOU MUST:
# - Answer ONLY about this topic
# - Ignore other policies in context
# - Do NOT summarize multiple leave types
# - Give a DIRECT answer

# Example:
# Q: What is maternity leave?
# Q: How long is it?
# A: 16 weeks

# NOT:
# ❌ listing multiple leave policies
# ❌ general summaries
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}

# Answer ONLY for: {primary_topic}
# """
#     })

#     answer = safe_llm_call(messages)

#     return answer if answer else "I could not generate a response."


# # --------------------------------------------------
# # MAIN RAG
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

#     try:

#         if allowed_departments is None:
#             allowed_departments = resolve_departments(user_group_ids)

#         history = memory.get_history(session_id)

#         rewritten_query = rewrite_query(query, history)

#         # 🔥 FIX: GET PRIMARY TOPIC
#         primary_topic = get_primary_topic(history)

#         # 🔥 FIX: COMBINE QUERY
#         combined_query = f"{primary_topic} {query}"

#         logger.info(f"COMBINED QUERY: {combined_query}")

#         # 🔥🔥🔥 CRITICAL FIX HERE
#         retrieved_chunks = search_text(
#             combined_query,   # ✅ FIXED
#             department=allowed_departments,
#             limit=30
#         )

#         retrieved_chunks = [
#             c for c in retrieved_chunks
#             if c.get("department") in allowed_departments
#         ]

#         if not retrieved_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No data",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(combined_query, retrieved_chunks)

#         texts = [c["text"] for c in reranked]
#         sources = list({c["source"] for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Department-filtered pipeline",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG ERROR: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Something went wrong while processing your request.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }























# import time
# from typing import List

# from openai import OpenAI

# from app.core.vector_store import search_text
# from app.core.logger import logger
# from app.services.memory_service import memory

# # ⭐ STEP 39
# from app.auth.permissions import resolve_departments

# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     primary_topic = get_primary_topic(history)

#     system_prompt = f"""
# You are AstraMind.

# STRICT:
# - Follow-up question
# - Topic: {primary_topic}
# - Answer ONLY about this
# - No unrelated policies
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"Context:\n{context}\n\nQuestion:\n{query}"
#     })

#     return safe_llm_call(messages) or "I could not generate a response."


# # --------------------------------------------------
# # MAIN RAG (STEP 39 FINAL)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user: dict):

#     try:

#         # ⭐ STEP 39 — ROLE BASED ACCESS
#         allowed_departments = resolve_departments(user)

#         logger.info(f"ROLE: {user.get('role')}")
#         logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#         history = memory.get_history(session_id)

#         rewritten_query = rewrite_query(query, history)

#         primary_topic = get_primary_topic(history)

#         combined_query = f"{primary_topic} {query}"

#         # 🔍 FILTERED SEARCH
#         retrieved_chunks = search_text(
#             combined_query,
#             department=allowed_departments,
#             limit=30
#         )

#         retrieved_chunks = [
#             c for c in retrieved_chunks
#             if c.get("department") in allowed_departments
#         ]

#         if not retrieved_chunks:
#             return {
#                 "question": query,
#                 "answer": "No accessible information found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "Access filtered",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(combined_query, retrieved_chunks)

#         texts = [c["text"] for c in reranked]
#         sources = list({c["source"] for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Role-based access enforced",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG ERROR: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Something went wrong while processing your request.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }























# import time
# from typing import List

# from openai import OpenAI

# from app.core.vector_store import search_text
# from app.core.logger import logger
# from app.services.memory_service import memory

# # ⭐ STEP 39
# from app.auth.permissions import resolve_departments

# from app.config import (
#     OPENAI_API_KEY,
#     LLM_MODEL,
#     MAX_CONTEXT_CHARS,
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk["text"].lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     primary_topic = get_primary_topic(history)

#     system_prompt = f"""
# You are AstraMind.

# STRICT:
# - Follow-up question
# - Topic: {primary_topic}
# - Answer ONLY about this
# - No unrelated policies
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"Context:\n{context}\n\nQuestion:\n{query}"
#     })

#     return safe_llm_call(messages) or "I could not generate a response."


# # --------------------------------------------------
# # MAIN RAG (STEP 39 FINAL FIXED)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user: dict):

#     try:

#         # ✅ FIX — Extract group_ids properly
#         group_ids = user.get("group_ids", [])

#         # ✅ FIX — Correct input to permissions
#         allowed_departments = resolve_departments(group_ids)

#         logger.info(f"ROLE: {user.get('role')}")
#         logger.info(f"GROUP IDS: {group_ids}")
#         logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

#         history = memory.get_history(session_id)

#         rewritten_query = rewrite_query(query, history)

#         primary_topic = get_primary_topic(history)

#         combined_query = f"{primary_topic} {query}"

#         # 🔍 FILTERED SEARCH
#         retrieved_chunks = search_text(
#             combined_query,
#             department=allowed_departments,
#             limit=30
#         )

#         retrieved_chunks = [
#             c for c in retrieved_chunks
#             if c.get("department") in allowed_departments
#         ]

#         if not retrieved_chunks:
#             return {
#                 "question": query,
#                 "answer": "No accessible information found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "Access filtered",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(combined_query, retrieved_chunks)

#         texts = [c["text"] for c in reranked]
#         sources = list({c["source"] for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Role-based access enforced",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG ERROR: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Something went wrong while processing your request.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }






















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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # 🔥 CRITICAL FIX: CLEAN CHUNKS
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     for c in raw_chunks:

#         # Case 1: already dict
#         if isinstance(c, dict):
#             cleaned.append(c)
#             continue

#         # Case 2: list → flatten
#         if isinstance(c, list):
#             for item in c:
#                 if isinstance(item, dict):
#                     cleaned.append(item)
#             continue

#         # Case 3: ignore garbage
#         continue

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     primary_topic = get_primary_topic(history)

#     system_prompt = f"""
# You are AstraMind.

# STRICT:
# - Topic: "{primary_topic}"
# - Answer ONLY about this
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}
# """
#     })

#     return safe_llm_call(messages) or "I could not generate a response."


# # --------------------------------------------------
# # ✅ FINAL MAIN RAG (FIXED)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user):

#     try:

#         group_ids = user.get("group_ids", [])

#         allowed_departments = resolve_departments(group_ids)

#         history = memory.get_history(session_id)

#         primary_topic = get_primary_topic(history)
#         combined_query = f"{primary_topic} {query}"

#         raw_chunks = search_text(
#             combined_query,
#             department=allowed_departments,
#             limit=30
#         )

#         # 🔥 FIX APPLIED HERE
#         cleaned_chunks = clean_chunks(raw_chunks)

#         filtered_chunks = [
#             c for c in cleaned_chunks
#             if c.get("department") in allowed_departments
#         ]

#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No data",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(combined_query, filtered_chunks)

#         texts = [c.get("text", "") for c in reranked]
#         sources = list({c.get("source", "unknown") for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Department-filtered pipeline",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }















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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # 🔥 HELPER: NORMALIZE USER
# # --------------------------------------------------

# def normalize_user(user):
#     if isinstance(user, list):
#         if len(user) > 0 and isinstance(user[0], dict):
#             return user[0]
#         return {}

#     if isinstance(user, dict):
#         return user

#     return {}


# # --------------------------------------------------
# # 🔥 HELPER: FLATTEN LIST
# # --------------------------------------------------

# def flatten_list(data):
#     flat = []
#     for item in data:
#         if isinstance(item, list):
#             flat.extend(item)
#         else:
#             flat.append(item)
#     return flat


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # 🔥 CLEAN CHUNKS (FIXED PROPERLY)
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     def extract(item):
#         if isinstance(item, dict):
#             cleaned.append(item)

#         elif isinstance(item, list):
#             for sub in item:
#                 extract(sub)  # 🔥 RECURSIVE FIX

#         elif isinstance(item, tuple):
#             cleaned.append({
#                 "text": str(item[0]),
#                 "metadata": item[1] if len(item) > 1 and isinstance(item[1], dict) else {},
#                 "score": item[2] if len(item) > 2 else 0
#             })

#         else:
#             cleaned.append({
#                 "text": str(item),
#                 "metadata": {},
#                 "score": 0
#             })

#     for c in raw_chunks:
#         extract(c)

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         if not isinstance(chunk, dict):
#             continue

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     primary_topic = get_primary_topic(history)

#     system_prompt = f"""
# You are AstraMind.

# STRICT:
# - Topic: "{primary_topic}"
# - Answer ONLY about this
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}
# """
#     })

#     return safe_llm_call(messages) or "I could not generate a response."


# # --------------------------------------------------
# # ✅ FINAL MAIN RAG (FULLY FIXED)
# # --------------------------------------------------

# def generate_rag_answer(
#     query: str,
#     session_id: str,
#     user,
#     allowed_departments=None
# ):

#     try:

#         # 🔥 FIX 1: USER
#         user = normalize_user(user)
#         group_ids = user.get("group_ids", [])

#         # 🔥 FIX 2: DEPARTMENTS
#         if allowed_departments is None:
#             allowed_departments = resolve_departments(group_ids)

#         if isinstance(allowed_departments, list):
#             allowed_departments = flatten_list(allowed_departments)

#         # 🔥 MEMORY
#         history = memory.get_history(session_id)

#         # 🔥 SEARCH
#         raw_chunks = search_text(
#             query,
#             department=allowed_departments,
#             limit=30
#         )

#         # 🔥 DEBUG: log raw structure to identify nesting issues
#         logger.debug(f"RAW CHUNKS TYPE: {type(raw_chunks)}, SAMPLE: {str(raw_chunks[:2]) if raw_chunks else '[]'}")

#         # 🔥 CLEAN — double pass to handle deeply nested lists
#         cleaned_chunks = clean_chunks(raw_chunks)
#         cleaned_chunks = clean_chunks(cleaned_chunks)  # 🔥 FIX: second pass eliminates any remaining nested lists

#         # 🔥 FILTER (SAFE)
#         filtered_chunks = []

#         for c in cleaned_chunks:

#             if not isinstance(c, dict):
#                 continue

#             metadata = c.get("metadata", {})
#             dept = metadata.get("department") or c.get("department")

#             if not allowed_departments or dept in allowed_departments:
#                 filtered_chunks.append(c)

#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No data",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         # 🔥 RERANK
#         reranked = rerank_chunks(query, filtered_chunks)

#         texts = [c.get("text", "") for c in reranked]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         # 🔥 LLM
#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": [],
#             "evaluation": "Department-filtered pipeline",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }



























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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # HELPER: NORMALIZE USER
# # --------------------------------------------------

# def normalize_user(user):
#     if isinstance(user, list):
#         if len(user) > 0 and isinstance(user[0], dict):
#             return user[0]
#         return {}
#     if isinstance(user, dict):
#         return user
#     return {}


# # --------------------------------------------------
# # HELPER: FLATTEN LIST
# # --------------------------------------------------

# def flatten_list(data):
#     flat = []
#     for item in data:
#         if isinstance(item, list):
#             flat.extend(item)
#         else:
#             flat.append(item)
#     return flat


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue
#         content = msg["content"].lower()
#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []
#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )
#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """
#         rewritten = safe_llm_call([{"role": "user", "content": prompt}])
#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # CLEAN CHUNKS
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     def extract(item):
#         if isinstance(item, dict):
#             cleaned.append(item)
#         elif isinstance(item, list):
#             for sub in item:
#                 extract(sub)
#         elif isinstance(item, tuple):
#             cleaned.append({
#                 "text": str(item[0]),
#                 "metadata": item[1] if len(item) > 1 and isinstance(item[1], dict) else {},
#                 "score": item[2] if len(item) > 2 else 0
#             })
#         else:
#             cleaned.append({
#                 "text": str(item),
#                 "metadata": {},
#                 "score": 0
#             })

#     for c in raw_chunks:
#         extract(c)

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         if not isinstance(chunk, dict):
#             continue

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)
#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost
#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)
#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     primary_topic = get_primary_topic(history)

#     system_prompt = f"""
# You are AstraMind.

# STRICT:
# - Topic: "{primary_topic}"
# - Answer ONLY about this
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}
# """
#     })

#     return safe_llm_call(messages) or "I could not generate a response."


# # --------------------------------------------------
# # MAIN RAG
# # --------------------------------------------------

# def generate_rag_answer(
#     query: str,
#     session_id: str,
#     user,
#     allowed_departments=None
# ):

#     try:

#         # normalize user
#         user = normalize_user(user)

#         # 🔥 FIX: pass full user dict to resolve_departments (not just group_ids)
#         if allowed_departments is None:
#             allowed_departments = resolve_departments(user)

#         if isinstance(allowed_departments, list):
#             allowed_departments = flatten_list(allowed_departments)

#         # MEMORY
#         history = memory.get_history(session_id)

#         # SEARCH
#         raw_chunks = search_text(
#             query,
#             department=allowed_departments,
#             limit=30
#         )

#         logger.debug(f"RAW CHUNKS SAMPLE: {str(raw_chunks[:2]) if raw_chunks else '[]'}")

#         # CLEAN — double pass to handle any deep nesting
#         cleaned_chunks = clean_chunks(raw_chunks)
#         cleaned_chunks = clean_chunks(cleaned_chunks)

#         # FILTER
#         filtered_chunks = []

#         for c in cleaned_chunks:

#             if not isinstance(c, dict):
#                 continue

#             metadata = c.get("metadata", {})
#             dept = metadata.get("department") or c.get("department")

#             if not allowed_departments or dept in allowed_departments:
#                 filtered_chunks.append(c)

#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No data",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         # RERANK
#         reranked = rerank_chunks(query, filtered_chunks)
#         texts = [c.get("text", "") for c in reranked]
#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         # LLM
#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": [],
#             "evaluation": "Department-filtered pipeline",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }




















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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # HELPER: NORMALIZE USER
# # --------------------------------------------------

# def normalize_user(user):
#     if isinstance(user, list):
#         if len(user) > 0 and isinstance(user[0], dict):
#             return user[0]
#         return {}
#     if isinstance(user, dict):
#         return user
#     return {}


# # --------------------------------------------------
# # HELPER: FLATTEN LIST
# # --------------------------------------------------

# def flatten_list(data):
#     flat = []
#     for item in data:
#         if isinstance(item, list):
#             flat.extend(item)
#         else:
#             flat.append(item)
#     return flat


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue
#         content = msg["content"].lower()
#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []
#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )
#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """
#         rewritten = safe_llm_call([{"role": "user", "content": prompt}])
#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # CLEAN CHUNKS
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     def extract(item):
#         if isinstance(item, dict):
#             cleaned.append(item)
#         elif isinstance(item, list):
#             for sub in item:
#                 extract(sub)
#         elif isinstance(item, tuple):
#             cleaned.append({
#                 "text": str(item[0]),
#                 "metadata": item[1] if len(item) > 1 and isinstance(item[1], dict) else {},
#                 "score": item[2] if len(item) > 2 else 0
#             })
#         else:
#             cleaned.append({
#                 "text": str(item),
#                 "metadata": {},
#                 "score": 0
#             })

#     for c in raw_chunks:
#         extract(c)

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         if not isinstance(chunk, dict):
#             continue

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)
#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost
#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)
#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     primary_topic = get_primary_topic(history)

#     system_prompt = f"""
# You are AstraMind.

# STRICT:
# - Topic: "{primary_topic}"
# - Answer ONLY about this
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}
# """
#     })

#     return safe_llm_call(messages) or "I could not generate a response."


# # --------------------------------------------------
# # MAIN RAG
# # --------------------------------------------------

# def generate_rag_answer(
#     query: str,
#     session_id: str,
#     user,
#     allowed_departments=None
# ):

#     try:

#         # normalize user
#         user = normalize_user(user)

#         # 🔥 FIX: pass full user dict to resolve_departments (not just group_ids)
#         if allowed_departments is None:
#             allowed_departments = resolve_departments(user)

#         if isinstance(allowed_departments, list):
#             allowed_departments = flatten_list(allowed_departments)

#         # MEMORY
#         history = memory.get_history(session_id)

#         # SEARCH
#         raw_chunks = search_text(
#             query,
#             department=allowed_departments,
#             limit=30
#         )

#         # CLEAN — double pass to handle any deep nesting
#         cleaned_chunks = clean_chunks(raw_chunks)
#         cleaned_chunks = clean_chunks(cleaned_chunks)

#         # FILTER
#         filtered_chunks = []

#         for c in cleaned_chunks:

#             if not isinstance(c, dict):
#                 continue

#             metadata = c.get("metadata", {})
#             dept = metadata.get("department") or c.get("department")

#             if not allowed_departments or dept in allowed_departments:
#                 filtered_chunks.append(c)

#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No data",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         # RERANK
#         reranked = rerank_chunks(query, filtered_chunks)
#         texts = [c.get("text", "") for c in reranked]
#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         # LLM
#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": [],
#             "evaluation": "Department-filtered pipeline",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }
























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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # CLEAN CHUNKS (CRITICAL FIX)
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     if not raw_chunks:
#         return cleaned

#     # CASE 1 → list of dicts
#     if isinstance(raw_chunks, list):
#         for item in raw_chunks:
#             if isinstance(item, dict):
#                 cleaned.append(item)

#             # CASE 2 → list inside list
#             elif isinstance(item, list):
#                 for sub in item:
#                     if isinstance(sub, dict):
#                         cleaned.append(sub)

#     # CASE 3 → single dict
#     elif isinstance(raw_chunks, dict):
#         cleaned.append(raw_chunks)

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind.

# STRICT RULES:
# - ONLY answer from provided context
# - If context is irrelevant → say "No relevant data found"
# - DO NOT guess
# - DO NOT use outside knowledge
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}
# """
#     })

#     return safe_llm_call(messages) or "No relevant data found."


# # --------------------------------------------------
# # MAIN RAG (FULL FIXED)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user):

#     try:

#         # ✅ ALWAYS PASS FULL USER (STEP 39 FIX)
#         allowed_departments = resolve_departments(user)

#         history = memory.get_history(session_id)

#         primary_topic = get_primary_topic(history)
#         combined_query = f"{primary_topic} {query}".strip()

#         raw_chunks = search_text(
#             combined_query,
#             department=allowed_departments,
#             limit=30
#         )

#         cleaned_chunks = clean_chunks(raw_chunks)

#         # 🔴 HARD FILTER (SECURITY FIX)
#         filtered_chunks = [
#             c for c in cleaned_chunks
#             if isinstance(c, dict)
#             and c.get("department") is not None
#             and c.get("department") in allowed_departments
#         ]

#         # ❌ NO DATA
#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No department match",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(combined_query, filtered_chunks)

#         texts = [c.get("text", "") for c in reranked if c.get("text")]
#         sources = list({c.get("source", "unknown") for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Department-secure RAG",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }





















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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # CLEAN CHUNKS (CRITICAL FIX)
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     if not raw_chunks:
#         return cleaned

#     # CASE 1 → list of dicts
#     if isinstance(raw_chunks, list):
#         for item in raw_chunks:
#             if isinstance(item, dict):
#                 cleaned.append(item)

#             # CASE 2 → list inside list
#             elif isinstance(item, list):
#                 for sub in item:
#                     if isinstance(sub, dict):
#                         cleaned.append(sub)

#     # CASE 3 → single dict
#     elif isinstance(raw_chunks, dict):
#         cleaned.append(raw_chunks)

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind.

# STRICT RULES:
# - ONLY answer from provided context
# - If context is irrelevant → say "No relevant data found"
# - DO NOT guess
# - DO NOT use outside knowledge
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}
# """
#     })

#     return safe_llm_call(messages) or "No relevant data found."


# # --------------------------------------------------
# # MAIN RAG (FULL FIXED)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user, allowed_departments=None):

#     try:

#         # 🔥 FIX: use passed allowed_departments if provided, else resolve from user
#         if allowed_departments is None:
#             allowed_departments = resolve_departments(user)

#         history = memory.get_history(session_id)

#         # primary_topic = get_primary_topic(history)
#         # combined_query = f"{primary_topic} {query}".strip()



#         # Step 39 FIX — intelligent rewrite
#         rewritten_query = rewrite_query(query, history)
#         combined_query = rewritten_query

#         raw_chunks = search_text(
#             combined_query,
#             department=allowed_departments,
#             limit=30
#         )

#         cleaned_chunks = clean_chunks(raw_chunks)

#         # 🔴 HARD FILTER (SECURITY FIX)
#         filtered_chunks = [
#             c for c in cleaned_chunks
#             if isinstance(c, dict)
#             and c.get("department") is not None
#             and c.get("department") in allowed_departments
#         ]

#         # ❌ NO DATA
#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No department match",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(combined_query, filtered_chunks)

#         texts = [c.get("text", "") for c in reranked if c.get("text")]
#         sources = list({c.get("source", "unknown") for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": calculate_confidence(texts),
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Department-secure RAG",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }


















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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE (STEP 39 FIX)
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.
# Make it standalone and clear.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # CLEAN CHUNKS (CRITICAL FIX)
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     if not raw_chunks:
#         return cleaned

#     if isinstance(raw_chunks, list):
#         for item in raw_chunks:
#             if isinstance(item, dict):
#                 cleaned.append(item)
#             elif isinstance(item, list):
#                 for sub in item:
#                     if isinstance(sub, dict):
#                         cleaned.append(sub)

#     elif isinstance(raw_chunks, dict):
#         cleaned.append(raw_chunks)

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     system_prompt = """
# You are AstraMind.

# STRICT RULES:
# - ONLY answer from provided context
# - If context is irrelevant → say "No relevant data found"
# - DO NOT guess
# - DO NOT use outside knowledge
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}
# """
#     })

#     return safe_llm_call(messages) or "No relevant data found."


# # --------------------------------------------------
# # MAIN RAG (FINAL FIXED)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user, allowed_departments=None):

#     try:

#         if allowed_departments is None:
#             allowed_departments = resolve_departments(user)

#         history = memory.get_history(session_id)

#         # 🔥 STEP 39 FIX — FOLLOW-UP HANDLING
#         rewritten_query = rewrite_query(query, history)
#         combined_query = rewritten_query.strip()

#         raw_chunks = search_text(
#             combined_query,
#             department=allowed_departments,
#             limit=30
#         )

#         cleaned_chunks = clean_chunks(raw_chunks)

#         # 🔴 HARD FILTER (SECURITY)
#         filtered_chunks = [
#             c for c in cleaned_chunks
#             if isinstance(c, dict)
#             and c.get("department") is not None
#             and c.get("department") in allowed_departments
#         ]

#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No department match",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(combined_query, filtered_chunks)

#         texts = [c.get("text", "") for c in reranked if c.get("text")]
#         sources = list({c.get("source", "unknown") for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         # 🔥 confidence fix
#         confidence = calculate_confidence(texts) if answer != "No relevant data found." else 0.0

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": confidence,
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Department-secure RAG",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }





















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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE (STEP 39 FIX)
# # --------------------------------------------------

# def rewrite_query(query: str, history: list):

#     try:
#         recent_history = history[-3:] if history else []

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in recent_history]
#         )

#         prompt = f"""
# Rewrite the query for better retrieval.
# Make it standalone and clear.

# Chat:
# {history_text}

# Query:
# {query}
# """

#         rewritten = safe_llm_call([
#             {"role": "user", "content": prompt}
#         ])

#         return rewritten if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # CLEAN CHUNKS (CRITICAL FIX)
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     if not raw_chunks:
#         return cleaned

#     if isinstance(raw_chunks, list):
#         for item in raw_chunks:
#             if isinstance(item, dict):
#                 cleaned.append(item)
#             elif isinstance(item, list):
#                 for sub in item:
#                     if isinstance(sub, dict):
#                         cleaned.append(sub)

#     elif isinstance(raw_chunks, dict):
#         cleaned.append(raw_chunks)

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost

#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER — FIXED: inject primary topic into prompt
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     primary_topic = get_primary_topic(history)

#     system_prompt = f"""
# You are AstraMind.

# STRICT RULES:
# - ONLY answer from provided context
# - If context is irrelevant → say "No relevant data found"
# - DO NOT guess
# - DO NOT use outside knowledge

# FOLLOW-UP HANDLING:
# - Primary topic: "{primary_topic}"
# - If the question is vague (e.g., "how many days", "how long")
#   → interpret it using the primary topic
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""
# Context:
# {context}

# Question:
# {query}

# If needed, interpret the question using:
# Primary topic: {primary_topic}
# """
#     })

#     return safe_llm_call(messages) or "No relevant data found."


# # --------------------------------------------------
# # MAIN RAG (FINAL FIXED)
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user, allowed_departments=None):

#     try:

#         if allowed_departments is None:
#             allowed_departments = resolve_departments(user)

#         history = memory.get_history(session_id)

#         # 🔥 STEP 39 FIX — FOLLOW-UP HANDLING
#         rewritten_query = rewrite_query(query, history)
#         combined_query = rewritten_query.strip()

#         raw_chunks = search_text(
#             combined_query,
#             department=allowed_departments,
#             limit=30
#         )

#         cleaned_chunks = clean_chunks(raw_chunks)

#         # 🔴 HARD FILTER (SECURITY)
#         filtered_chunks = [
#             c for c in cleaned_chunks
#             if isinstance(c, dict)
#             and c.get("department") is not None
#             and c.get("department") in allowed_departments
#         ]

#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No department match",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(combined_query, filtered_chunks)

#         texts = [c.get("text", "") for c in reranked if c.get("text")]
#         sources = list({c.get("source", "unknown") for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         # 🔥 confidence fix
#         confidence = calculate_confidence(texts) if answer != "No relevant data found." else 0.0

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": confidence,
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Department-secure RAG",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }






















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
# )

# client = OpenAI(api_key=OPENAI_API_KEY)


# # --------------------------------------------------
# # SAFE LLM
# # --------------------------------------------------

# def safe_llm_call(messages):
#     try:
#         response = client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=messages,
#             temperature=0,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logger.error(f"LLM ERROR: {str(e)}")
#         return None


# # --------------------------------------------------
# # PRIMARY TOPIC
# # --------------------------------------------------

# def get_primary_topic(history):

#     follow_up_words = ["how long", "how many", "what about", "and", "then"]

#     for msg in reversed(history):
#         if msg["role"] != "user":
#             continue

#         content = msg["content"].lower()

#         if not any(f in content for f in follow_up_words):
#             return msg["content"]

#     return ""


# # --------------------------------------------------
# # QUERY REWRITE — FIXED: uses full history to resolve follow-ups
# # --------------------------------------------------

# def rewrite_query(query: str, history: list) -> str:

#     if not history:
#         return query

#     try:
#         # Build a readable conversation so the LLM has full context
#         history_text = "\n".join(
#             f"{msg['role'].upper()}: {msg['content']}"
#             for msg in history[-6:]
#         )

#         prompt = f"""You are helping rewrite a follow-up question into a fully self-contained search query.

# Conversation so far:
# {history_text}

# Latest question: "{query}"

# Rules:
# - If the question is a follow-up (e.g. "how many days?", "what about paternity?", "and sick leave?"), rewrite it to include the topic from the conversation.
# - If the question is already clear and standalone, return it unchanged.
# - Return ONLY the rewritten question. No explanation. No quotes.

# Rewritten question:"""

#         rewritten = safe_llm_call([{"role": "user", "content": prompt}])
#         return rewritten.strip() if rewritten else query

#     except Exception:
#         return query


# # --------------------------------------------------
# # CLEAN CHUNKS
# # --------------------------------------------------

# def clean_chunks(raw_chunks):

#     cleaned = []

#     if not raw_chunks:
#         return cleaned

#     if isinstance(raw_chunks, list):
#         for item in raw_chunks:
#             if isinstance(item, dict):
#                 cleaned.append(item)
#             elif isinstance(item, list):
#                 for sub in item:
#                     if isinstance(sub, dict):
#                         cleaned.append(sub)

#     elif isinstance(raw_chunks, dict):
#         cleaned.append(raw_chunks)

#     return cleaned


# # --------------------------------------------------
# # RERANK
# # --------------------------------------------------

# def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

#     query_words = set(query.lower().split())
#     scored = []

#     for chunk in chunks:

#         text = chunk.get("text", "").lower()
#         keyword_score = sum(1 for w in query_words if w in text)
#         semantic_score = chunk.get("score", 0)

#         source = chunk.get("source", "")

#         if ".pdf" in source.lower():
#             boost = 0.6
#         elif "http" in source.lower() and "github" not in source.lower():
#             boost = 0.4
#         elif "github" in source.lower():
#             boost = -0.3
#         else:
#             boost = 0

#         final_score = semantic_score + (keyword_score * 0.05) + boost
#         scored.append((final_score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)
#     return [c[1] for c in scored[:top_k]]


# # --------------------------------------------------
# # CONTEXT
# # --------------------------------------------------

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


# # --------------------------------------------------
# # LLM ANSWER — injects primary topic for follow-up awareness
# # --------------------------------------------------

# def generate_answer_from_llm(query: str, context: str, history):

#     primary_topic = get_primary_topic(history)

#     system_prompt = f"""You are AstraMind, an enterprise HR assistant.

# STRICT RULES:
# - ONLY answer from the provided context
# - If context is irrelevant → say "No relevant data found"
# - DO NOT guess or use outside knowledge

# FOLLOW-UP HANDLING:
# - The user's primary topic in this conversation is: "{primary_topic}"
# - If the question is vague (e.g. "how many days?", "how long?"), interpret it in the context of: "{primary_topic}"
# - Give a direct, specific answer — do not list all leave types unless explicitly asked
# """

#     messages = [{"role": "system", "content": system_prompt.strip()}]

#     for msg in history[-6:]:
#         messages.append(msg)

#     messages.append({
#         "role": "user",
#         "content": f"""Context:
# {context}

# Question: {query}

# Remember: interpret this question in the context of "{primary_topic}" if it is vague."""
#     })

#     return safe_llm_call(messages) or "No relevant data found."


# # --------------------------------------------------
# # MAIN RAG
# # --------------------------------------------------

# def generate_rag_answer(query: str, session_id: str, user, allowed_departments=None):

#     try:

#         if allowed_departments is None:
#             allowed_departments = resolve_departments(user)

#         history = memory.get_history(session_id)

#         # 🔥 Rewrite vague follow-up into standalone query using full history
#         rewritten_query = rewrite_query(query, history)
#         logger.info(f"Original: '{query}' → Rewritten: '{rewritten_query}'")

#         raw_chunks = search_text(
#             rewritten_query,
#             department=allowed_departments,
#             limit=30
#         )

#         cleaned_chunks = clean_chunks(raw_chunks)

#         # Hard department filter
#         filtered_chunks = [
#             c for c in cleaned_chunks
#             if isinstance(c, dict)
#             and c.get("department") is not None
#             and c.get("department") in allowed_departments
#         ]

#         if not filtered_chunks:
#             return {
#                 "question": query,
#                 "answer": "No relevant data found.",
#                 "confidence": 0.0,
#                 "grounded": False,
#                 "sources": [],
#                 "evaluation": "No department match",
#                 "context_used": [],
#                 "session_id": session_id
#             }

#         reranked = rerank_chunks(rewritten_query, filtered_chunks)

#         texts = [c.get("text", "") for c in reranked if c.get("text")]
#         sources = list({c.get("source", "unknown") for c in reranked})[:3]

#         context = build_context(texts)

#         if len(context) > MAX_CONTEXT_CHARS:
#             context = context[:MAX_CONTEXT_CHARS]

#         answer = generate_answer_from_llm(query, context, history)

#         confidence = calculate_confidence(texts) if answer != "No relevant data found." else 0.0

#         return {
#             "question": query,
#             "answer": answer,
#             "confidence": confidence,
#             "grounded": True,
#             "sources": sources,
#             "evaluation": "Department-secure RAG",
#             "context_used": texts,
#             "session_id": session_id
#         }

#     except Exception as e:
#         logger.error(f"RAG failed: {str(e)}")

#         return {
#             "question": query,
#             "answer": "Internal error occurred.",
#             "confidence": 0.0,
#             "grounded": False,
#             "sources": [],
#             "evaluation": "Error",
#             "context_used": [],
#             "session_id": session_id
#         }



















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
)

client = OpenAI(api_key=OPENAI_API_KEY)


# --------------------------------------------------
# SAFE LLM CALL
# --------------------------------------------------

def safe_llm_call(messages):
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"LLM ERROR: {str(e)}")
        return None


# --------------------------------------------------
# PRIMARY TOPIC
# --------------------------------------------------

def get_primary_topic(history):

    follow_up_words = ["how long", "how many", "what about", "and", "then"]

    for msg in reversed(history):
        if msg["role"] != "user":
            continue

        content = msg["content"].lower()

        if not any(f in content for f in follow_up_words):
            return msg["content"]

    return ""


# --------------------------------------------------
# CLEAN CHUNKS (CRITICAL FIX)
# --------------------------------------------------

def clean_chunks(raw_chunks):

    cleaned = []

    if not raw_chunks:
        return cleaned

    if isinstance(raw_chunks, list):
        for item in raw_chunks:
            if isinstance(item, dict):
                cleaned.append(item)
            elif isinstance(item, list):
                for sub in item:
                    if isinstance(sub, dict):
                        cleaned.append(sub)

    elif isinstance(raw_chunks, dict):
        cleaned.append(raw_chunks)

    return cleaned


# --------------------------------------------------
# RERANK
# --------------------------------------------------

def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

    query_words = set(query.lower().split())
    scored = []

    for chunk in chunks:

        text = chunk.get("text", "").lower()
        keyword_score = sum(1 for w in query_words if w in text)
        semantic_score = chunk.get("score", 0)

        source = chunk.get("source", "")

        if ".pdf" in source.lower():
            boost = 0.6
        elif "http" in source.lower() and "github" not in source.lower():
            boost = 0.4
        elif "github" in source.lower():
            boost = -0.3
        else:
            boost = 0

        final_score = semantic_score + (keyword_score * 0.05) + boost

        scored.append((final_score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [c[1] for c in scored[:top_k]]


# --------------------------------------------------
# CONTEXT
# --------------------------------------------------

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


# --------------------------------------------------
# LLM ANSWER (STRICT FOLLOW-UP CONTROL)
# --------------------------------------------------

def generate_answer_from_llm(query: str, context: str, history):

    primary_topic = get_primary_topic(history)

    system_prompt = f"""
You are AstraMind.

STRICT RULES:
- The topic is: "{primary_topic}"
- Answer ONLY about this topic
- Use ONLY the provided context
- DO NOT bring unrelated policies
- DO NOT say "No relevant data found" if answer exists in context

FOLLOW-UP RULE:
If question is vague (e.g., "how many days", "how long"),
interpret it using the topic.
"""

    messages = [{"role": "system", "content": system_prompt.strip()}]

    for msg in history[-6:]:
        messages.append(msg)

    messages.append({
        "role": "user",
        "content": f"""
Context:
{context}

Question:
{query}

Answer specifically for: {primary_topic}
"""
    })

    answer = safe_llm_call(messages)

    return answer if answer else "No relevant data found."


# --------------------------------------------------
# MAIN RAG (FINAL)
# --------------------------------------------------

def generate_rag_answer(query: str, session_id: str, user, allowed_departments=None):

    try:

        # ✅ STEP 39: ROLE-BASED ACCESS
        if allowed_departments is None:
            allowed_departments = resolve_departments(user)

        history = memory.get_history(session_id)

        # 🔥 CRITICAL FIX (DO NOT CHANGE THIS)
        primary_topic = get_primary_topic(history)
        combined_query = f"{primary_topic} {query}".strip()

        logger.info(f"COMBINED QUERY: {combined_query}")

        raw_chunks = search_text(
            combined_query,
            department=allowed_departments,
            limit=30
        )

        # ✅ FIX CRASH
        cleaned_chunks = clean_chunks(raw_chunks)

        # 🔒 STRICT SECURITY FILTER
        filtered_chunks = [
            c for c in cleaned_chunks
            if isinstance(c, dict)
            and c.get("department") in allowed_departments
        ]

        if not filtered_chunks:
            return {
                "question": query,
                "answer": "No relevant data found.",
                "confidence": 0.0,
                "grounded": False,
                "sources": [],
                "evaluation": "No department match",
                "context_used": [],
                "session_id": session_id
            }

        reranked = rerank_chunks(combined_query, filtered_chunks)

        texts = [c.get("text", "") for c in reranked]
        sources = list({c.get("source", "unknown") for c in reranked})[:3]

        context = build_context(texts)

        if len(context) > MAX_CONTEXT_CHARS:
            context = context[:MAX_CONTEXT_CHARS]

        answer = generate_answer_from_llm(query, context, history)

        confidence = calculate_confidence(texts)

        return {
            "question": query,
            "answer": answer,
            "confidence": confidence,
            "grounded": True,
            "sources": sources,
            "evaluation": "Department-secure RAG",
            "context_used": texts,
            "session_id": session_id
        }

    except Exception as e:
        logger.error(f"RAG failed: {str(e)}")

        return {
            "question": query,
            "answer": "Internal error occurred.",
            "confidence": 0.0,
            "grounded": False,
            "sources": [],
            "evaluation": "Error",
            "context_used": [],
            "session_id": session_id
        }