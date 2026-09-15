from openai import OpenAI
from config.loader import get_api_key, get_model
from providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):

    def __init__(self):
        self.api_key = get_api_key("openai")
        self.model = get_model("openai")

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured")

        if not self.model:
            raise ValueError("OPENAI_MODEL is not configured")

        self.client = OpenAI(api_key=self.api_key)

    def ask(self, prompt):
        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text