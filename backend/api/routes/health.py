import requests

from fastapi import APIRouter, Request

from backend.core.response import APIResponse

from backend.models.schemas import (
    HealthResponse,
    ComponentHealth,
)

from backend.rag.vector_store import VectorStore

from backend.utils.config import settings
from backend.utils.logger import app_logger


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=APIResponse,
)
def health_check(request: Request):

    app_logger.info("Running health check")

    # ==========================================
    # CHECK VECTOR DATABASE
    # ==========================================

    vector_store_status = "healthy"

    try:

        vector_store = VectorStore()

        stats = vector_store.get_collection_stats()

    except Exception as e:

        vector_store_status = f"unhealthy: {str(e)}"

        stats = {}

    # ==========================================
    # CHECK OLLAMA
    # ==========================================

    ollama_status = "healthy"

    try:

        response = requests.get(
            f"{settings.OLLAMA_BASE_URL}/api/tags"
        )

        if response.status_code != 200:

            ollama_status = "unhealthy"

    except Exception as e:

        ollama_status = f"unhealthy: {str(e)}"

    # ==========================================
    # BUILD RESPONSE
    # ==========================================

    health_data = HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        uptime_seconds=0,
        components={
            "vector_database": ComponentHealth(
                status=vector_store_status
            ),
            "ollama": ComponentHealth(
                status=ollama_status
            ),
        },
        total_documents=stats.get(
            "total_documents",
            0,
        ),
    )

    app_logger.info("Health check completed")

    return APIResponse(
    success=True,
    message="Health check successful",
    request_id=request.state.request_id,
    data=health_data.model_dump(),
)