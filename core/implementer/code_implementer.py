import json
import re


class CodeImplementer:
    def __init__(self, router, context_builder):
        self.router = router
        self.context_builder = context_builder

    def generate_change(self, task, implementation_step):
        if not task or not task.strip():
            raise ValueError("Task cannot be empty")

        if not implementation_step or not implementation_step.strip():
            raise ValueError("Implementation step cannot be empty")

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

        return self._parse_response(response)

    def _parse_response(self, response):
        if not response or not response.strip():
            raise ValueError(
                "AI returned an empty implementation proposal"
            )

        text = response.strip()

        proposal = self._parse_json(text)

        if proposal is None:
            proposal = self._parse_markdown(text)

        if proposal is None:
            raise ValueError(
                "AI returned an unsupported implementation format"
            )

        self._validate_proposal(proposal)

        return proposal

    def _parse_json(self, text):
        candidates = [text]

        if text.startswith("```"):
            lines = text.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            candidates.append("\n".join(lines).strip())

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end > start:
            candidates.append(text[start:end + 1])

        for candidate in candidates:
            try:
                value = json.loads(candidate)

                if isinstance(value, dict):
                    return value

            except json.JSONDecodeError:
                continue

        return None

    def _parse_markdown(self, text):
        file_patterns = [
            r"\*\*(?:New File|Added File|File):\*\*\s*`([^`]+)`",
            r"(?:New File|Added File|File):\s*`([^`]+)`",
            r"(?:New File|Added File|File):\s*([^\s`]+)",
        ]

        target_file = None

        for pattern in file_patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                target_file = match.group(1).strip()
                break

        code_blocks = re.findall(
            r"```(?:python|py)?\s*\n(.*?)```",
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not code_blocks:
            return None

        code = code_blocks[0].strip()

        if target_file is None:
            target_file = self._infer_file_from_text(text)

        if target_file is None:
            return None

        return {
            "file": target_file,
            "change": "Implement the requested change.",
            "code": code,
        }

    def _infer_file_from_text(self, text):
        match = re.search(
            r"`((?:core|agent|providers|tools|config|workspace)/[^`]+\.py)`",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return None

    def _validate_proposal(self, proposal):
        if not isinstance(proposal, dict):
            raise ValueError(
                "Implementation proposal must be a JSON object"
            )

        required_fields = {
            "file",
            "change",
            "code",
        }

        missing = required_fields - proposal.keys()

        if missing:
            raise ValueError(
                "Implementation proposal missing fields: "
                + ", ".join(sorted(missing))
            )

        for field in required_fields:
            if not isinstance(proposal[field], str):
                raise ValueError(
                    f"Implementation field '{field}' must be a string"
                )

            if not proposal[field].strip():
                raise ValueError(
                    f"Implementation field '{field}' cannot be empty"
                )

        if "..." in proposal["code"]:
            raise ValueError(
                "Incomplete code detected in implementation proposal"
            )