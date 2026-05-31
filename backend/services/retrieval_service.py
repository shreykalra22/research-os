from typing import Dict

from backend.rag.retriever import Retriever
from backend.rag.prompt_builder import PromptBuilder

from backend.services.llm_service import LLMService
from backend.services.chat_db_service import ChatDBService

from backend.utils.config import settings
from backend.utils.logger import app_logger


class RetrievalService:

    def __init__(self):

        self.retriever = Retriever()

        self.prompt_builder = PromptBuilder()

        self.llm_service = LLMService()

        self.chat_db = ChatDBService()

    # ====================================================
    # NORMAL RESPONSE
    # ====================================================

    def generate_answer(
        self,
        query: str,
        session_id: str,
    ) -> Dict:

        app_logger.info(
            f"Starting retrieval pipeline for query: {query}"
        )

        # ==========================================
        # LOAD CHAT HISTORY FROM SQLITE
        # ==========================================

        history = self.chat_db.get_history(
            session_id
        )

        conversation_context = ""

        for msg in history[-10:]:

            conversation_context += (
                f"{msg['role']}: {msg['content']}\n"
            )

        # ==========================================
        # RETRIEVE DOCUMENTS
        # ==========================================

        retrieved_docs = self.retriever.retrieve(
            query=query,
            top_k=settings.TOP_K_RESULTS,
        )

        retrieved_contents = [
            doc["content"]
            for doc in retrieved_docs
        ]

        # ==========================================
        # BUILD PROMPT
        # ==========================================

        prompt = self.prompt_builder.build_prompt(
            query=query,
            retrieved_chunks=retrieved_contents,
            conversation_history=conversation_context,
        )

        # ==========================================
        # GENERATE ANSWER
        # ==========================================

        answer = self.llm_service.generate_response(
            prompt
        )

        # ==========================================
        # SAVE TO SQLITE
        # ==========================================

        self.chat_db.add_message(
            session_id,
            "user",
            query,
        )

        self.chat_db.add_message(
            session_id,
            "assistant",
            answer,
        )

        # ==========================================
        # SOURCES
        # ==========================================

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

        history = self.chat_db.get_history(
            session_id
        )

        conversation_context = ""

        for msg in history[-10:]:

            conversation_context += (
                f"{msg['role']}: {msg['content']}\n"
            )

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
            conversation_history=conversation_context,
        )

        return self.llm_service.stream_response(
            prompt
        )