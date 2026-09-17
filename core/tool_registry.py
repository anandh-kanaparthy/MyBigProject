from tools.filesystem.filesystem_tool import FilesystemTool
from tools.terminal.terminal_tool import TerminalTool


class ToolRegistry:
    def __init__(self, root_path):
        self.root_path = root_path

        self.filesystem = FilesystemTool(root_path)
        self.terminal = TerminalTool(root_path)

        self.tools = {
            "filesystem": self.filesystem,
            "terminal": self.terminal,
        }

    def get_tool(self, name):
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        return self.tools[name]

    def list_tools(self):
        return list(self.tools.keys())