from sympy import symbols, diff, integrate, sympify
import re

x = symbols('x')

def preprocess_expression(expr: str) -> str:
    """
    Convert user-friendly math into SymPy-friendly format.
    Examples:
    2x -> 2*x
    x^2 -> x**2
    sin x -> sin(x)
    """
    expr = expr.replace("^", "**")

    # Insert * between number and variable (2x -> 2*x)
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)

    # Insert * between variable and number (x2 -> x*2)
    expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)

    return expr

def solve_expression(expr, operation):
    try:
        expr = preprocess_expression(expr)
        sym_expr = sympify(expr)

        if operation == "differentiate":
            return diff(sym_expr, x)

        elif operation == "integrate":
            return integrate(sym_expr, x)

        return "Unsupported operation"

    except Exception as e:
        return f"⚠️ Invalid expression: {e}"