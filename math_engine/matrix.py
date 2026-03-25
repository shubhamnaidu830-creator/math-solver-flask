import sympy as sp

def determinant(matrix):

    M = sp.Matrix(matrix)

    return M.det()


def eigenvalues(matrix):

    M = sp.Matrix(matrix)

    return M.eigenvals()