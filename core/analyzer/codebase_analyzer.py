from pathlib import Path
import re


class CodebaseAnalyzer:
    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode",
    }

    IGNORED_FILES = {
        ".env",
        "config.env",
    }

    TEXT_EXTENSIONS = {
        ".py",
        ".java",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".json",
        ".yaml",
        ".yml",
        ".md",
        ".txt",
        ".html",
        ".css",
        ".sql",
        ".xml",
        ".properties",
    }

    MAX_FILE_SIZE = 500_000

    def __init__(self, root_path):
        self.root_path = Path(root_path).resolve()

        if not self.root_path.exists():
            raise ValueError(f"Path does not exist: {self.root_path}")

        if not self.root_path.is_dir():
            raise ValueError(f"Path is not a directory: {self.root_path}")

    def list_files(self):
        files = []

        for path in self.root_path.rglob("*"):
            if not path.is_file():
                continue

            if any(
                ignored in path.parts
                for ignored in self.IGNORED_DIRECTORIES
            ):
                continue

            if path.name in self.IGNORED_FILES:
                continue

            files.append(path)

        return sorted(files)

    def get_file_count(self):
        return len(self.list_files())

    def get_structure(self):
        return [
            str(path.relative_to(self.root_path))
            for path in self.list_files()
        ]

    def read_file(self, file_path):
        path = Path(file_path).resolve()

        try:
            path.relative_to(self.root_path)
        except ValueError:
            raise ValueError("File is outside the project directory")

        if path.name in self.IGNORED_FILES:
            raise ValueError("Access to this file is blocked")

        if any(
            ignored in path.parts
            for ignored in self.IGNORED_DIRECTORIES
        ):
            raise ValueError("Access to this directory is blocked")

        if not path.is_file():
            raise ValueError("File does not exist")

        if path.suffix.lower() not in self.TEXT_EXTENSIONS:
            raise ValueError("Unsupported text file type")

        if path.stat().st_size > self.MAX_FILE_SIZE:
            raise ValueError("File is too large to read")

        return path.read_text(
            encoding="utf-8",
            errors="replace"
        )

    def find_relevant_files(self, task, max_files=8):
        if not task or not task.strip():
            return []

        task_words = self._extract_keywords(task)

        scored_files = []

        for path in self.list_files():
            if path.suffix.lower() not in self.TEXT_EXTENSIONS:
                continue

            relative_path = str(
                path.relative_to(self.root_path)
            ).lower()

            try:
                content = self.read_file(path)
            except ValueError:
                continue

            searchable_text = (
                relative_path
                + " "
                + content.lower()
            )

            score = 0

            for word in task_words:
                if word in relative_path:
                    score += 5

                score += searchable_text.count(word)

            if path.name.lower() in {
                "readme.md",
                "pyproject.toml",
                "requirements.txt",
            }:
                score += 1

            if score > 0:
                scored_files.append(
                    (score, path)
                )

        scored_files.sort(
            key=lambda item: (-item[0], str(item[1]))
        )

        return [
            path
            for _, path in scored_files[:max_files]
        ]

    def _extract_keywords(self, text):
        words = re.findall(
            r"[a-zA-Z_][a-zA-Z0-9_]*",
            text.lower()
        )

        stop_words = {
            "the",
            "this",
            "that",
            "with",
            "from",
            "into",
            "for",
            "and",
            "or",
            "to",
            "of",
            "a",
            "an",
            "is",
            "are",
            "be",
            "it",
            "in",
            "on",
            "my",
            "project",
        }

        return {
            word
            for word in words
            if len(word) >= 3
            and word not in stop_words
        }