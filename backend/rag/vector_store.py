import chromadb
from typing import List, Dict

from backend.utils.config import settings
from backend.utils.logger import app_logger


class VectorStore:
    def __init__(self):
        app_logger.info("Initializing ChromaDB")

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_DIR
        )

        self.collection = self.client.get_or_create_collection(
            name="research_documents"
        )

        app_logger.info("ChromaDB initialized successfully")

    def add_documents(
        self,
        embedded_chunks: List[Dict]
    ):

        app_logger.info(
            f"Adding {len(embedded_chunks)} chunks to vector database"
        )

        documents = []
        embeddings = []
        metadatas = []
        ids = []

        for index, chunk in enumerate(embedded_chunks):

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

            ids.append(
                f"chunk_{index}"
            )

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

        app_logger.info("Documents added successfully")

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 3,
    ):

        app_logger.info("Performing similarity search")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        return results