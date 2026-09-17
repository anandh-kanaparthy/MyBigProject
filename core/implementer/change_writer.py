from pathlib import Path
import shutil


class ChangeWriter:
    def __init__(self, root_path="."):
        self.root_path = Path(root_path).resolve()

    def write(self, target_file, content):
        target_path = (self.root_path / target_file).resolve()

        try:
            target_path.relative_to(self.root_path)
        except ValueError:
            raise ValueError(
                "Target file is outside the project directory"
            )

        if target_path.name in {".env", "config.env"}:
            raise ValueError("Protected configuration file")

        if not target_path.is_file():
            raise ValueError(
                f"Target file does not exist: {target_file}"
            )

        backup_path = target_path.with_suffix(
            target_path.suffix + ".backup"
        )

        shutil.copy2(target_path, backup_path)

        target_path.write_text(
            content,
            encoding="utf-8",
        )

        return {
            "success": True,
            "file": target_file,
            "backup": str(
                backup_path.relative_to(self.root_path)
            ),
        }