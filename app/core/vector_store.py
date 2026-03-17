# import os
# from typing import Union, List

# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchValue,
# )

# from app.core.embeddings import generate_embedding
# from app.core.logger import logger
# from app.config import QDRANT_HOST, QDRANT_PORT


# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


# # --------------------------------------------------
# # Qdrant Connection
# # --------------------------------------------------

# if QDRANT_API_KEY:
#     client = QdrantClient(
#         url=f"https://{QDRANT_HOST}",
#         api_key=QDRANT_API_KEY
#     )
# else:
#     client = QdrantClient(
#         host=QDRANT_HOST,
#         port=QDRANT_PORT
#     )


# COLLECTION_NAME = "astramind_collection"


# # --------------------------------------------------
# # Create Collection
# # --------------------------------------------------

# def create_collection():

#     try:

#         existing = client.get_collections()
#         collection_names = [c.name for c in existing.collections]

#         if COLLECTION_NAME in collection_names:
#             logger.info("Collection already exists.")
#             return

#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(
#                 size=1536,
#                 distance=Distance.COSINE,
#             ),
#         )

#         client.create_payload_index(
#             collection_name=COLLECTION_NAME,
#             field_name="department",
#             field_schema="keyword"
#         )

#         logger.info("Vector collection created successfully.")

#     except Exception as e:

#         logger.error(f"Collection creation failed: {str(e)}")
#         raise


# # --------------------------------------------------
# # Add Text
# # --------------------------------------------------

# def add_text(text: str, doc_id: str, metadata: dict = None):

#     try:

#         embedding = generate_embedding(text)

#         payload = metadata.copy() if metadata else {}
#         payload["text"] = text

#         client.upsert(
#             collection_name=COLLECTION_NAME,
#             points=[
#                 PointStruct(
#                     id=doc_id,
#                     vector=embedding,
#                     payload=payload
#                 )
#             ]
#         )

#     except Exception as e:
#         logger.error(f"Vector store upsert failed: {str(e)}")
#         raise


# # --------------------------------------------------
# # Secure Search
# # --------------------------------------------------

# def search_text(
#     query: str,
#     department: Union[str, List[str]] = None,
#     limit: int = 5
# ):

#     try:

#         query_vector = generate_embedding(query)

#         # STRICT FILTER
#         if isinstance(department, str):

#             search_filter = Filter(
#                 must=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchValue(value=department)
#                     )
#                 ]
#             )

#         elif isinstance(department, list) and department:

#             search_filter = Filter(
#                 must=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchValue(value=dept)
#                     )
#                     for dept in department
#                 ]
#             )

#         else:
#             search_filter = None

#         results = client.query_points(
#             collection_name=COLLECTION_NAME,
#             query=query_vector,
#             limit=20,
#             query_filter=search_filter
#         )

#         payloads = [p.payload for p in results.points]

#         final_results = []

#         seen = set()

#         for payload in payloads:

#             text = payload.get("text")

#             if text and text not in seen:

#                 seen.add(text)

#                 final_results.append({
#                     "text": text,
#                     "source": payload.get("source", "unknown"),
#                     "department": payload.get("department", "unknown"),
#                     "type": payload.get("type", "unknown")
#                 })

#         return final_results[:limit]

#     except Exception as e:

#         logger.error(f"Vector search failed: {str(e)}")
#         raise
























# import os
# from typing import Union, List

# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchValue,
# )

# from app.core.embeddings import generate_embedding
# from app.core.logger import logger
# from app.config import QDRANT_HOST, QDRANT_PORT


# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# # lowered threshold for better recall
# SIMILARITY_THRESHOLD = 0.45


# # --------------------------------------------------
# # Qdrant Connection
# # --------------------------------------------------

# if QDRANT_API_KEY:
#     client = QdrantClient(
#         url=f"https://{QDRANT_HOST}",
#         api_key=QDRANT_API_KEY
#     )
# else:
#     client = QdrantClient(
#         host=QDRANT_HOST,
#         port=QDRANT_PORT
#     )


# COLLECTION_NAME = "astramind_collection"


# # --------------------------------------------------
# # Create Collection
# # --------------------------------------------------

