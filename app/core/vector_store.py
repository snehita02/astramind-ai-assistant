# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchValue
# )
# from app.core.embeddings import generate_embedding
# from app.core.logger import logger
# from app.config import QDRANT_HOST, QDRANT_PORT

# client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# COLLECTION_NAME = "astramind_collection"


# def create_collection():
#     client.recreate_collection(
#         collection_name=COLLECTION_NAME,
#         vectors_config=VectorParams(
#             size=1536,
#             distance=Distance.COSINE,
#         ),
#     )

#     # Payload index for department filtering
#     client.create_payload_index(
#         collection_name=COLLECTION_NAME,
#         field_name="department",
#         field_schema="keyword"
#     )


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


# def search_text(query: str, department: str = None, limit: int = 5):

#     try:
#         query_vector = generate_embedding(query)

#         search_filter = None

#         if department:
#             search_filter = Filter(
#                 must=[
#                     FieldCondition(
#                         key="department",
#                         match=MatchValue(value=department)
#                     )
#                 ]
#             )

#         # ----------------------------------------
#         # 1️⃣ Detect generic repository question
#         # ----------------------------------------
#         generic_repo_keywords = [
#             "what does this repository do",
#             "what is this repository",
#             "what is this project",
#             "about this repository",
#             "about this project"
#         ]

#         is_generic_repo_query = any(
#             phrase in query.lower()
#             for phrase in generic_repo_keywords
#         )

#         readme_payloads = []

#         if is_generic_repo_query and department:

#             # 🔥 Fetch README chunks directly by metadata ONLY
#             readme_filter = Filter(
#                 must=[
#                     FieldCondition(
#                     key="department",
#                     match=MatchValue(value=department)
#                     ),
#                     FieldCondition(
#                     key="is_primary_chunk",
#                     match=MatchValue(value=True)
#                     )
#                 ]
#             )

#             scroll_result = client.scroll(
#                 collection_name=COLLECTION_NAME,
#                 scroll_filter=readme_filter,
#                 limit=50,
#                 with_payload=True
#             )

#             readme_payloads = [point.payload for point in scroll_result[0]]

#         # ----------------------------------------
#         # 2️⃣ Semantic search fallback
#         # ----------------------------------------
#         semantic_results = client.query_points(
#             collection_name=COLLECTION_NAME,
#             query=query_vector,
#             limit=20,
#             query_filter=search_filter
#         )

#         semantic_payloads = [p.payload for p in semantic_results.points]

#         # ----------------------------------------
#         # 3️⃣ Merge (README first)
#         # ----------------------------------------
#         combined = readme_payloads + semantic_payloads

#         seen = set()
#         final_payloads = []

#         for payload in combined:
#             text = payload.get("text")
#             if text and text not in seen:
#                 seen.add(text)
#                 final_payloads.append(payload)

#         # ----------------------------------------
#         # 4️⃣ Return top chunks
#         # ----------------------------------------
#         retrieved = []

#         for payload in final_payloads[:limit]:
#             retrieved.append(payload["text"])

#         return retrieved

#     except Exception as e:
#         logger.error(f"Vector search failed: {str(e)}")
#         raise




import os
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

from app.core.embeddings import generate_embedding
from app.core.logger import logger
from app.config import QDRANT_HOST, QDRANT_PORT

# ============================================================
# Qdrant Cloud Authentication
# ============================================================

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# client = QdrantClient(
#     host=QDRANT_HOST,
#     port=QDRANT_PORT,
#     api_key=QDRANT_API_KEY
# )
client = QdrantClient(
    url=f"https://{QDRANT_HOST}",
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "astramind_collection"


# ============================================================
# Collection Creation
# ============================================================

def create_collection():

    try:

        existing = client.get_collections()

        collection_names = [c.name for c in existing.collections]

        if COLLECTION_NAME in collection_names:
            logger.info("Collection already exists. Skipping creation.")
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

# ============================================================
# Add Text to Vector Store
# ============================================================

def add_text(text: str, doc_id: str, metadata: dict = None):
    try:
        embedding = generate_embedding(text)

        payload = metadata.copy() if metadata else {}
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


# ============================================================
# Vector Search
# ============================================================

def search_text(query: str, department: str = None, limit: int = 5):

    try:
        query_vector = generate_embedding(query)

        search_filter = None

        if department:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="department",
                        match=MatchValue(value=department)
                    )
                ]
            )

        # ------------------------------------------------------------
        # Detect generic repository question
        # ------------------------------------------------------------
        generic_repo_keywords = [
            "what does this repository do",
            "what is this repository",
            "what is this project",
            "about this repository",
            "about this project"
        ]

        is_generic_repo_query = any(
            phrase in query.lower()
            for phrase in generic_repo_keywords
        )

        readme_payloads = []

        if is_generic_repo_query and department:

            readme_filter = Filter(
                must=[
                    FieldCondition(
                        key="department",
                        match=MatchValue(value=department)
                    ),
                    FieldCondition(
                        key="is_primary_chunk",
                        match=MatchValue(value=True)
                    )
                ]
            )

            scroll_result = client.scroll(
                collection_name=COLLECTION_NAME,
                scroll_filter=readme_filter,
                limit=50,
                with_payload=True
            )

            readme_payloads = [point.payload for point in scroll_result[0]]

        # ------------------------------------------------------------
        # Semantic Search
        # ------------------------------------------------------------

        semantic_results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=20,
            query_filter=search_filter
        )

        semantic_payloads = [p.payload for p in semantic_results.points]

        # ------------------------------------------------------------
        # Merge Results
        # ------------------------------------------------------------

        combined = readme_payloads + semantic_payloads

        seen = set()
        final_payloads = []

        for payload in combined:
            text = payload.get("text")

            if text and text not in seen:
                seen.add(text)
                final_payloads.append(payload)

        # ------------------------------------------------------------
        # Return Top Chunks
        # ------------------------------------------------------------

        retrieved = []

        for payload in final_payloads[:limit]:
            retrieved.append(payload["text"])

        return retrieved

    except Exception as e:
        logger.error(f"Vector search failed: {str(e)}")
        raise