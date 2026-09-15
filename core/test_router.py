from core.ai_router import AIRouter


class CodingProvider:

    def ask(self, prompt):
        return f"Coding provider handled: {prompt}"


class ReasoningProvider:

    def ask(self, prompt):
        return f"Reasoning provider handled: {prompt}"


router = AIRouter()

router.register_provider("coding", CodingProvider())
router.register_provider("reasoning", ReasoningProvider())

router.set_task_route(
    "coding",
    ["coding"]
)

router.set_task_route(
    "reasoning",
    ["reasoning"]
)

print(router.smart_ask("Implement a binary search algorithm"))
print(router.smart_ask("Explain why binary search is efficient"))