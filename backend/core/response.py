# backend/core/response.py
"""
Standardized API response envelope.

All endpoints return responses in this shape:
{
  "success": true,
  "request_id": "abc-123",
  "data": { ... },          # on success
  "error": null
}

{
  "success": false,
  "request_id": "abc-123",
  "data": null,
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "...",
    "detail": { ... }
  }
}

Why a consistent envelope?
- Frontend can always check response.success first
- Error logging can always extract request_id
- API versioning becomes simpler
- Clients don't need to guess error shapes
"""

from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel, Field
from datetime import datetime, timezone

T = TypeVar("T")


class ErrorBody(BaseModel):
    code: str
    message: str
    detail: Optional[Any] = None


class APIResponse(BaseModel, Generic[T]):
    """
    Generic response envelope.
    T is the type of the data payload — fully typed in route return annotations.
    """
    success: bool
    request_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: Optional[T] = None
    error: Optional[ErrorBody] = None


def success_response(data: Any, request_id: str) -> dict:
    """Build a success envelope. Returns dict for FastAPI JSONResponse."""
    return APIResponse(
        success=True,
        request_id=request_id,
        data=data,
    ).model_dump(mode="json")


def error_response(
    code: str,
    message: str,
    request_id: str,
    detail: Any = None,
) -> dict:
    """Build an error envelope."""
    return APIResponse(
        success=False,
        request_id=request_id,
        error=ErrorBody(code=code, message=message, detail=detail),
    ).model_dump(mode="json")