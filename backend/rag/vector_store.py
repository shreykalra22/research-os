import uuid
from typing import List, Dict, Optional

import chromadb

from backend.utils.config import settings
from backend.utils.logger import app_logger


class VectorStore:

    def __init__(self):

        app_logger.info("Initializing ChromaDB client")

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_DIR
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME
        )

        app_logger.info(
            f"Connected to collection: {settings.COLLECTION_NAME}"
        )

    # ====================================================
    # ADD DOCUMENTS
    # ====================================================

    def add_documents(
        self,
        embedded_chunks: List[Dict],
    ) -> int:

        app_logger.info(
            f"Adding {len(embedded_chunks)} chunks to vector database"
        )

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in embedded_chunks:

            chunk_id = str(uuid.uuid4())

            ids.append(chunk_id)

            documents.append(
                chunk["content"]
            )

            embeddings.append(
                chunk["embedding"]
            )

            metadatas.append(
                {
                    "page_number": chunk["page_number"],
                    "source": chunk["source"],
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        app_logger.info(
            f"Successfully stored {len(ids)} vectors"
        )

        return len(ids)

    # ====================================================
    # SIMILARITY SEARCH
    # ====================================================

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 3,
        filters: Optional[Dict] = None,
    ) -> Dict:

        app_logger.info(
            f"Performing similarity search with top_k={top_k}"
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters,
        )

        return results

    # ====================================================
    # COLLECTION INFO
    # ====================================================

    def get_collection_stats(self) -> Dict:

        total_documents = self.collection.count()

        return {
            "collection_name": settings.COLLECTION_NAME,
            "total_documents": total_documents,
        }

    # ====================================================
    # DELETE DOCUMENTS
    # ====================================================

    def delete_documents_by_source(
        self,
        source: str,
    ):

        app_logger.info(
            f"Deleting documents for source: {source}"
        )

        self.collection.delete(
            where={
                "source": source
            }
        )

        app_logger.info(
            f"Documents deleted for source: {source}"
        )

    # ====================================================
    # RESET COLLECTION
    # ====================================================

    def reset_collection(self):

        app_logger.warning(
            "Resetting vector collection"
        )

        self.client.delete_collection(
            settings.COLLECTION_NAME
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME
        )

        app_logger.info(
            "Vector collection reset completed"
        )