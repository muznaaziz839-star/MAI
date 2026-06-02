import numpy as np
import plotly.graph_objects as go
# =========================================================
# SAFE MATHEMATICAL FUNCTIONS
# =========================================================
SAFE_FUNCTIONS = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "exp": np.exp,
    "log": np.log,
    "sqrt": np.sqrt,
    "abs": np.abs,
    "pi": np.pi,
    "e": np.e
}


# =========================================================
# CLEAN EXPRESSION
# =========================================================
def clean_expression(expr: str) -> str:
    """
    Convert user-friendly mathematical syntax
    into Python-compatible syntax.
    """

    expr = expr.lower().strip()

    # Convert powers
    expr = expr.replace("^", "**")

    return expr


# =========================================================
# CREATE X RANGE
# =========================================================
def create_x_range(expr: str):
    """
    Create appropriate x-range depending
    on function type.
    """

    if "log" in expr:
        return np.linspace(0.1, 10, 1000)

    return np.linspace(-10, 10, 1000)


# =========================================================
# EVALUATE FUNCTION
# =========================================================
def evaluate_expression(expr: str, x):
    """
    Safely evaluate mathematical expression.
    """

    return eval(
        expr,
        {"__builtins__": {}},
        {
            "x": x,
            **SAFE_FUNCTIONS
        }
    )


# =========================================================
# MAIN GRAPH FUNCTION
# =========================================================
def plot_graph(expr):
    """
    Generate interactive Plotly graph
    for mathematical expressions.
    """

    try:

        # ================= CLEAN INPUT =================
        expr = clean_expression(expr)

        # ================= X VALUES =================
        x = create_x_range(expr)

        # ================= COMPUTE Y =================
        y = evaluate_expression(expr, x)

        # ================= FIGURE =================
        fig = go.Figure()

        # =================================================
        # FUNCTION GRAPH
        # =================================================
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"f(x) = {expr}",
                line=dict(
                    width=3
                ),
                hovertemplate=
                "<b>x:</b> %{x:.3f}<br>" +
                "<b>y:</b> %{y:.3f}<extra></extra>"
            )
        )

        # =================================================
        # LAYOUT
        # =================================================
        fig.update_layout(

            title={
                "text": f"Graph of f(x) = {expr}",
                "x": 0.5,
                "xanchor": "center"
            },

            template="plotly_white",

            height=500,

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            ),

            xaxis=dict(
                title="x",
                zeroline=True,
                showgrid=True
            ),

            yaxis=dict(
                title="y",
                zeroline=True,
                showgrid=True
            ),

            hovermode="x unified"
        )

        # =================================================
        # AXIS LINES
        # =================================================
        fig.add_hline(
            y=0,
            line_width=1,
            opacity=0.5
        )

        fig.add_vline(
            x=0,
            line_width=1,
            opacity=0.5
        )

        return fig

    # =====================================================
    # ERROR HANDLING
    # =====================================================
    except Exception as e:

        fig = go.Figure()

        fig.update_layout(
            title="Unable to Generate Graph",
            template="plotly_white",
            height=400,

            annotations=[
                dict(
                    text=f"Graph Error: {str(e)}",
                    showarrow=False,
                    font=dict(size=14),
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper"
                )
            ]
        )

        return fig