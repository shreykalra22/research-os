from backend.api.routes.upload import router as upload_router
from fastapi import FastAPI

from backend.api.routes.health import router as health_router

from backend.middleware.request_context import (
    RequestContextMiddleware,
)

from backend.utils.config import settings
from backend.utils.logger import app_logger


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# ====================================================
# MIDDLEWARE
# ====================================================

app.add_middleware(
    RequestContextMiddleware
)

# ====================================================
# ROUTERS
# ====================================================

app.include_router(
    health_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    upload_router,
    prefix=settings.API_V1_PREFIX,
)

# ====================================================
# ROOT ENDPOINT
# ====================================================

@app.get("/")
def root():

    return {
        "message": "ResearchOS API Running"
    }


app_logger.info("FastAPI application initialized")