# def create_collection():

#     try:

#         existing = client.get_collections()
#         collection_names = [c.name for c in existing.collections]

#         if COLLECTION_NAME in collection_names:
#             logger.info("Collection already exists.")
#             return

#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(
#                 size=1536,
#                 distance=Distance.COSINE,
#             ),
#         )

#         client.create_payload_index(
#             collection_name=COLLECTION_NAME,
#             field_name="department",
#             field_schema="keyword"
#         )

#         logger.info("Vector collection created successfully.")

#     except Exception as e:

#         logger.error(f"Collection creation failed: {str(e)}")
#         raise


# # --------------------------------------------------
# # Add Text
# # --------------------------------------------------

# def add_text(text: str, doc_id: str, metadata: dict = None):

#     try:

#         embedding = generate_embedding(text)

#         payload = metadata.copy() if metadata else {}
#         payload["text"] = text

#         client.upsert(
#             collection_name=COLLECTION_NAME,
#             points=[
#                 PointStruct(
#                     id=doc_id,
#                     vector=embedding,
#                     payload=payload
#                 )
#             ]
#         )

#     except Exception as e:
#         logger.error(f"Vector store upsert failed: {str(e)}")
#         raise


# # --------------------------------------------------
# # Secure Hybrid Search
# # --------------------------------------------------

# def search_text(
#     query: str,
#     department: Union[str, List[str]] = None,
#     limit: int = 5
# ):

#     try:

#         query_vector = generate_embedding(query)

#         # ----------------------------
#         # Department Filtering
#         # ----------------------------

#         if isinstance(department, str):

#             search_filter = Filter(
#                 must=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchValue(value=department)
#                     )
#                 ]
#             )

#         elif isinstance(department, list) and department:

#             search_filter = Filter(
#                 should=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchValue(value=dept)
#                     )
#                     for dept in department
#                 ]
#             )

#         else:
#             search_filter = None

#         # ----------------------------
#         # Vector Search
#         # ----------------------------

#         results = client.query_points(
#             collection_name=COLLECTION_NAME,
#             query=query_vector,
#             limit=20,
#             query_filter=search_filter
#         )

#         final_results = []
#         seen = set()

#         for p in results.points:

#             score = p.score

#             print("VECTOR SCORE:", score)

#             if score < SIMILARITY_THRESHOLD:
#                 continue

#             payload = p.payload
#             text = payload.get("text")

#             if not text:
#                 continue

#             if text in seen:
#                 continue

#             seen.add(text)

#             final_results.append({
#                 "text": text,
#                 "source": payload.get("source", "unknown"),
#                 "department": payload.get("department", "unknown"),
#                 "type": payload.get("type", "unknown"),
#                 "vector_score": score
#             })

#         # ----------------------------
#         # Hybrid keyword boost
#         # ----------------------------

#         keywords = query.lower().split()

#         for r in final_results:

#             text = r["text"].lower()

#             keyword_hits = sum(1 for w in keywords if w in text)

#             r["keyword_score"] = keyword_hits

#             r["hybrid_score"] = r["vector_score"] + (keyword_hits * 0.05)

#         final_results.sort(
#             key=lambda x: x["hybrid_score"],
#             reverse=True
#         )

#         return final_results[:limit]

#     except Exception as e:

#         logger.error(f"Vector search failed: {str(e)}")
#         raise



















# import os
# from typing import Union, List

# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchValue,
#     MatchAny
# )

# from app.core.embeddings import generate_embedding
# from app.core.logger import logger
# from app.config import QDRANT_HOST, QDRANT_PORT


# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# SIMILARITY_THRESHOLD = 0.15


# # --------------------------------------------------
# # Qdrant Connection
# # --------------------------------------------------

# if QDRANT_API_KEY:
#     client = QdrantClient(
#         url=f"https://{QDRANT_HOST}",
#         api_key=QDRANT_API_KEY
#     )
# else:
#     client = QdrantClient(
#         host=QDRANT_HOST,
#         port=QDRANT_PORT
#     )


# COLLECTION_NAME = "astramind_collection"


