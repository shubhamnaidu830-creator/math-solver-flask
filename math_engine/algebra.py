import sympy as sp

def solve_equation(expr):

    x = sp.symbols('x')

    roots = sp.solve(expr, x)

    return roots


def factor_expression(expr):

    return sp.factor(expr)


def simplify_expression(expr):

    return sp.simplify(expr)