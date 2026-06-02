import numpy as np
from plotly import graph_objects as go

def plot_graph(topic):
    x = np.linspace(-10, 10, 400)

    topic_lower = topic.lower()

    # ================= DERIVATIVE =================
    if "derivative" in topic_lower or "differentiate" in topic_lower:
        y = 2 * x
        title = "Derivative Visualization: f'(x) = 2x"

    # ================= INTEGRAL =================
    elif "integral" in topic_lower or "integration" in topic_lower:
        y = np.sin(x)
        title = "Integral Visualization: ∫ sin(x) dx"

    # ================= QUADRATIC =================
    elif "quadratic" in topic_lower or "x^2" in topic_lower:
        y = x ** 2
        title = "Quadratic Function: f(x) = x²"

    # ================= DEFAULT =================
    else:
        y = x
        title = f"Graph of {topic}"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Graph'))

    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="y"
    )

    return fig