import requests

from backend.utils.config import settings
from backend.utils.logger import app_logger


class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    def generate_response(
        self,
        prompt: str,
    ) -> str:

        app_logger.info("Sending request to Ollama")

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
        )

        result = response.json()

        app_logger.info("LLM response generated")

        return result["response"]