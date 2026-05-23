from typing import Dict

from backend.services.memory_service import MemoryService

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

        self.memory_service = MemoryService()

    # ====================================================
    # MAIN AI PIPELINE
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
        # LOAD CONVERSATION MEMORY
        # ==========================================

        history = self.memory_service.get_history(
            session_id
        )

        conversation_context = ""

        for msg in history[-6:]:

            conversation_context += (
                f"{msg['role']}: {msg['content']}\n"
            )

        # ==========================================
        # RETRIEVE RELEVANT DOCUMENTS
        # ==========================================

        retrieved_docs = self.retriever.retrieve(
            query=query,
            top_k=settings.TOP_K_RESULTS,
        )

        app_logger.info(
            f"Retrieved {len(retrieved_docs)} documents"
        )

        # ==========================================
        # BUILD CONTEXT
        # ==========================================

        retrieved_contents = [
            doc["content"]
            for doc in retrieved_docs
        ]

        prompt = self.prompt_builder.build_prompt(
            query=query,
            retrieved_chunks=retrieved_contents,
            conversation_history=conversation_context,
        )

        app_logger.info(
            "Prompt constructed successfully"
        )

        # ==========================================
        # QUERY LLM
        # ==========================================

        answer = self.llm_service.generate_response(
            prompt
        )

        app_logger.info(
            "LLM response generated successfully"
        )

        # ==========================================
        # STORE MEMORY
        # ==========================================

        self.memory_service.add_message(
            session_id,
            "user",
            query,
        )

        self.memory_service.add_message(
            session_id,
            "assistant",
            answer,
        )

        # ==========================================
        # FORMAT SOURCES
        # ==========================================

        sources = []

        for doc in retrieved_docs:

            sources.append(
                {
                    "page_number": doc["page_number"],
                    "source": doc["source"],
                }
            )

        # ==========================================
        # RETURN STRUCTURED RESPONSE
        # ==========================================

        return {
            "query": query,
            "answer": answer,
            "sources": sources,
            "session_id": session_id,
        }