# # --------------------------------------------------
# # Normalize Department
# # --------------------------------------------------

# VALID_DEPARTMENTS = {
#     "general",
#     "engineering",
#     "finance",
#     "hr",
#     "research"
# }


# def normalize_department(department: str):

#     if not department:
#         return "general"

#     department = department.strip().lower()

#     if department not in VALID_DEPARTMENTS:
#         logger.warning(f"Invalid department '{department}', defaulting to general")
#         return "general"

#     return department


# # --------------------------------------------------
# # Create Collection
# # --------------------------------------------------

# def create_collection():

#     try:

#         existing = client.get_collections()
#         collection_names = [c.name for c in existing.collections]

#         if COLLECTION_NAME in collection_names:
#             logger.info("Collection already exists.")
#             return

#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(
#                 size=1536,
#                 distance=Distance.COSINE,
#             ),
#         )

#         client.create_payload_index(
#             collection_name=COLLECTION_NAME,
#             field_name="department",
#             field_schema="keyword"
#         )

#         logger.info("Vector collection created successfully.")

#     except Exception as e:

#         logger.error(f"Collection creation failed: {str(e)}")
#         raise


# # --------------------------------------------------
# # Add Text (WITH METADATA VALIDATION)
# # --------------------------------------------------

# def add_text(text: str, doc_id: str, metadata: dict = None):

#     try:

#         embedding = generate_embedding(text)

#         payload = metadata.copy() if metadata else {}

#         # -------------------------------
#         # Department validation
#         # -------------------------------

#         department = payload.get("department", "general")
#         payload["department"] = normalize_department(department)

#         payload["text"] = text

#         client.upsert(
#             collection_name=COLLECTION_NAME,
#             points=[
#                 PointStruct(
#                     id=doc_id,
#                     vector=embedding,
#                     payload=payload
#                 )
#             ]
#         )

#     except Exception as e:
#         logger.error(f"Vector store upsert failed: {str(e)}")
#         raise


# # --------------------------------------------------
# # Secure Department Filtered Search
# # --------------------------------------------------

# def search_text(
#     query: str,
#     department: Union[str, List[str]] = None,
#     limit: int = 5
# ):

#     try:

#         query_vector = generate_embedding(query)

#         search_filter = None

#         # --------------------------------------------------
#         # STRICT Department Filtering
#         # --------------------------------------------------

#         if isinstance(department, str):

#             department = normalize_department(department)

#             search_filter = Filter(
#                 must=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchValue(value=department)
#                     )
#                 ]
#             )

#         elif isinstance(department, list) and department:

#             department = [
#                 normalize_department(d) for d in department
#             ]

#             search_filter = Filter(
#                 must=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchAny(any=department)
#                     )
#                 ]
#             )

#         # --------------------------------------------------
#         # Vector Search
#         # --------------------------------------------------

#         results = client.query_points(
#             collection_name=COLLECTION_NAME,
#             query=query_vector,
#             limit=20,
#             query_filter=search_filter
#         )

#         final_results = []
#         seen = set()

#         for p in results.points:

#             score = p.score

#             if score < SIMILARITY_THRESHOLD:
#                 continue

#             payload = p.payload
#             text = payload.get("text")

#             if not text:
#                 continue

#             if text in seen:
#                 continue

#             seen.add(text)

#             final_results.append({
#                 "text": text,
#                 "source": payload.get("source", "unknown"),
#                 "department": payload.get("department", "unknown"),
#                 "type": payload.get("type", "unknown"),
#                 "score": score
#             })

#         # --------------------------------------------------
#         # Keyword Boost
#         # --------------------------------------------------

#         keywords = query.lower().split()

#         boosted = []

#         for r in final_results:

#             text = r["text"].lower()

#             keyword_hits = sum(1 for w in keywords if w in text)

#             r["keyword_score"] = keyword_hits

#             boosted.append(r)

#         boosted.sort(key=lambda x: (x["keyword_score"], x["score"]), reverse=True)

#         return boosted[:limit]

#     except Exception as e:

#         logger.error(f"Vector search failed: {str(e)}")
#         raise


















# import os
# from typing import Union, List

# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchValue,
#     MatchAny
# )

