from core.task_classifier import TaskClassifier
from providers.provider_factory import ProviderFactory
from config.loader import get_enabled_providers


class AIRouter:

    def __init__(self):
        self.providers = {}
        self.task_classifier = TaskClassifier()
        self.task_routes = {}

        self.load_configured_providers()
        self.configure_default_routes()

    def load_configured_providers(self):
        for provider_name in get_enabled_providers():
            try:
                provider = ProviderFactory.create(provider_name)
                self.register_provider(provider_name, provider)

            except Exception as error:
                print(
                    f"Warning: Could not initialize provider "
                    f"'{provider_name}': {error}"
                )

    def register_provider(self, name, provider):
        self.providers[name] = provider

    def configure_default_routes(self):
        available = list(self.providers.keys())

        if not available:
            return

        self.task_routes = {
            "coding": available,
            "debugging": available,
            "analysis": available,
            "reasoning": available,
            "fast": available,
        }

    def set_task_route(self, task_type, provider_names):
        self.task_routes[task_type] = provider_names

    def get_provider(self, name):
        if name not in self.providers:
            raise ValueError(
                f"Provider '{name}' is not registered"
            )

        return self.providers[name]

    def ask(self, provider_name, prompt):
        provider = self.get_provider(provider_name)
        return provider.ask(prompt)

    def ask_with_fallback(self, provider_names, prompt):
        errors = []

        for name in provider_names:
            try:
                provider = self.get_provider(name)
                return provider.ask(prompt)

            except Exception as error:
                errors.append(f"{name}: {error}")

        raise RuntimeError(
            "All providers failed:\n" + "\n".join(errors)
        )

    def smart_ask(self, prompt):
        task_type = self.task_classifier.classify(prompt)

        providers = self.task_routes.get(task_type)

        if not providers:
            raise ValueError(
                f"No provider route configured for task type: {task_type}"
            )

        return self.ask_with_fallback(providers, prompt)