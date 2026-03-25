import sympy as sp
import numpy as np
import plotly.graph_objs as go


# -----------------------------
# 2D GRAPH
# -----------------------------
def generate_graph(expr):

    x = sp.symbols('x')

    f = sp.lambdify(x, expr, "numpy")

    xs = np.linspace(-10, 10, 400)

    ys = f(xs)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode='lines',
            name='f(x)'
        )
    )

    fig.update_layout(
        title="Function Graph",
        xaxis_title="x",
        yaxis_title="y"
    )

    return fig.to_html(full_html=False)


# -----------------------------
# 3D GRAPH
# -----------------------------
def generate_3d_graph(expr):

    x, y = sp.symbols('x y')

    f = sp.lambdify((x, y), expr, "numpy")

    X = np.linspace(-5, 5, 50)
    Y = np.linspace(-5, 5, 50)

    X, Y = np.meshgrid(X, Y)

    Z = f(X, Y)

    fig = go.Figure(
        data=[go.Surface(z=Z, x=X, y=Y)]
    )

    fig.update_layout(
        title="3D Surface Plot",
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z'
        )
    )

    return fig.to_html(full_html=False)