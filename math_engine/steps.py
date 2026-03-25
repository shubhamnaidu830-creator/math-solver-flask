import sympy as sp


x = sp.symbols('x')


# ---------------------------
# Solve Equation Steps
# ---------------------------
def solve_steps(expr):

    steps = []

    steps.append(f"Original equation: {expr}")

    factored = sp.factor(expr)

    steps.append(f"Factorized form: {factored}")

    roots = sp.solve(expr, x)

    steps.append(f"Solving factors = 0")

    steps.append(f"Roots: {roots}")

    return steps


# ---------------------------
# Derivative Steps
# ---------------------------
def derivative_steps(expr):

    steps = []

    steps.append(f"Function: {expr}")

    derivative = sp.diff(expr, x)

    steps.append(f"Applying differentiation rule")

    steps.append(f"Derivative: {derivative}")

    return steps


# ---------------------------
# Integral Steps
# ---------------------------
def integral_steps(expr):

    steps = []

    steps.append(f"Function: {expr}")

    integral = sp.integrate(expr, x)

    steps.append("Applying integration rule")

    steps.append(f"Integral: {integral} + C")

    return steps