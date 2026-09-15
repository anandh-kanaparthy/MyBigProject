from providers.openai_provider import OpenAIProvider
from providers.gemini_provider import GeminiProvider
from providers.groq_provider import GroqProvider


class ProviderFactory:

    PROVIDER_CLASSES = {
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
        "groq": GroqProvider,
    }

    @classmethod
    def create(cls, provider_name):
        provider_name = provider_name.lower()

        if provider_name not in cls.PROVIDER_CLASSES:
            raise ValueError(
                f"Unsupported provider: {provider_name}"
            )

        provider_class = cls.PROVIDER_CLASSES[provider_name]

        return provider_class()