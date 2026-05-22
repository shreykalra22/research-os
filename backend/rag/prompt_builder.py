from typing import List


class PromptBuilder:
    def build_prompt(
        self,
        query: str,
        retrieved_chunks: List[str],
    ) -> str:

        context = "\n\n".join(retrieved_chunks)

        prompt = f"""
You are an AI Research Assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context,
say:
"I could not find relevant information in the documents."

================ CONTEXT ================

{context}

=========================================

USER QUESTION:
{query}

ANSWER:
"""

        return prompt