from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = "ResearchOS"
    APP_VERSION: str = "1.0.0"

    API_V1_STR: str = "/api/v1"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"

    CHROMA_DB_DIR: str = "./chroma_db"

    EMBEDDING_MODEL: str = "BAAI/bge-small-en"

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100

    MAX_UPLOAD_SIZE_MB: int = 20

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()