import numpy as np


def impedance(R, XL=0, XC=0):
    return np.sqrt(R**2 + (XL-XC)**2)


def susceptance(R=0, X=1):
    if R == 0:
        return 1 / X
    else:
        return X / (R**2 + X**2)


def admittance(Z=None, R=None, X=None):
    if R is not None and X is not None:
        return 1 / np.sqrt(R**2 + X**2)
    elif Z is not None:
        return 1 / Z
    else:
        raise ValueError("Must specify 'Z' or both 'R' and 'X'")


def phase(cx, deg=False):
    if deg:
        if cx.real == 0:
            return 90
        return np.degrees(np.arctan(cx.imag/cx.real))
    if cx.real == 0:
        return 1.6
    return np.arctan(cx.imag/cx.real)


def phase_angle(cx, deg=False):
    ''' Phase angle in degrees from complex input (x+yj)

    cx - Complex number representing the response from H(ω)
    '''
    if deg:  # TODO: Switch this back to arctan2(cx.imag, cx.real)
        if cx.real == 0:
            if cx.imag > 0:
                return 90
            else:
                return -90
        return -np.degrees(np.arctan2(cx.imag, cx.real))
    if cx.real == 0:
        if cx.imag > 0:
            return np.pi / 2.0
        else:
            return (np.pi / 2.0)
    return np.arctan2(cx.imag, cx.real)


def power_factor(V=None, I=None, P=None, R=None, Z=None, angle=None):
    '''

    '''
    if P and V and I:
        return P / (V * I)
    elif R and Z:
        return R / Z
    elif angle:
        return np.cos(angle)
    else:
        raise ValueError("Must specify ('P', 'V', and 'I') or ('Z' and 'R') or 'angle'")


def solve_for_V(I=None, P=None, Z=None, angle=None):
    if P is not None and I is not None and angle is not None:
        return P / (I * np.cos(angle))
    elif P is not None and Z is not None and angle is not None:
        return np.sqrt(P * Z) / np.cos(angle)
    elif I and Z:
        return I * Z
    elif P and I:
        return P / I


def solve_for_I(V=None, P=None, Z=None, angle=None):
    if P is not None and V is not None and angle is not None:
        return P / (V * np.cos(angle))
    elif P is not None and Z is not None and angle is not None:
        return np.sqrt(P) / (Z * np.cos(angle))
    elif V and Z:
        return V / Z
    elif P and V:
        return P / V


def solve_for_Z(V=None, I=None, R=None, P=None, angle=None):
    if R and angle:
        return R / np.cos(angle)
    elif P and I and angle:
        return P / (I**2 * np.cos(angle))
    elif P and V and angle:
        return ((V**2) * np.cos(angle)) / P
    elif V and I:
        return V / I


def solve_for_P(V=None, I=None, R=None, Z=None, angle=None):
    if V and I and angle:
        return 0.5 * (V * I * np.cos(angle))
    elif V and Z and angle:
        return ((V**2) * np.cos(angle)) / Z
    elif I and Z and angle:
        return (I**2) * Z * np.cos(angle)
    elif V and I:
        return V * I
    elif I and R:
        return (I**2) * R
    elif V and R:
        return (V**2) / R


def solve(V=None, I=None, R=None, P=None, Z=None, angle=None):
    if V is None:
        V = solve_for_V(I, R, P, Z, angle)
    if I is None:
        I = solve_for_I(V, R, P, Z, angle)
    if Z is None:
        Z = solve_for_Z(V, I, R, P, angle)
    if P is None:
        P = solve_for_P(V, I, R, Z, angle)
    return {'V': V, 'I': I, 'Z': Z, 'P': P}
