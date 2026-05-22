from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    # =========================
    # APPLICATION
    # =========================

    APP_NAME: str = "ResearchOS"

    APP_VERSION: str = "2.0.0"

    API_V1_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    # =========================
    # SERVER
    # =========================

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # =========================
    # FILE UPLOADS
    # =========================

    UPLOAD_DIR: str = "data/uploads"

    MAX_UPLOAD_SIZE_MB: int = 20

    ALLOWED_FILE_TYPES: list[str] = [
        "application/pdf"
    ]

    # =========================
    # CHUNKING
    # =========================

    CHUNK_SIZE: int = 800

    CHUNK_OVERLAP: int = 100

    # =========================
    # EMBEDDINGS
    # =========================

    EMBEDDING_MODEL: str = "BAAI/bge-small-en"

    # =========================
    # VECTOR DATABASE
    # =========================

    CHROMA_DB_DIR: str = "chroma_db"

    COLLECTION_NAME: str = "research_documents"

    # =========================
    # OLLAMA / LLM
    # =========================

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    OLLAMA_MODEL: str = "mistral"

    # =========================
    # RETRIEVAL
    # =========================

    TOP_K_RESULTS: int = 3

    # =========================
    # LOGGING
    # =========================

    LOG_LEVEL: str = "INFO"

    # =========================
    # Pydantic Config
    # =========================

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }


settings = Settings()