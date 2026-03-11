# import os
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

# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# client = QdrantClient(
#     url=f"https://{QDRANT_HOST}",
#     api_key=QDRANT_API_KEY
# )

# COLLECTION_NAME = "astramind_collection"


# def create_collection():

#     try:

#         existing = client.get_collections()
#         collection_names = [c.name for c in existing.collections]

#         if COLLECTION_NAME in collection_names:
#             logger.info("Collection already exists. Skipping creation.")
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

#         semantic_results = client.query_points(
#             collection_name=COLLECTION_NAME,
#             query=query_vector,
#             limit=20,
#             query_filter=search_filter
#         )

#         semantic_payloads = [p.payload for p in semantic_results.points]

#         seen = set()
#         final_payloads = []

#         for payload in semantic_payloads:

#             text = payload.get("text")

#             if text and text not in seen:

#                 seen.add(text)

#                 final_payloads.append({
#                     "text": text,
#                     "source": payload.get("source", "unknown"),
#                     "type": payload.get("type", "unknown")
#                 })

#         return final_payloads[:limit]

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


QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# --------------------------------------------------
# Qdrant Connection
# --------------------------------------------------

if QDRANT_API_KEY:
    # Cloud connection
    client = QdrantClient(
        url=f"https://{QDRANT_HOST}",
        api_key=QDRANT_API_KEY
    )
else:
    # Local connection
    client = QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT
    )


COLLECTION_NAME = "astramind_collection"


# --------------------------------------------------
# Create Collection
# --------------------------------------------------

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


# --------------------------------------------------
# Add Text
# --------------------------------------------------

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


# --------------------------------------------------
# Search
# --------------------------------------------------

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

        semantic_results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=20,
            query_filter=search_filter
        )

        semantic_payloads = [p.payload for p in semantic_results.points]

        seen = set()
        final_payloads = []

        for payload in semantic_payloads:

            text = payload.get("text")

            if text and text not in seen:

                seen.add(text)

                final_payloads.append({
                    "text": text,
                    "source": payload.get("source", "unknown"),
                    "type": payload.get("type", "unknown")
                })

        return final_payloads[:limit]

    except Exception as e:

        logger.error(f"Vector search failed: {str(e)}")
        raise