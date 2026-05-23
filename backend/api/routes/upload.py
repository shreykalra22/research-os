from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)

from backend.api.dependencies import (
    get_ingestion_service,
)

from backend.core.response import APIResponse

from backend.services.ingestion_service import (
    IngestionService,
)

from backend.utils.config import settings
from backend.utils.logger import app_logger


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("")
async def upload_pdf(
    request: Request,
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(
        get_ingestion_service
    ),
):

    app_logger.info(
        f"Received upload request: {file.filename}"
    )

    # ==========================================
    # VALIDATE FILE TYPE
    # ==========================================

    if file.content_type not in settings.ALLOWED_FILE_TYPES:

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    # ==========================================
    # CREATE UPLOAD DIRECTORY
    # ==========================================

    upload_dir = Path(settings.UPLOAD_DIR)

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ==========================================
    # SAVE FILE
    # ==========================================

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    app_logger.info(
        f"File saved successfully: {file_path}"
    )

    # ==========================================
    # RUN INGESTION PIPELINE
    # ==========================================

    try:

        result = ingestion_service.ingest_document(
            str(file_path)
        )

    except Exception as e:

        app_logger.error(
            f"Ingestion failed: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}",
        )

    # ==========================================
    # RETURN RESPONSE
    # ==========================================

    return APIResponse(
        success=True,
        message="PDF uploaded and processed successfully",
        request_id=request.state.request_id,
        data=result,
    )