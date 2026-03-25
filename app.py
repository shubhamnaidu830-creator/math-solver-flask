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

app = Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core_math.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equation = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# --- Sympy Parser Settings ---
transformations = standard_transformations + (implicit_multiplication_application,)

def preprocess_equation(eq):
    """Handles standard user input and converts to Sympy-ready format."""
    eq = eq.replace("^", "**")
    if "=" in eq:
        left, right = eq.split("=")
        eq = f"({left})-({right})"
    return eq

def generate_tactical_graph(expr, roots=None):
    """Generates the HUD-style glowing graph."""
    x = sp.symbols('x')
    try:
        f = sp.lambdify(x, expr, "numpy")
        xs = np.linspace(-10, 10, 400)
        ys = f(xs)
        if isinstance(ys, (int, float)):
            ys = np.full_like(xs, ys)
    except:
        xs = np.linspace(-10, 10, 400)
        ys = np.zeros_like(xs)

    fig = go.Figure()
    # Cyan line with a faint area fill for that holographic look
    fig.add_trace(go.Scatter(
        x=xs, y=ys, 
        mode='lines', 
        name='f(x)', 
        line=dict(color='#00f2ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 242, 255, 0.05)'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00f2ff', family="Orbitron"),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='#ffffff'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='#ffffff'),
        showlegend=False,
        height=350
    )
    return fig.to_html(full_html=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Initializing HUD data structure
    context = {
        "equation_latex": None,
        "solution": None,
        "steps": [],
        "graph": None
    }

    if request.method == 'POST':
        prob_eq = request.form.get('equation')
        if not prob_eq:
            return render_template("index.html", **context)

        try:
            # Step 1: Initialize Scan
            processed = preprocess_equation(prob_eq)
            expr = parse_expr(processed, transformations=transformations)
            context["equation_latex"] = sp.latex(expr)
            context["steps"].append({"op": "SCAN", "msg": f"Target locked: $${sp.latex(expr)}$$"})
            
            # Step 2: Optimization Sequence
            simplified = sp.simplify(expr)
            if simplified != expr:
                context["steps"].append({"op": "OPTZ", "msg": f"Simplifying structure: $${sp.latex(simplified)}$$"})
            
            # Step 3: Differential Analysis (Internal)
            x_sym = sp.symbols('x')
            diff_expr = sp.diff(simplified, x_sym)
            context["steps"].append({"op": "CORE", "msg": f"Gradient calculated: $${sp.latex(diff_expr)}$$"})

            # Step 4: Symbolic Extraction
            roots = sp.solve(simplified, x_sym)
            context["steps"].append({"op": "DONE", "msg": f"Extraction complete. Found {len(roots)} roots."})
            
            # Step 5: Final Result Formatting
            if roots:
                context["solution"] = "<br>".join([f"$$ x = {sp.latex(r)} $$" for r in roots])
            else:
                context["solution"] = "No real roots detected in current coordinate plane."

            # Step 6: Visual Projection
            context["graph"] = generate_tactical_graph(expr, roots)

            # DB Log
            new_calc = Calculation(equation=prob_eq, solution=str(roots))
            db.session.add(new_calc)
            db.session.commit()

        except Exception as e:
            context["steps"] = [{"op": "ERR!", "msg": f"Logic Conflict: {str(e)}"}]

    return render_template("index.html", **context)

if __name__ == "__main__":
    app.run(debug=True)