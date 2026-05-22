# backend/core/exceptions.py
"""
Typed exception hierarchy for ResearchOS.

Architecture principle: exceptions carry semantic meaning.
- Callers raise the right exception type (not RuntimeError)
- The API layer has ONE place that maps exceptions to HTTP responses
- Adding a new exception = add one class + one handler entry

Never raise HTTPException from services — that couples business logic
to the transport layer. Services raise domain exceptions; routes translate.
"""

from typing import Any


class ResearchOSException(Exception):
    """
    Base exception for all ResearchOS domain errors.
    Carries a machine-readable code for client handling.
    """
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", detail: Any = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.detail = detail


# ── Validation Errors (HTTP 400 / 422) ────────────────────────

class ValidationError(ResearchOSException):
    """Input failed validation — bad request from caller."""
    def __init__(self, message: str, detail: Any = None):
        super().__init__(message, code="VALIDATION_ERROR", detail=detail)


class FileTooLargeError(ResearchOSException):
    """Uploaded file exceeds the configured size limit."""
    def __init__(self, size_mb: float, limit_mb: int):
        super().__init__(
            f"File size {size_mb:.1f}MB exceeds {limit_mb}MB limit",
            code="FILE_TOO_LARGE",
            detail={"size_mb": size_mb, "limit_mb": limit_mb},
        )


class InvalidFileTypeError(ResearchOSException):
    """Uploaded file is not an accepted type."""
    def __init__(self, received: str, accepted: list[str]):
        super().__init__(
            f"File type '{received}' not accepted. Accepted: {accepted}",
            code="INVALID_FILE_TYPE",
            detail={"received": received, "accepted": accepted},
        )


class EmptyDocumentError(ResearchOSException):
    """PDF parsed successfully but contains no extractable text."""
    def __init__(self, filename: str):
        super().__init__(
            f"'{filename}' contains no extractable text. "
            "It may be a scanned image-only PDF.",
            code="EMPTY_DOCUMENT",
            detail={"filename": filename},
        )


# ── Not Found Errors (HTTP 404) ───────────────────────────────

class DocumentNotFoundError(ResearchOSException):
    """Requested document does not exist in the vector store."""
    def __init__(self, document_id: str):
        super().__init__(
            f"Document '{document_id}' not found",
            code="DOCUMENT_NOT_FOUND",
            detail={"document_id": document_id},
        )


# ── Processing Errors (HTTP 422) ──────────────────────────────

class IngestionError(ResearchOSException):
    """Failure during the ingestion pipeline."""
    def __init__(self, message: str, stage: str, detail: Any = None):
        super().__init__(message, code="INGESTION_ERROR", detail={"stage": stage, **(detail or {})})
        self.stage = stage


class ChunkingError(IngestionError):
    def __init__(self, message: str):
        super().__init__(message, stage="chunking")


class EmbeddingError(IngestionError):
    def __init__(self, message: str):
        super().__init__(message, stage="embedding")


# ── Infrastructure Errors (HTTP 503) ─────────────────────────

class VectorStoreError(ResearchOSException):
    """ChromaDB operation failed."""
    def __init__(self, message: str, operation: str = "unknown"):
        super().__init__(message, code="VECTOR_STORE_ERROR", detail={"operation": operation})


class LLMUnavailableError(ResearchOSException):
    """Ollama is not reachable or the model is not loaded."""
    def __init__(self, reason: str):
        super().__init__(
            f"LLM service unavailable: {reason}",
            code="LLM_UNAVAILABLE",
            detail={"reason": reason},
        )


class LLMTimeoutError(ResearchOSException):
    """LLM took too long to respond."""
    def __init__(self, timeout_seconds: int):
        super().__init__(
            f"LLM request timed out after {timeout_seconds}s",
            code="LLM_TIMEOUT",
            detail={"timeout_seconds": timeout_seconds},
        )


class RetrievalError(ResearchOSException):
    """Semantic retrieval failed."""
    def __init__(self, message: str):
        super().__init__(message, code="RETRIEVAL_ERROR")