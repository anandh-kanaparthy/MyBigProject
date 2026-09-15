import re


class TaskClassifier:

    TASK_TYPES = {
        "reasoning",
        "coding",
        "debugging",
        "analysis",
        "fast",
    }

    def _contains(self, text, words):
        return any(
            re.search(rf"\b{re.escape(word)}\b", text)
            for word in words
        )

    def classify(self, prompt):
        text = prompt.lower()

        if self._contains(text, [
            "debug",
            "debugging",
            "bug",
            "error",
            "exception",
            "traceback",
            "crash",
            "broken",
            "fix this",
            "fix the",
        ]):
            return "debugging"

        if self._contains(text, [
            "implement",
            "write code",
            "create code",
            "function",
            "class",
            "algorithm",
            "program",
            "coding",
        ]):
            return "coding"

        if self._contains(text, [
            "analyze",
            "analyse",
            "review",
            "architecture",
            "codebase",
            "repository",
            "project structure",
            "find improvements",
        ]):
            return "analysis"

        if self._contains(text, [
            "explain",
            "why",
            "compare",
            "reason",
            "design",
            "how does",
        ]):
            return "reasoning"

        return "fast"