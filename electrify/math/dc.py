import numpy as np


def conductance(R, X=0):
    return R / (R**2 + X**2)


def solve_for_V(I=None, R=None, P=None):
    if I and R:
        return I * R
    elif P and I:
        return P / I
    elif P and R:
        return np.sqrt(P * R)


def solve_for_I(V=None, R=None, P=None):
    if V and R:
        return V / R
    elif P and V:
        return P / V
    elif P and R:
        return np.sqrt(P / R)


def solve_for_R(V=None, I=None, P=None):
    if V and I:
        return V / I
    elif P and I:
        return P / (I**2)
    elif P and V:
        return (V**2) / P


def solve_for_P(V=None, I=None, R=None):
    if V and I:
        return V * I
    elif I and R:
        return (I**2) * R
    elif V and R:
        return (V**2) / R

# def solve(V=None, I=None, R=None, P=None):
#     if V is None:
#         V = solve_for_V(I, R, P, Z, angle)
#     if I is None:
#         I = solve_for_I(V, R, P, Z, angle)
#     if R is None:
#         R = solve_for_R(V, I, P)
#     if P is None:
#         P = solve_for_P(V, I, R, Z, angle)
#     return {'V':V, 'I':I, 'R':R, 'P':P}
