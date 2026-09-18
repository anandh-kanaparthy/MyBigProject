from pathlib import Path
import shutil


class ChangeWriter:
    PROTECTED_FILES = {
        ".env",
        "config.env",
    }

    MAX_CODE_SIZE = 500_000

    def __init__(self, root_path="."):
        self.root_path = Path(root_path).resolve()

    def write(self, target_file, content):
        if not target_file or not target_file.strip():
            raise ValueError("Target file cannot be empty")

        if not content or not content.strip():
            raise ValueError("File content cannot be empty")

        target_file = target_file.strip()
        content = content.strip()

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

        if len(content.encode("utf-8")) > self.MAX_CODE_SIZE:
            raise ValueError(
                "Generated code is too large"
            )

        target_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup_path = None

        if target_path.is_file():
            backup_path = target_path.with_suffix(
                target_path.suffix + ".backup"
            )

            shutil.copy2(
                target_path,
                backup_path,
            )

        target_path.write_text(
            content + "\n",
            encoding="utf-8",
        )

        result = {
            "success": True,
            "file": target_file,
            "created": backup_path is None,
        }

        if backup_path is not None:
            result["backup"] = str(
                backup_path.relative_to(
                    self.root_path
                )
            )

        return result