from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.vector_store import VectorStore

from backend.utils.logger import app_logger


class Retriever:
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ):

        app_logger.info(
            f"Retrieving documents for query: {query}"
        )

        query_embedding = self.embedding_generator.model.encode(
            query
        ).tolist()

        results = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        retrieved_docs = []

        for idx, document in enumerate(results["documents"][0]):

            metadata = results["metadatas"][0][idx]

            retrieved_docs.append(
                {
                    "content": document,
                    "page_number": metadata["page_number"],
                    "source": metadata["source"],
                }
            )

        app_logger.info(
            f"Retrieved {len(retrieved_docs)} relevant chunks"
        )

        return retrieved_docs