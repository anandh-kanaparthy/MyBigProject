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
        if not proposal:
            raise ValueError(
                "Empty implementation proposal"
            )

        if isinstance(proposal, dict):
            target_file = proposal.get("file")
            change = proposal.get("change")
            code = proposal.get("code")

        elif isinstance(proposal, str):
            target_file, change, code = self._parse_proposal(
                proposal
            )

        else:
            raise ValueError(
                "Unsupported implementation proposal type"
            )

        if not target_file or not target_file.strip():
            raise ValueError(
                "Proposal does not specify a target file"
            )

        if not change or not change.strip():
            raise ValueError(
                "Proposal does not specify a change"
            )

        if not code or not code.strip():
            raise ValueError(
                "Proposal does not contain code"
            )

        target_file = target_file.strip()
        code = code.strip()

        target_path = (
            self.root_path / target_file
        ).resolve()

        try:
            target_path.relative_to(
                self.root_path
            )
        except ValueError:
            raise ValueError(
                "Target file is outside the project directory"
            )

        if target_path.name in self.PROTECTED_FILES:
            raise ValueError(
                "Protected configuration file"
            )

        if len(code.encode("utf-8")) > self.MAX_CODE_SIZE:
            raise ValueError(
                "Generated code is too large"
            )

        self._validate_code_quality(
            target_file,
            code,
        )

        return True

    def _parse_proposal(self, proposal):
        lines = proposal.splitlines()

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
                change_lines.append(
                    stripped[7:].strip()
                )
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
            raise ValueError(
                "Proposal does not specify a target file"
            )

        change = "\n".join(
            change_lines
        ).strip()

        if not change:
            raise ValueError(
                "Proposal does not specify a change"
            )

        if not code_lines:
            raise ValueError(
                "Proposal does not contain code"
            )

        code = "\n".join(
            code_lines
        ).strip()

        return target_file, change, code

    def _validate_code_quality(
        self,
        target_file,
        code,
    ):
        code_lower = code.lower()

        for marker in self.FORBIDDEN_MARKERS:
            if marker in code_lower:
                raise ValueError(
                    f"Invalid placeholder detected: {marker}"
                )

        suffix = Path(
            target_file
        ).suffix.lower()

        if suffix == ".py":
            self._validate_python(code)

    def _validate_python(self, code):
        try:
            ast.parse(code)
        except SyntaxError as error:
            raise ValueError(
                "Generated Python code has invalid syntax: "
                f"{error}"
            )