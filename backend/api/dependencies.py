from backend.services.ingestion_service import IngestionService
from backend.services.retrieval_service import RetrievalService

from backend.utils.logger import app_logger


# ====================================================
# SINGLETON SERVICE INSTANCES
# ====================================================

app_logger.info("Initializing service dependencies")

ingestion_service = IngestionService()

retrieval_service = RetrievalService()

app_logger.info("Service dependencies initialized")


# ====================================================
# DEPENDENCY PROVIDERS
# ====================================================

def get_ingestion_service() -> IngestionService:

    return ingestion_service


def get_retrieval_service() -> RetrievalService:

    return retrieval_service