# from app.core.embeddings import generate_embedding
# from app.core.logger import logger
# from app.config import QDRANT_HOST, QDRANT_PORT


# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# SIMILARITY_THRESHOLD = 0.15


# # --------------------------------------------------
# # Qdrant Connection
# # --------------------------------------------------

# if QDRANT_API_KEY:
#     client = QdrantClient(
#         url=f"https://{QDRANT_HOST}",
#         api_key=QDRANT_API_KEY
#     )
# else:
#     client = QdrantClient(
#         host=QDRANT_HOST,
#         port=QDRANT_PORT
#     )


# COLLECTION_NAME = "astramind_collection"


# # --------------------------------------------------
# # Normalize Department
# # --------------------------------------------------

# VALID_DEPARTMENTS = {
#     "general",
#     "engineering",
#     "finance",
#     "hr",
#     "research"
# }


# def normalize_department(department: str):

#     if not department:
#         return "general"

#     department = department.strip().lower()

#     if department not in VALID_DEPARTMENTS:
#         logger.warning(f"Invalid department '{department}', defaulting to general")
#         return "general"

#     return department


# # --------------------------------------------------
# # Create Collection
# # --------------------------------------------------

# def create_collection():

#     try:

#         existing = client.get_collections()
#         collection_names = [c.name for c in existing.collections]

#         if COLLECTION_NAME in collection_names:
#             logger.info("Collection already exists.")
#             return

#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(
#                 size=1536,
#                 distance=Distance.COSINE,
#             ),
#         )

#         client.create_payload_index(
#             collection_name=COLLECTION_NAME,
#             field_name="department",
#             field_schema="keyword"
#         )

#         logger.info("Vector collection created successfully.")

#     except Exception as e:

#         logger.error(f"Collection creation failed: {str(e)}")
#         raise


# # --------------------------------------------------
# # Add Text
# # --------------------------------------------------

# def add_text(text: str, doc_id: str, metadata: dict = None):

#     try:

#         embedding = generate_embedding(text)

#         payload = metadata.copy() if metadata else {}

#         department = payload.get("department", "general")
#         payload["department"] = normalize_department(department)

#         payload["text"] = text

#         client.upsert(
#             collection_name=COLLECTION_NAME,
#             points=[
#                 PointStruct(
#                     id=doc_id,
#                     vector=embedding,
#                     payload=payload
#                 )
#             ]
#         )

#     except Exception as e:
#         logger.error(f"Vector store upsert failed: {str(e)}")
#         raise


# # --------------------------------------------------
# # Tiered Retrieval Strategy
# # --------------------------------------------------

# def search_text(
#     query: str,
#     department: Union[str, List[str]] = None,
#     limit: int = 5
# ):

#     try:

#         query_vector = generate_embedding(query)

#         search_filter = None

#         if isinstance(department, str):

#             department = normalize_department(department)

#             search_filter = Filter(
#                 must=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchValue(value=department)
#                     )
#                 ]
#             )

#         elif isinstance(department, list) and department:

#             department = [normalize_department(d) for d in department]

#             search_filter = Filter(
#                 must=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchAny(any=department)
#                     )
#                 ]
#             )

#         results = client.query_points(
#             collection_name=COLLECTION_NAME,
#             query=query_vector,
#             limit=40,
#             query_filter=search_filter
#         )

#         docs = []
#         repo_docs = []
#         repo_code = []

#         seen = set()

#         for p in results.points:

#             score = p.score

#             if score < SIMILARITY_THRESHOLD:
#                 continue

#             payload = p.payload or {}

#             text = payload.get("text")

#             if not text or text in seen:
#                 continue

#             seen.add(text)

#             result = {
#                 "text": text,
#                 "source": payload.get("source", "unknown"),
#                 "department": payload.get("department", "unknown"),
#                 "type": payload.get("type", "unknown"),
#                 "score": score
#             }

#             # Tier classification
#             if payload.get("type") in ["pdf", "url"]:
#                 docs.append(result)

#             elif payload.get("type") == "repo":

#                 source = payload.get("source", "")

