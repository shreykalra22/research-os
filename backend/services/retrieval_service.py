from typing import Dict

from backend.rag.retriever import Retriever
from backend.rag.prompt_builder import PromptBuilder

from backend.services.llm_service import LLMService

from backend.utils.config import settings
from backend.utils.logger import app_logger


class RetrievalService:

    def __init__(self):

        self.retriever = Retriever()

        self.prompt_builder = PromptBuilder()

        self.llm_service = LLMService()

    # ====================================================
    # NORMAL RESPONSE
    # ====================================================

    def generate_answer(
        self,
        query: str,
        session_id: str,
    ) -> Dict:

        retrieved_docs = self.retriever.retrieve(
            query=query,
            top_k=settings.TOP_K_RESULTS,
        )

        retrieved_contents = [
            doc["content"]
            for doc in retrieved_docs
        ]

        prompt = self.prompt_builder.build_prompt(
            query=query,
            retrieved_chunks=retrieved_contents,
            conversation_history="",
        )

        answer = self.llm_service.generate_response(
            prompt
        )

        sources = []

        for doc in retrieved_docs:

            sources.append(
                {
                    "page_number": doc["page_number"],
                    "source": doc["source"],
                }
            )

        return {
            "query": query,
            "answer": answer,
            "sources": sources,
            "session_id": session_id,
        }

    # ====================================================
    # STREAMING RESPONSE
    # ====================================================

    def stream_answer(
        self,
        query: str,
        session_id: str,
    ):

        retrieved_docs = self.retriever.retrieve(
            query=query,
            top_k=settings.TOP_K_RESULTS,
        )

        retrieved_contents = [
            doc["content"]
            for doc in retrieved_docs
        ]

        prompt = self.prompt_builder.build_prompt(
            query=query,
            retrieved_chunks=retrieved_contents,
            conversation_history="",
        )

        return self.llm_service.stream_response(
            prompt
        )