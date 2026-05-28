from typing import List

from backend.utils.logger import app_logger


class PromptBuilder:

    # ====================================================
    # BUILD RAG PROMPT
    # ====================================================

    def build_prompt(
        self,
        query: str,
        retrieved_chunks: List[str],
        conversation_history: str = "",
    ) -> str:

        app_logger.info(
            "Building RAG prompt"
        )

        # ==========================================
        # COMBINE RETRIEVED CONTEXT
        # ==========================================

        context = "\n\n".join(
            retrieved_chunks
        )

        # ==========================================
        # BUILD FINAL PROMPT
        # ==========================================

        prompt = f"""
You are ResearchOS, a professional AI research assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context,
say:
"I could not find the answer in the provided documents."

Be concise, accurate, and professional.
IMPORTANT:
- Format answers using markdown.
- Use bullet points whenever possible.
- Use headings for sections.
- Keep spacing clean and readable.
- Do not write huge paragraphs.
==============================
CONVERSATION HISTORY
==============================

{conversation_history}

==============================
RETRIEVED CONTEXT
==============================

{context}

==============================
CURRENT QUESTION
==============================

{query}

==============================
ANSWER
==============================
"""

        app_logger.info(
            "Prompt built successfully"
        )

        return prompt