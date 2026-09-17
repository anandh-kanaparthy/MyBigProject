from core.analyzer.codebase_analyzer import CodebaseAnalyzer


class ProjectContextBuilder:
    MAX_CONTEXT_CHARS = 24000
    MAX_RELEVANT_FILES = 8

    def __init__(self, root_path):
        self.analyzer = CodebaseAnalyzer(root_path)

    def build(self, task=None):
        structure = self.analyzer.get_structure()

        sections = [
            "PROJECT STRUCTURE:",
            *structure,
            "",
            "RELEVANT SOURCE CODE:",
        ]

        if task:
            files = self.analyzer.find_relevant_files(
                task,
                max_files=self.MAX_RELEVANT_FILES,
            )
        else:
            files = self.analyzer.list_files()

        total_chars = len("\n".join(sections))

        for file_path in files:
            if (
                file_path.suffix.lower()
                not in self.analyzer.TEXT_EXTENSIONS
            ):
                continue

            try:
                content = self.analyzer.read_file(file_path)
            except ValueError:
                continue

            relative_path = file_path.relative_to(
                self.analyzer.root_path
            )

            file_section = (
                f"\n--- FILE: {relative_path} ---\n"
                f"{content}"
            )

            if total_chars + len(file_section) > self.MAX_CONTEXT_CHARS:
                continue

            sections.append(file_section)
            total_chars += len(file_section)

        return "\n".join(sections)