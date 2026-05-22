from typing import List, Dict

from backend.utils.config import settings
from backend.utils.logger import app_logger


class TextChunker:
    def __init__(
        self,
        chunk_size: int = settings.CHUNK_SIZE,
        chunk_overlap: int = settings.CHUNK_OVERLAP,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(
        self,
        documents: List[Dict]
    ) -> List[Dict]:

        app_logger.info("Starting document chunking")

        chunks = []

        for document in documents:
            page_number = document["page_number"]
            text = document["text"]
            source = document["source"]

            page_chunks = self.chunk_text(
                text=text,
                page_number=page_number,
                source=source,
            )

            chunks.extend(page_chunks)

        app_logger.info(
            f"Chunking completed. Total chunks created: {len(chunks)}"
        )

        return chunks

    def chunk_text(
        self,
        text: str,
        page_number: int,
        source: str,
    ) -> List[Dict]:

        text_chunks = []

        start = 0

        while start < len(text):
            end = start + self.chunk_size

            chunk = text[start:end]

            text_chunks.append(
                {
                    "content": chunk,
                    "page_number": page_number,
                    "source": source,
                }
            )

            start += self.chunk_size - self.chunk_overlap

        return text_chunks