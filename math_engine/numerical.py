import sympy as sp

def newton_method(expr):

    x = sp.symbols('x')

    try:
        root = sp.nsolve(expr, 1)
        return root
    except:
        return None