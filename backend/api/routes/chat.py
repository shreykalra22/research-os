from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)

from backend.api.dependencies import (
    get_retrieval_service,
)

from backend.core.response import APIResponse

from backend.models.schemas import ChatRequest

from backend.services.retrieval_service import (
    RetrievalService,
)

from backend.utils.logger import app_logger


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("")
def chat(
    request: Request,
    chat_request: ChatRequest,
    retrieval_service: RetrievalService = Depends(
        get_retrieval_service
    ),
):

    app_logger.info(
        f"Received chat request: {chat_request.query}"
    )

    try:

        result = retrieval_service.generate_answer(
            chat_request.query
        )

    except Exception as e:

        app_logger.error(
            f"Chat pipeline failed: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}",
        )

    return APIResponse(
        success=True,
        message="Chat response generated successfully",
        request_id=request.state.request_id,
        data=result,
    )