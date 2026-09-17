from config.loader import get_enabled_providers


class ProviderFactory:

    @classmethod
    def create(cls, provider_name):
        provider_name = provider_name.lower()

        if provider_name == "openai":
            from providers.openai_provider import OpenAIProvider
            return OpenAIProvider()

        if provider_name == "gemini":
            from providers.gemini_provider import GeminiProvider
            return GeminiProvider()

        if provider_name == "groq":
            from providers.groq_provider import GroqProvider
            return GroqProvider()

        raise ValueError(
            f"Unsupported provider: {provider_name}"
        )