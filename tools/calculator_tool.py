"""
Calculator Tool
Provides mathematical calculation capabilities
"""

from langchain_core.tools import Tool
import re


def calculate(expression: str) -> str:
    """
    Evaluate mathematical expressions safely

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        Calculation result or error message
    """
    try:
        # Remove any non-mathematical characters for safety
        expression = expression.strip()

        # Allow only numbers, operators, parentheses, and basic math functions
        allowed_chars = set('0123456789+-*/().^ ')
        if not all(c in allowed_chars or c.isspace() for c in expression):
            # Check for basic math functions
            if not re.match(r'^[\d\s\+\-\*/\(\)\.\^]+$', expression.replace('**', '^')):
                return "Invalid expression. Only basic mathematical operations are allowed."

        # Replace ^ with ** for Python evaluation
        expression = expression.replace('^', '**')

        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}}, {})

        return f"Result: {result}"

    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return "Error: Invalid mathematical expression"
    except Exception as e:
        return f"Calculation error: {str(e)}"


def create_calculator_tool() -> Tool:
    """Create and return the calculator tool"""
    return Tool(
        name="Calculator",
        func=calculate,
        description=(
            "Useful for performing mathematical calculations. "
            "Can handle basic arithmetic operations: addition (+), subtraction (-), "
            "multiplication (*), division (/), and exponentiation (**). "
            "Input should be a mathematical expression. "
            "Examples: '18*25+99', '(100+50)/2', '2**8'"
        )
    )
