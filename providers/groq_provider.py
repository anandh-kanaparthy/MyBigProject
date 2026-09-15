from groq import Groq

from config.loader import get_api_key, get_model
from providers.base_provider import BaseProvider


class GroqProvider(BaseProvider):

    def __init__(self):
        self.api_key = get_api_key("groq")
        self.model = get_model("groq")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not configured")

        if not self.model:
            raise ValueError("GROQ_MODEL is not configured")

        self.client = Groq(api_key=self.api_key)

    def ask(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content