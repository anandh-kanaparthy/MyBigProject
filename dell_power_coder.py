import os
from google import genai

class DynamicAIEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        self.client = genai.Client(api_key=self.api_key)

    def ask(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

if __name__ == "__main__":
    ai = DynamicAIEngine()
    answer = ai.ask("Hello! Introduce yourself in one short sentence.")
    print("\nAI:", answer)
