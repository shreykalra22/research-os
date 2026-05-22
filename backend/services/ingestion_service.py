from pathlib import Path
from typing import Dict

from backend.services.pdf_parser import PDFParser
from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.vector_store import VectorStore

from backend.utils.logger import app_logger


class IngestionService:

    def __init__(self):

        self.parser = PDFParser()

        self.chunker = TextChunker()

        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = VectorStore()

    # ====================================================
    # MAIN INGESTION PIPELINE
    # ====================================================

    def ingest_document(
        self,
        file_path: str,
    ) -> Dict:

        app_logger.info(
            f"Starting ingestion pipeline for: {file_path}"
        )

        # ==========================================
        # VALIDATE FILE
        # ==========================================

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        # ==========================================
        # PARSE PDF
        # ==========================================

        parsed_pages = self.parser.parse_pdf(
            file_path
        )

        app_logger.info(
            f"Parsed {len(parsed_pages)} pages"
        )

        # ==========================================
        # CHUNK DOCUMENTS
        # ==========================================

        chunks = self.chunker.chunk_documents(
            parsed_pages
        )

        app_logger.info(
            f"Generated {len(chunks)} chunks"
        )

        # ==========================================
        # GENERATE EMBEDDINGS
        # ==========================================

        embedded_chunks = self.embedding_generator.generate_embeddings(
            chunks
        )

        app_logger.info(
            f"Generated embeddings for {len(embedded_chunks)} chunks"
        )

        # ==========================================
        # STORE IN VECTOR DB
        # ==========================================

        stored_count = self.vector_store.add_documents(
            embedded_chunks
        )

        app_logger.info(
            f"Stored {stored_count} vectors"
        )

        # ==========================================
        # RETURN INGESTION SUMMARY
        # ==========================================

        return {
            "status": "success",
            "file_name": path.name,
            "pages_processed": len(parsed_pages),
            "chunks_created": len(chunks),
            "vectors_stored": stored_count,
        }