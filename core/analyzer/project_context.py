from core.analyzer.codebase_analyzer import CodebaseAnalyzer


class ProjectContextBuilder:

    def __init__(self, root_path):
        self.analyzer = CodebaseAnalyzer(root_path)

    def build(self):
        structure = self.analyzer.get_structure()

        sections = []

        sections.append("PROJECT STRUCTURE:")
        sections.extend(structure)

        sections.append("")
        sections.append("SOURCE CODE:")

        for file_path in self.analyzer.list_files():

            if file_path.suffix.lower() not in self.analyzer.TEXT_EXTENSIONS:
                continue

            try:
                content = self.analyzer.read_file(file_path)
            except ValueError:
                continue

            relative_path = file_path.relative_to(
                self.analyzer.root_path
            )

            sections.append("")
            sections.append(f"--- FILE: {relative_path} ---")
            sections.append(content)

        return "\n".join(sections)