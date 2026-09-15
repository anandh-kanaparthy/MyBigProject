from core.analyzer.project_context import ProjectContextBuilder


class CodingAgent:

    def __init__(self, root_path, router):
        self.root_path = root_path
        self.router = router
        self.context_builder = ProjectContextBuilder(root_path)

    def build_prompt(self, task):
        project_context = self.context_builder.build()

        return f"""
You are an advanced software engineering AI agent.

You are working on the following software project.

PROJECT CONTEXT:
{project_context}

USER TASK:
{task}

Instructions:
1. Understand the project before answering.
2. Identify relevant files and existing architecture.
3. Do not invent files, functions, or dependencies.
4. For coding tasks, provide precise implementation guidance.
5. Consider correctness, security, performance, and maintainability.
6. If information is missing, clearly state what is missing.
7. Do not expose secrets or environment variables.
"""

    def ask(self, task):
        task_type = self.router.task_classifier.classify(task)

        providers = self.router.task_routes.get(task_type)

        if not providers:
            raise ValueError(
                f"No provider route configured for task type: {task_type}"
            )

        prompt = self.build_prompt(task)

        return self.router.ask_with_fallback(providers, prompt)