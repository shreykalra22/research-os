# backend/models/schemas.py
"""
All Pydantic request/response models.

Design rules:
- Request models: strict validation, fail fast
- Response models: explicit fields, no Optional surprises
- Never expose internal IDs or implementation details
- Document every non-obvious field
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


# ── Enums ─────────────────────────────────────────────────────

class IngestionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentStatus(str, Enum):
    INDEXED = "indexed"
    FAILED = "failed"


# ── Upload / Ingestion ────────────────────────────────────────

class DocumentMetadata(BaseModel):
    filename: str
    total_pages: int
    total_chunks: int
    file_size_bytes: int
    ingested_at: datetime


class UploadResponse(BaseModel):
    document_id: str
    status: IngestionStatus
    message: str
    metadata: DocumentMetadata


class IngestionJobStatus(BaseModel):
    """
    Returned when upload is processed asynchronously.
    Client polls GET /documents/{document_id} to check completion.
    """
    document_id: str
    status: IngestionStatus
    queued_at: datetime


# ── Document Management ───────────────────────────────────────

class DocumentSummary(BaseModel):
    """Lightweight document record for listing."""
    document_id: str
    filename: str
    total_chunks: int
    ingested_at: Optional[datetime] = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentSummary]
    total: int


class DocumentDeleteResponse(BaseModel):
    document_id: str
    deleted_chunks: int
    message: str


# ── Chat / Retrieval ──────────────────────────────────────────

class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Natural language question to ask about uploaded documents",
    )
    document_id: Optional[str] = Field(
        default=None,
        description="Restrict search to a specific document. Omit to search all.",
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of source chunks to retrieve",
    )
    conversation_history: list[dict] = Field(
        default_factory=list,
        description="Prior turns: [{'role': 'user'|'assistant', 'content': '...'}]",
        max_length=10,  # prevent context explosion
    )

    @field_validator("query")
    @classmethod
    def question_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query must not be blank")
        return v.strip()

    @field_validator("conversation_history")
    @classmethod
    def validate_history_roles(cls, v: list[dict]) -> list[dict]:
        allowed_roles = {"user", "assistant"}
        for turn in v:
            if turn.get("role") not in allowed_roles:
                raise ValueError(f"history role must be one of {allowed_roles}")
            if not turn.get("content", "").strip():
                raise ValueError("history content must not be blank")
        return v


class CitationSource(BaseModel):
    """A single source chunk that contributed to the answer."""
    document_id: str
    filename: str
    page_number: int
    chunk_text: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    chunk_index: int


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[CitationSource]
    model: str
    retrieval_count: int
    has_context: bool = Field(
        description="False when no relevant chunks were found above the threshold"
    )


# ── Health ────────────────────────────────────────────────────

class ComponentHealth(BaseModel):
    status: str  # "ok" | "degraded" | "down"
    latency_ms: Optional[float] = None
    detail: Optional[str] = None


class HealthResponse(BaseModel):
    status: str  # "healthy" | "degraded" | "unhealthy"
    version: str
    uptime_seconds: float
    components: dict[str, ComponentHealth]


# ── Error (for OpenAPI docs) ──────────────────────────────────

class ErrorDetail(BaseModel):
    code: str
    message: str
    detail: Optional[dict] = None