#                 if source.endswith(".md") or source.endswith(".txt"):
#                     repo_docs.append(result)
#                 else:
#                     repo_code.append(result)

#         final_results = []

#         # Stage 1 → PDFs + URLs
#         for r in docs:
#             if len(final_results) < limit:
#                 final_results.append(r)

#         # Stage 2 → repo documentation
#         for r in repo_docs:
#             if len(final_results) < limit:
#                 final_results.append(r)

#         # Stage 3 → repo code
#         for r in repo_code:
#             if len(final_results) < limit:
#                 final_results.append(r)

#         return final_results

#     except Exception as e:

#         logger.error(f"Vector search failed: {str(e)}")
#         raise















import os
from typing import Union, List

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    MatchAny
)

from app.core.embeddings import generate_embedding
from app.core.logger import logger
from app.config import QDRANT_HOST, QDRANT_PORT


QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

SIMILARITY_THRESHOLD = 0.15


# --------------------------------------------------
# Qdrant Connection
# --------------------------------------------------

if QDRANT_API_KEY:
    client = QdrantClient(
        url=f"https://{QDRANT_HOST}",
        api_key=QDRANT_API_KEY
    )
else:
    client = QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT
    )


COLLECTION_NAME = "astramind_collection"


# --------------------------------------------------
# Normalize Department
# --------------------------------------------------

VALID_DEPARTMENTS = {
    "general",
    "engineering",
    "finance",
    "hr",
    "research"
}


def normalize_department(department: str):

    if not department:
        return "general"

    department = department.strip().lower()

    if department not in VALID_DEPARTMENTS:
        logger.warning(f"Invalid department '{department}', defaulting to general")
        return "general"

    return department


# --------------------------------------------------
# Create Collection
# --------------------------------------------------

def create_collection():

    try:

        existing = client.get_collections()
        collection_names = [c.name for c in existing.collections]

        if COLLECTION_NAME in collection_names:
            logger.info("Collection already exists.")
            return

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE,
            ),
        )

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="department",
            field_schema="keyword"
        )

        logger.info("Vector collection created successfully.")

    except Exception as e:

        logger.error(f"Collection creation failed: {str(e)}")
        raise


# --------------------------------------------------
# Add Text
# --------------------------------------------------

def add_text(text: str, doc_id: str, metadata: dict = None):

    try:

        embedding = generate_embedding(text)

        payload = metadata.copy() if metadata else {}

        department = payload.get("department", "general")
        payload["department"] = normalize_department(department)

        payload["text"] = text

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )

    except Exception as e:
        logger.error(f"Vector store upsert failed: {str(e)}")
        raise


# --------------------------------------------------
# Search Text
# --------------------------------------------------

def search_text(
    query: str,
    department: Union[str, List[str]] = None,
    limit: int = 5
):

    try:

        query_vector = generate_embedding(query)

        search_filter = None

        # --------------------------------------------------
        # Allow department + general documents
        # --------------------------------------------------

        if isinstance(department, str):

            department = normalize_department(department)

            search_filter = Filter(
                should=[
                    FieldCondition(
                        key="department",
                        match=MatchValue(value=department)
                    ),
                    FieldCondition(
                        key="department",
                        match=MatchValue(value="general")
                    )
                ]
            )

        elif isinstance(department, list) and department:

            department = [
                normalize_department(d) for d in department
            ]

            department.append("general")

            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="department",
                        match=MatchAny(any=department)
                    )
                ]
            )

        # --------------------------------------------------
        # Vector Search
        # --------------------------------------------------

        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=20,
            query_filter=search_filter
        )

        final_results = []
        seen = set()

        for p in results.points:

            score = p.score

            if score < SIMILARITY_THRESHOLD:
                continue

            payload = p.payload
            text = payload.get("text")

            if not text:
                continue

            if text in seen:
                continue

            seen.add(text)

            final_results.append({
                "text": text,
                "source": payload.get("source", "unknown"),
                "department": payload.get("department", "unknown"),
                "type": payload.get("type", "unknown"),
                "score": score
            })

        return final_results[:limit]

    except Exception as e:

        logger.error(f"Vector search failed: {str(e)}")
        raise
