from sse_starlette.sse import EventSourceResponse
import json

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


# ====================================================
# NORMAL CHAT
# ====================================================

@router.post("/")
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
            query=chat_request.query,
            session_id=chat_request.session_id,
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


# ====================================================
# STREAMING CHAT
# ====================================================

@router.post("/stream")
async def stream_chat(
    chat_request: ChatRequest,
    retrieval_service: RetrievalService = Depends(
        get_retrieval_service
    ),
):

    async def event_generator():

        try:

            app_logger.info(
                f"Streaming chat request: {chat_request.query}"
            )

            for token in retrieval_service.stream_answer(
                query=chat_request.query,
                session_id=chat_request.session_id,
            ):

                yield {
                    "event": "message",
                    "data": json.dumps(
                        {
                            "token": token
                        }
                    ),
                }

        except Exception as e:

            app_logger.error(
                f"Streaming failed: {str(e)}"
            )

            yield {
                "event": "error",
                "data": json.dumps(
                    {
                        "error": str(e)
                    }
                ),
            }

    return EventSourceResponse(
        event_generator()
    )