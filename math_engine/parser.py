import sympy as sp

# Import engines
from math_engine.algebra import solve_equation, factor_expression, simplify_expression # type: ignore
from math_engine.calculus import derivative,integral,limit,taylor_series, solve_ode,laplace,inverse_laplace # type: ignore

from math_engine.matrix import determinant, eigenvalues # type: ignore
from math_engine.steps import solve_steps, derivative_steps, integral_steps # type: ignore


def parse_math_input(user_input):

    x = sp.symbols('x')

    try:

        user_input = user_input.replace("^", "**")

        # -------------------------
        # DERIVATIVE
        # -------------------------
        if "d/dx" in user_input:

            expr = user_input.replace("d/dx", "")
            expr = sp.sympify(expr)

            steps = derivative_steps(expr)

            return "<br>".join(steps)


        # -------------------------
        # INTEGRAL
        # -------------------------
        elif "∫" in user_input or "integrate" in user_input:

            expr = user_input.replace("∫", "").replace("integrate", "")
            expr = sp.sympify(expr)

            steps = integral_steps(expr)

            return "<br>".join(steps)


        # -------------------------
        # LIMIT
        # -------------------------
        elif "lim" in user_input:

            expr = user_input.replace("lim", "")
            expr = sp.sympify(expr)

            return f"Limit: {limit(expr)}"


        # -------------------------
        # TAYLOR SERIES
        # -------------------------
        elif "series" in user_input:

            expr = user_input.replace("series", "")
            expr = sp.sympify(expr)

            return f"Taylor Series: {taylor_series(expr)}"


        # -------------------------
        # DIFFERENTIAL EQUATION
        # -------------------------
        elif "ode" in user_input:

            expr = user_input.replace("ode", "")
            expr = sp.sympify(expr)

            return f"ODE Solution: {solve_ode(expr)}"


        # -------------------------
        # LAPLACE
        # -------------------------
        elif "laplace" in user_input:

            expr = user_input.replace("laplace", "")
            expr = sp.sympify(expr)

            return f"Laplace Transform: {laplace(expr)}"


        # -------------------------
        # INVERSE LAPLACE
        # -------------------------
        elif "ilaplace" in user_input:

            expr = user_input.replace("ilaplace", "")
            expr = sp.sympify(expr)

            return f"Inverse Laplace: {inverse_laplace(expr)}"


        # -------------------------
        # FACTOR
        # -------------------------
        elif "factor" in user_input:

            expr = user_input.replace("factor", "")
            expr = sp.sympify(expr)

            return f"Factorized: {factor_expression(expr)}"


        # -------------------------
        # MATRIX DETERMINANT
        # -------------------------
        elif "det" in user_input:

            matrix = eval(user_input.replace("det", ""))

            return f"Determinant: {determinant(matrix)}"


        # -------------------------
        # EIGENVALUES
        # -------------------------
        elif "eigen" in user_input:

            matrix = eval(user_input.replace("eigen", ""))

            return f"Eigenvalues: {eigenvalues(matrix)}"


        # -------------------------
        # EQUATION SOLVER (WITH STEPS)
        # -------------------------
        elif "=" in user_input:

            left, right = user_input.split("=")

            expr = sp.sympify(left) - sp.sympify(right)

            steps = solve_steps(expr)

            return "<br>".join(steps)


        # -------------------------
        # POLYNOMIAL ROOTS
        # -------------------------
        elif "x" in user_input:

            expr = sp.sympify(user_input)

            roots = solve_equation(expr)

            if roots:
                return f"Roots: {roots}"
            else:
                return f"Simplified: {simplify_expression(expr)}"


        # -------------------------
        # GENERAL SIMPLIFY
        # -------------------------
        else:

            expr = sp.sympify(user_input)

            return f"Simplified: {simplify_expression(expr)}"


    except Exception as e:

        return f"Error: {e}"
    