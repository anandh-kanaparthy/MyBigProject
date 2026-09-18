from core.ai_router import AIRouter
from core.planner.planner import Planner
from core.tool_registry import ToolRegistry
from core.executor.agent_executor import AgentExecutor


def main():
    root_path = "."

    router = AIRouter()
    tools = ToolRegistry(root_path)
    planner = Planner(router, root_path)
    executor = AgentExecutor(planner, tools, router)

    task = input(
        "\nWhat do you want me to do? "
    ).strip()

    if not task:
        print("No task provided.")
        return

    result = executor.execute(task)

    print("\n=== PLAN ===")

    for step in result["plan"]:
        print(
            f'{step["step"]}. '
            f'{step["description"]}'
        )

    print("\n=== RESULTS ===")

    for item in result["results"]:
        print(
            f'\nStep {item["step"]}: '
            f'{item["action"]} '
            f'[{item["status"]}]'
        )

        print(item["result"])

        if (
            item["action"] == "implement"
            and item["status"] == "review_required"
        ):
            proposal = item["result"]

            print("\n=== IMPLEMENTATION PROPOSAL ===")
            print(f'File: {proposal["file"]}')
            print(f'Change: {proposal["change"]}')
            print("\nCode:")
            print(proposal["code"])

            approval = input(
                "\nApply this change? [yes/no]: "
            ).strip().lower()

            if approval in {"yes", "y"}:
                try:
                    applied = executor.apply_approved_change(
                        proposal
                    )

                    print("\n=== CHANGE APPLIED ===")
                    print(applied)

                except Exception as error:
                    print(
                        "\n=== CHANGE REJECTED ==="
                    )
                    print(error)

            else:
                print(
                    "\nChange not applied."
                )


if __name__ == "__main__":
    main()