from typing import Callable, Dict

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, function: Callable):
        self.tools[name] = function

    def get_tool(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())


# Global registry instance
tool_registry = ToolRegistry()


from app.services.tools import calculator_tool