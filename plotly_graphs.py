import numpy as np
import plotly.graph_objects as go

def plot_graph(topic):
    x = np.linspace(-10, 10, 400)

    if "Derivative" in topic:
        y = 2 * x
        title = "Derivative Example: f'(x) = 2x"
    elif "Integral" in topic:
        y = np.sin(x)
        title = "Integral Example: sin(x)"
    else:
        y = x**2
        title = "Example Graph: f(x)=x²"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Graph'))
    fig.update_layout(title=title, xaxis_title="x", yaxis_title="y")

    return fig