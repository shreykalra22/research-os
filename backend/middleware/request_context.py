# backend/api/middleware.py
"""
Production middleware stack.

Request ID middleware: every request gets a UUID that propagates
through logs, service calls, and the response header. This is how
you correlate a user-reported error with a log entry.

Timing middleware: records total request duration for performance monitoring.
"""

import time
import uuid
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from backend.utils.logger import app_logger

logger = app_logger

# Thread-local equivalent for async contexts.
# Any code in the same async call chain can read the current request ID.
request_id_var: ContextVar[str] = ContextVar("request_id", default="no-request")


def get_request_id() -> str:
    """Read the current request's correlation ID from anywhere in the call chain."""
    return request_id_var.get()


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Assigns a unique ID to every request and injects it into:
    - The async context (readable by all downstream services)
    - The response headers (readable by clients for support queries)
    - All log entries via loguru's bind mechanism
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate or forward request ID (forwarded from upstream load balancer)
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_var.set(request_id)

        start = time.perf_counter()

        # Bind to logger context for this request
        with logger.contextualize(request_id=request_id):
            logger.info(f"{request.method} {request.url.path}")
            response = await call_next(request)

        duration_ms = (time.perf_counter() - start) * 1000

        # Inject metadata into response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-Ms"] = f"{duration_ms:.1f}"

        logger.info(
            f"{request.method} {request.url.path} → {response.status_code} "
            f"({duration_ms:.1f}ms)"
        )

        return response