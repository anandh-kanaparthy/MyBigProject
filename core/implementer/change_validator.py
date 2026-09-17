from pathlib import Path
import ast


class ChangeValidator:
    FORBIDDEN_MARKERS = {
        "...",
        "rest of the file unchanged",
        "existing code unchanged",
        "same as above",
        "todo",
        "fixme",
    }

    PROTECTED_FILES = {
        ".env",
        "config.env",
    }

    MAX_CODE_SIZE = 500_000

    def __init__(self, root_path="."):
        self.root_path = Path(root_path).resolve()

    def validate(self, proposal):
        if not proposal or not proposal.strip():
            raise ValueError("Empty implementation proposal")

        target_file, change, code = self._parse_proposal(proposal)

        target_path = (self.root_path / target_file).resolve()

        try:
            target_path.relative_to(self.root_path)
        except ValueError:
            raise ValueError(
                "Target file is outside the project directory"
            )

        if target_path.name in self.PROTECTED_FILES:
            raise ValueError("Protected configuration file")

        if not code.strip():
            raise ValueError("Generated code cannot be empty")

        if len(code.encode("utf-8")) > self.MAX_CODE_SIZE:
            raise ValueError("Generated code is too large")

        self._validate_code_quality(target_file, code)

        return True

    def _parse_proposal(self, proposal):
        lines = proposal.splitlines()

        target_file = None
        change = None
        code_lines = []

        in_code = False

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("FILE:"):
                target_file = stripped[5:].strip()
                continue

            if stripped.startswith("CHANGE:"):
                change = stripped[7:].strip()
                continue

            if stripped.startswith("CODE:"):
                in_code = True
                remainder = line.split("CODE:", 1)[1]
                if remainder.strip():
                    code_lines.append(remainder.lstrip())
                continue

            if in_code:
                code_lines.append(line)

        if not target_file:
            raise ValueError("Proposal does not specify a target file")

        if not change:
            raise ValueError("Proposal does not specify a change")

        if not code_lines:
            raise ValueError("Proposal does not contain code")

        code = "\n".join(code_lines).strip()

        return target_file, change, code

    def _validate_code_quality(self, target_file, code):
        code_lower = code.lower()

        for marker in self.FORBIDDEN_MARKERS:
            if marker in code_lower:
                raise ValueError(
                    f"Invalid placeholder detected: {marker}"
                )

        suffix = Path(target_file).suffix.lower()

        if suffix == ".py":
            self._validate_python(code)

    def _validate_python(self, code):
        try:
            ast.parse(code)
        except SyntaxError as error:
            raise ValueError(
                f"Generated Python code has invalid syntax: {error}"
            )