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

    task = input("\nWhat do you want me to do? ").strip()

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


if __name__ == "__main__":
    main()