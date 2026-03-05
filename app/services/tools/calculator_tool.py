import ast
import operator

from app.services.tools.base_tool import BaseTool
from app.services.tools.tool_registry import tool_registry


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs basic arithmetic operations."

    def run(self, input_data: str):
        """
        Safely evaluate arithmetic expressions.
        Allowed operators: +, -, *, /, %, ()
        """

        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
        }

        def eval_node(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                return allowed_operators[type(node.op)](
                    eval_node(node.left),
                    eval_node(node.right),
                )
            elif isinstance(node, ast.UnaryOp):
                return allowed_operators[type(node.op)](
                    eval_node(node.operand)
                )
            else:
                raise ValueError("Invalid expression")

        parsed = ast.parse(input_data, mode="eval")
        result = eval_node(parsed.body)
        return result


# Register tool
calculator_tool = CalculatorTool()
tool_registry.register_tool(calculator_tool.name, calculator_tool)