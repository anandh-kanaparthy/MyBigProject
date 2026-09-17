from core.implementer.code_implementer import CodeImplementer
from core.implementer.change_validator import ChangeValidator


class AgentExecutor:
    def __init__(self, planner, tool_registry, router):
        self.planner = planner
        self.tools = tool_registry
        self.router = router

        self.implementer = CodeImplementer(
            router,
            planner.context_builder,
        )

        self.change_validator = ChangeValidator(
            tool_registry.filesystem.root_path
        )

    def execute(self, task):
        plan = self.planner.create_plan(task)

        results = []
        execution_context = []

        for step in plan:
            action = step["action"]

            if action == "understand":
                result = step["description"]

                execution_context.append(
                    f"UNDERSTAND:\n{result}"
                )

                results.append({
                    "step": step["step"],
                    "action": action,
                    "status": "completed",
                    "result": result,
                })

            elif action == "inspect":
                files = self.tools.filesystem.list_files()

                file_list = [
                    str(
                        file.relative_to(
                            self.tools.filesystem.root_path
                        )
                    )
                    for file in files
                ]

                execution_context.append(
                    "INSPECTED FILES:\n"
                    + "\n".join(file_list)
                )

                results.append({
                    "step": step["step"],
                    "action": action,
                    "status": "completed",
                    "result": file_list,
                })

            elif action == "implement":
                try:
                    proposal = self.implementer.generate_change(
                        task,
                        step["description"],
                    )

                    proposal_text = (
                        f"FILE: {proposal['file']}\n\n"
                        f"CHANGE:\n{proposal['change']}\n\n"
                        f"CODE:\n{proposal['code']}"
                    )

                    self.change_validator.validate(
                        proposal_text
                    )

                    implementation_result = {
                        "file": proposal["file"],
                        "change": proposal["change"],
                        "code": proposal["code"],
                    }

                    execution_context.append(
                        "IMPLEMENTATION PROPOSAL:\n"
                        + str(implementation_result)
                    )

                    results.append({
                        "step": step["step"],
                        "action": action,
                        "status": "review_required",
                        "result": implementation_result,
                    })

                except Exception as error:
                    results.append({
                        "step": step["step"],
                        "action": action,
                        "status": "rejected",
                        "result": str(error),
                    })

            elif action == "test":
                test_result = self.tools.terminal.run(
                    "python -m core.test_router"
                )

                execution_context.append(
                    "TEST RESULT:\n"
                    + str(test_result)
                )

                results.append({
                    "step": step["step"],
                    "action": action,
                    "status": (
                        "completed"
                        if test_result["success"]
                        else "failed"
                    ),
                    "result": test_result,
                })

            elif action == "report":
                report = "\n\n".join(
                    execution_context
                )

                results.append({
                    "step": step["step"],
                    "action": action,
                    "status": "completed",
                    "result": report,
                })

            else:
                results.append({
                    "step": step["step"],
                    "action": action,
                    "status": "unsupported",
                    "result": (
                        f"Action '{action}' is not supported."
                    ),
                })

        return {
            "task": task,
            "plan": plan,
            "results": results,
            "execution_context": execution_context,
        }