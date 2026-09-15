from google import genai

from config.loader import get_api_key, get_model
from providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):

    def __init__(self):
        self.api_key = get_api_key("gemini")
        self.model = get_model("gemini")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        if not self.model:
            raise ValueError("GEMINI_MODEL is not configured")

        self.client = genai.Client(api_key=self.api_key)

    def ask(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "automatic_function_calling": {
                    "disable": True
                }
            }
        )

        return response.text