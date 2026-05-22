from sentence_transformers import SentenceTransformer
from typing import List, Dict

from backend.utils.config import settings
from backend.utils.logger import app_logger


class EmbeddingGenerator:
    def __init__(self):
        app_logger.info(
            f"Loading embedding model: {settings.EMBEDDING_MODEL}"
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        app_logger.info("Embedding model loaded successfully")

    def generate_embeddings(
        self,
        chunks: List[Dict]
    ) -> List[Dict]:

        app_logger.info("Generating embeddings for chunks")

        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            embedded_chunks.append(
                {
                    "content": chunk["content"],
                    "embedding": embedding.tolist(),
                    "page_number": chunk["page_number"],
                    "source": chunk["source"],
                }
            )

        app_logger.info(
            f"Generated embeddings for {len(embedded_chunks)} chunks"
        )

        return embedded_chunks