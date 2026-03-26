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
# Query Intent Detection (ONLY for logging)
# --------------------------------------------------

def detect_query_department(query: str):

    query = query.lower()

    if any(word in query for word in [
        "leave", "vacation", "employee", "benefits", "hr",
        "payroll", "hiring", "recruitment", "policy"
    ]):
        return "hr"

    if any(word in query for word in [
        "expense", "reimbursement", "finance", "budget",
        "cost", "payment", "invoice", "travel"
    ]):
        return "finance"

    if any(word in query for word in [
        "code", "engineering", "api", "system",
        "architecture", "backend", "frontend", "deployment"
    ]):
        return "engineering"

    return "general"


# --------------------------------------------------
# Rerank
# --------------------------------------------------

def rerank_chunks(query: str, chunks: List[dict], top_k: int = 5):

    query_words = set(query.lower().split())
    scored = []

    for chunk in chunks:

        text = chunk["text"].lower()
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
#         temperature=0,
#     )

#     return response.choices[0].message.content.strip()


def generate_answer_from_llm(query: str, context: str, history):

    system_prompt = """
You are AstraMind, an enterprise knowledge assistant.

Rules:
1. Answer using ONLY the provided context.
2. Use chat history if needed to understand follow-up questions.
3. Be direct.
4. Do NOT hallucinate.
"""

    # ✅ FORMAT HISTORY PROPERLY
    messages = [{"role": "system", "content": system_prompt.strip()}]

    # Limit history (avoid token overflow)
    recent_history = history[-6:]

    for msg in recent_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # ✅ ADD CURRENT QUESTION WITH CONTEXT
    user_prompt = f"""
Context:
{context}

Question:
{query}
"""

    messages.append({
        "role": "user",
        "content": user_prompt.strip()
    })

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0,
    )

    return response.choices[0].message.content.strip()


    

# --------------------------------------------------
# RAG Pipeline (FINAL PRODUCTION VERSION)
# --------------------------------------------------

def generate_rag_answer(query: str, session_id: str, user_group_ids: list, allowed_departments=None):

    # ✅ Resolve allowed departments
    if allowed_departments is None:
        allowed_departments = resolve_departments(user_group_ids)

    logger.info(f"USER GROUP IDS: {user_group_ids}")
    logger.info(f"ALLOWED DEPARTMENTS: {allowed_departments}")

    # (Only for debug visibility — not used for blocking)
    detected_department = detect_query_department(query)
    logger.info(f"DETECTED QUERY DEPARTMENT: {detected_department}")

    history = memory.get_history(session_id)

    rewritten_query = rewrite_query(query)
    logger.info(f"REWRITTEN QUERY: {rewritten_query}")

    # 🔍 Retrieval (THIS is your real access control)
    retrieved_chunks = search_text(
        rewritten_query,
        department=allowed_departments,
        limit=30
    )

    # 🔒 Strict safety filter
    retrieved_chunks = [
        c for c in retrieved_chunks
        if c.get("department") in allowed_departments
    ]

    logger.info(f"RETRIEVED CHUNKS COUNT: {len(retrieved_chunks)}")

    # ⚠️ No data found (NOT access issue)
    if not retrieved_chunks:
        logger.warning("NO DATA FOUND FOR ALLOWED DEPARTMENTS")

        return {
            "question": query,
            "answer": "I could not find information about this in your accessible knowledge base.",
            "confidence": 0.0,
            "grounded": False,
            "sources": [],
            "evaluation": "No data found",
            "context_used": [],
            "session_id": session_id
        }

    # 🚫 Remove GitHub noise
    non_repo_chunks = [
        c for c in retrieved_chunks
        if "github" not in c.get("source", "").lower()
    ]

    if non_repo_chunks:
        retrieved_chunks = non_repo_chunks

    # 📊 Rerank
    reranked_chunks = rerank_chunks(query, retrieved_chunks, top_k=5)

    texts = [chunk["text"] for chunk in reranked_chunks]
    sources = list({chunk["source"] for chunk in reranked_chunks})[:3]

    context = build_context(texts)

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS]

    answer = generate_answer_from_llm(query, context, history)

    return {
        "question": query,
        "answer": answer,
        "confidence": calculate_confidence(texts),
        "grounded": True,
        "sources": sources,
        "evaluation": "Department-filtered pipeline (retrieval-only access control)",
        "context_used": texts,
        "session_id": session_id
    }