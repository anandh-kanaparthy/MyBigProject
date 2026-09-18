import ast
import json
import re


class ProposalParser:
    def parse(self, proposal):
        if not proposal or not proposal.strip():
            raise ValueError("Empty proposal")

        text = proposal.strip()

        parsed = self._parse_json(text)

        if parsed is None:
            parsed = self._parse_structured(text)

        if parsed is None:
            parsed = self._parse_markdown(text)

        if parsed is None:
            raise ValueError(
                "Unsupported implementation proposal format"
            )

        self._validate(parsed)

        return parsed

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
                    if all(
                        field in value
                        for field in ("file", "change", "code")
                    ):
                        return value

            except json.JSONDecodeError:
                continue

        return None

    def _parse_structured(self, text):
        lines = text.splitlines()

        target_file = None
        change_lines = []
        code_lines = []

        section = None

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("FILE:"):
                target_file = stripped[5:].strip()
                section = None
                continue

            if stripped == "CHANGE:":
                section = "change"
                continue

            if stripped.startswith("CHANGE:"):
                change_lines.append(stripped[7:].strip())
                section = "change"
                continue

            if stripped == "CODE:":
                section = "code"
                continue

            if section == "change":
                change_lines.append(line)

            elif section == "code":
                code_lines.append(line)

        if not target_file:
            return None

        change = "\n".join(change_lines).strip()
        code = "\n".join(code_lines).strip()

        if not change or not code:
            return None

        return {
            "file": target_file,
            "change": change,
            "code": self._remove_code_fences(code),
        }

    def _parse_markdown(self, text):
        patterns = [
            r"\*\*(?:Added file|New file|File):\*\*\s*`([^`]+)`",
            r"(?:Added file|New file|File):\s*`([^`]+)`",
            r"\*\*`([^`]+\.py)`\*\*",
            r"`((?:core|agent|providers|tools|config|workspace)/[^`]+\.py)`",
        ]

        target_file = None

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                target_file = match.group(1).strip()
                break

        if target_file is None:
            return None

        code_blocks = re.findall(
            r"```(?:python|py)?\s*\n(.*?)```",
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not code_blocks:
            return None

        code = code_blocks[0].strip()

        return {
            "file": target_file,
            "change": "Implement the requested change.",
            "code": code,
        }

    def _remove_code_fences(self, code):
        lines = code.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        return "\n".join(lines).strip()

    def _validate(self, proposal):
        required_fields = {
            "file",
            "change",
            "code",
        }

        missing = required_fields - proposal.keys()

        if missing:
            raise ValueError(
                "Proposal missing fields: "
                + ", ".join(sorted(missing))
            )

        for field in required_fields:
            if not isinstance(proposal[field], str):
                raise ValueError(
                    f"Proposal field '{field}' must be a string"
                )

            if not proposal[field].strip():
                raise ValueError(
                    f"Proposal field '{field}' cannot be empty"
                )

        code = proposal["code"]

        if "```" in code:
            raise ValueError(
                "Markdown code fence detected inside generated code"
            )

        if "..." in code:
            raise ValueError(
                "Incomplete code detected"
            )

        if proposal["file"].lower().endswith(".py"):
            try:
                ast.parse(code)
            except SyntaxError as error:
                raise ValueError(
                    "Generated Python code has invalid syntax: "
                    f"{error}"
                )