import sympy as sp

x = sp.symbols('x')
y = sp.Function('y')

def derivative(expr):
    return sp.diff(expr, x)


def integral(expr):
    return sp.integrate(expr, x)


def limit(expr):
    return sp.limit(expr, x, 0)


def taylor_series(expr):
    return sp.series(expr, x, 0, 6)


def solve_ode(expr):
    return sp.dsolve(expr)


def laplace(expr):
    t, s = sp.symbols('t s')
    return sp.laplace_transform(expr, t, s)


def inverse_laplace(expr):
    t, s = sp.symbols('t s')
    return sp.inverse_laplace_transform(expr, s, t)