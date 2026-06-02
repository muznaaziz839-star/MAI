from sympy import symbols, diff, integrate, sympify
import re

# =========================================================
# SYMBOLS (EXTENSIBLE)
# =========================================================
x = symbols('x')


# =========================================================
# PREPROCESSING
# =========================================================
def preprocess_expression(expr: str) -> str:
    """
    Convert user-friendly math into SymPy-friendly format.
    """

    expr = expr.lower().strip()

    # Replace power symbol
    expr = expr.replace("^", "**")

    # Insert multiplication: 2x -> 2*x
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)

    # Insert multiplication: x2 -> x*2
    expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)

    # Handle cases like: 2(x+1) -> 2*(x+1)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)

    # Handle cases like: )( -> )*(
    expr = expr.replace(")(", ")*(")

    return expr


# =========================================================
# CORE SOLVER
# =========================================================
def solve_expression(expr, operation):
    """
    Perform symbolic calculus operations.
    Returns structured result (not just raw output).
    """

    try:
        # Clean expression
        expr = preprocess_expression(expr)

        # Convert to symbolic form
        sym_expr = sympify(expr)

        # ================= DIFFERENTIATION =================
        if operation == "differentiate":

            result = diff(sym_expr, x)

            return {
                "operation": "derivative",
                "input": str(sym_expr),
                "result": str(result),
                "explanation": f"The derivative of {sym_expr} with respect to x is {result}"
            }

        # ================= INTEGRATION =================
        elif operation == "integrate":

            result = integrate(sym_expr, x)

            return {
                "operation": "integral",
                "input": str(sym_expr),
                "result": str(result),
                "explanation": f"The integral of {sym_expr} with respect to x is {result} + C"
            }

        # ================= UNSUPPORTED =================
        else:

            return {
                "operation": "error",
                "input": expr,
                "result": None,
                "explanation": "Unsupported operation"
            }

    except Exception as e:

        return {
            "operation": "error",
            "input": expr,
            "result": None,
            "explanation": f"Invalid expression: {str(e)}"
        }