from core.implementer.proposal_parser import ProposalParser


class CodeImplementer:
    def __init__(self, router, context_builder):
        self.router = router
        self.context_builder = context_builder
        self.proposal_parser = ProposalParser()

    def generate_change(self, task, implementation_step):
        if not task or not task.strip():
            raise ValueError("Task cannot be empty")

        if not implementation_step or not implementation_step.strip():
            raise ValueError(
                "Implementation step cannot be empty"
            )

        project_context = self.context_builder.build(
            f"{task}\n{implementation_step}"
        )

        prompt = f"""
You are the implementation module of a software engineering AI agent.

USER TASK:
{task}

IMPLEMENTATION STEP:
{implementation_step}

RELEVANT PROJECT CONTEXT:
{project_context}

Return exactly ONE JSON object.

Required fields:

- file
- change
- code

Rules:

- file must be a relative project path.
- code must contain COMPLETE file content.
- Do not use Markdown.
- Do not use code fences.
- Do not add explanations outside the JSON object.
- Do not use placeholders such as "...".
- Do not expose secrets.
- Preserve unrelated existing functionality.

Required format:

{{
    "file": "relative/path/to/file.py",
    "change": "Description of the change",
    "code": "Complete file content"
}}
"""

        response = self.router.smart_ask(prompt)

        print("\n=== RAW IMPLEMENTATION RESPONSE ===")
        print(response)
        print("=== END RAW RESPONSE ===")

        return self.proposal_parser.parse(response)