from core.analyzer.project_context import ProjectContextBuilder


class Planner:
    ALLOWED_ACTIONS = {
        "understand",
        "inspect",
        "implement",
        "test",
        "report",
    }

    def __init__(self, router=None, root_path="."):
        self.router = router
        self.context_builder = ProjectContextBuilder(root_path)

    def create_plan(self, task):
        if not task or not task.strip():
            raise ValueError("Task cannot be empty")

        task = task.strip()

        if self.router is None:
            return self._fallback_plan(task)

        project_context = self.context_builder.build(task)

        prompt = f"""
You are the planning module of a software engineering AI agent.

Create a concise execution plan for this developer task.

TASK:
{task}

REAL PROJECT CONTEXT:
{project_context}

Rules:

- Use ONLY files and components that actually appear in the project context.
- Do NOT invent files, directories, frameworks, dependencies, or architecture.
- Do not write code.
- Create 3 to 8 steps.
- Every step MUST use exactly one action.
- Allowed actions are ONLY:
  understand
  inspect
  implement
  test
  report

Return ONLY lines in this exact format:

ACTION | DESCRIPTION

Example:

inspect | Inspect the relevant project files.
implement | Modify the existing authentication module.
test | Run the relevant tests.
report | Summarize the changes and test results.
"""

        try:
            response = self.router.smart_ask(prompt)
            return self._parse_plan(response)
        except Exception:
            return self._fallback_plan(task)

    def _parse_plan(self, response):
        steps = []

        for line in response.splitlines():
            line = line.strip()

            if not line or "|" not in line:
                continue

            action, description = line.split("|", 1)

            action = action.strip().lower()
            description = description.strip()

            if action not in self.ALLOWED_ACTIONS:
                continue

            if not description:
                continue

            steps.append({
                "step": len(steps) + 1,
                "action": action,
                "description": description,
            })

            if len(steps) >= 8:
                break

        if not steps:
            raise ValueError("AI returned an invalid plan")

        return steps

    def _fallback_plan(self, task):
        return [
            {
                "step": 1,
                "action": "inspect",
                "description": "Inspect the relevant project files.",
            },
            {
                "step": 2,
                "action": "implement",
                "description": f"Implement the required changes for: {task}",
            },
            {
                "step": 3,
                "action": "test",
                "description": "Run appropriate tests and verify the result.",
            },
            {
                "step": 4,
                "action": "report",
                "description": "Report the changes and test results.",
            },
        ]