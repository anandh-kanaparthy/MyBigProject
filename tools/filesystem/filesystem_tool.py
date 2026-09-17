from pathlib import Path


class FilesystemTool:
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

    def _validate_path(self, file_path):
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

        return path

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

    def read_file(self, file_path):
        path = self._validate_path(file_path)

        if not path.is_file():
            raise ValueError("File does not exist")

        if path.suffix.lower() not in self.TEXT_EXTENSIONS:
            raise ValueError("Unsupported text file type")

        if path.stat().st_size > self.MAX_FILE_SIZE:
            raise ValueError("File is too large to read")

        return path.read_text(
            encoding="utf-8",
            errors="replace",
        )

    def write_file(self, file_path, content):
        path = self._validate_path(file_path)

        if path.suffix.lower() not in self.TEXT_EXTENSIONS:
            raise ValueError("Unsupported text file type")

        if len(content.encode("utf-8")) > self.MAX_FILE_SIZE:
            raise ValueError("Content is too large")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            content,
            encoding="utf-8",
        )

        return f"File written successfully: {path.relative_to(self.root_path)}"

    def file_exists(self, file_path):
        path = self._validate_path(file_path)
        return path.is_file()