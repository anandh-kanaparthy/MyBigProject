class ProposalParser:
    def parse(self, proposal):
        if not proposal or not proposal.strip():
            raise ValueError("Empty proposal")

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

            if stripped == "CODE:":
                section = "code"
                continue

            if section == "change":
                change_lines.append(line)

            elif section == "code":
                code_lines.append(line)

        if not target_file:
            raise ValueError("Proposal does not contain a target file")

        change = "\n".join(change_lines).strip()
        code = "\n".join(code_lines).strip()

        if not change:
            raise ValueError("Proposal does not contain a change description")

        if not code:
            raise ValueError("Proposal does not contain code")

        code = self._remove_code_fences(code)

        if not code.strip():
            raise ValueError("Code section is empty")

        return {
            "file": target_file,
            "change": change,
            "code": code,
        }

    def _remove_code_fences(self, code):
        lines = code.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        return "\n".join(lines).strip()