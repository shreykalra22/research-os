from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.utils.config import settings
from backend.utils.logger import app_logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    app_logger.info("Root endpoint accessed")

    return {
        "message": "ResearchOS Backend Running"
    }


@app.get("/health")
async def health_check():
    app_logger.info("Health check endpoint called")

    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }