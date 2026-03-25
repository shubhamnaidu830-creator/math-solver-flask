from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import sympy as sp
import numpy as np
import plotly.graph_objs as go

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

# custom math engine
from math_engine.algebra import solve_equation  # type: ignore

# -----------------------------
# Sympy parser settings
# -----------------------------
transformations = standard_transformations + (
    implicit_multiplication_application,
)

# -----------------------------
# Flask App
# -----------------------------
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mathlab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# Database Model
# -----------------------------
class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    equation = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def repr(self):
        return f'<Calculation {self.id}>'

with app.app_context():
    db.create_all()

# -----------------------------
# Equation Preprocessor
# -----------------------------
def preprocess_equation(eq):
    eq = eq.replace("^", "**")
    if "=" in eq:
        left, right = eq.split("=")
        eq = f"({left})-({right})"
    return eq

# -----------------------------
# Newton Method
# -----------------------------
def newton_method(expr, x0=1, tol=1e-6, max_iter=50):
    x = sp.symbols('x')
    f = sp.lambdify(x, expr, "numpy")
    fprime_expr = sp.diff(expr, x)
    fprime = sp.lambdify(x, fprime_expr, "numpy")

    xn = x0
    table = []

    for i in range(max_iter):
        try:
            xn1 = xn - f(xn)/fprime(xn)
        except:
            break

        table.append((i+1, xn, xn1))

        if abs(xn1-xn) < tol:
            return xn1, table

        xn = xn1

    return xn, table

# -----------------------------
# Bisection Method
# -----------------------------
def bisection_method(expr, tol=1e-6):
    x = sp.symbols('x')
    f = sp.lambdify(x, expr, "numpy")

    xs = np.linspace(-10, 10, 200)

    a = None
    b = None

    for i in range(len(xs)-1):
        if f(xs[i]) * f(xs[i+1]) < 0:
            a = xs[i]
            b = xs[i+1]
            break

    if a is None:
        return None, []

    table = []

    while abs(b-a) > tol:
        c = (a+b)/2
        table.append((a,b,c))

        if f(c) == 0:
            break
        elif f(a)*f(c) < 0:
            b = c
        else:
            a = c

    return (a+b)/2, table

# -----------------------------
# Graph Generator
# -----------------------------
def generate_graph(expr, roots=None):
    x = sp.symbols('x')

    try:
        f = sp.lambdify(x, expr, "numpy")
        xs = np.linspace(-10, 10, 400)
        ys = np.real(f(xs))
    except:
        xs = np.linspace(-10,10,400)
        ys = np.zeros_like(xs)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=xs, y=ys, mode='lines', name='f(x)')
    )

    if roots:
        real_roots = []
        for r in roots:
            try:
                real_roots.append(float(sp.re(r)))
            except:
                pass

        fig.add_trace(
            go.Scatter(
                x=real_roots,
                y=[0]*len(real_roots),
                mode='markers',
                marker=dict(size=10),
                name="Roots"
            )
        )

    fig.update_layout(
        title="Function Graph",
        xaxis_title="x",
        yaxis_title="y"
    )

    return fig.to_html(full_html=False)

# -----------------------------
# Home Route (UPDATED WITH STEPS)
# -----------------------------
@app.route('/', methods=['GET','POST'])
def home():

    solution_text = None
    graph_html = None
    newton_table = None
    bisection_table = None
    equation_latex = None
    steps = []

    if request.method == 'POST':

        prob_title = request.form.get('title','Math Problem')
        prob_eq = request.form.get('equation')

        try:
            # Step 1
            steps.append(f"Input Equation: {prob_eq}")

            # Step 2
            processed = preprocess_equation(prob_eq)
            steps.append(f"After preprocessing: {processed}")

            # Step 3
            expr = parse_expr(processed, transformations=transformations)
            steps.append(f"Parsed expression: {expr}")

            equation_latex = sp.latex(expr)

            # Step 4
            roots = solve_equation(expr)
            steps.append(f"Symbolic roots: {roots}")

            latex_roots = [sp.latex(r) for r in roots]
            solution_text = "Symbolic Roots:<br>" + "<br>".join([f"$$ {r} $$" for r in latex_roots])

            # Step 5
            newton_root, newton_table = newton_method(expr)
            steps.append(f"Newton root ≈ {newton_root}")
            solution_text += f"<br>Newton Root ≈ {newton_root}"

            # Step 6
            bisection_root, bisection_table = bisection_method(expr)
            steps.append(f"Bisection root ≈ {bisection_root}")
            solution_text += f"<br>Bisection Root ≈ {bisection_root}"

            # Step 7
            graph_html = generate_graph(expr, roots)
            steps.append("Graph generated")

            # Save
            new_calc = Calculation(
                title=prob_title,
                equation=prob_eq,
                solution=solution_text
            )

            db.session.add(new_calc)
            db.session.commit()

        except Exception as e:
            solution_text = f"Error: {e}"
            steps = []

    return render_template(
        "index.html",
        solution=solution_text,
        graph=graph_html,
        newton_table=newton_table,
        bisection_table=bisection_table,
        equation_latex=equation_latex,
        steps=steps
    )

# -----------------------------
# Library Route
# -----------------------------
@app.route('/numerical')
def numerical_library():
    calculations = Calculation.query.order_by(
        Calculation.date_created.desc()
    ).all()

    return render_template(
        "numerical.html",
        calculations=calculations
    )

# -----------------------------
# Run
# -----------------------------
if __name__ == "main":
    app.run(debug=True)