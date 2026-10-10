import cmath
import math
from typing import Optional
from ..types import *

def get_capacitive_reactance(f: hertz, C: farad) -> ohm:
    """
    Get capacitive reactance in ohms from frequency and capacitance.

    The result is negative imaginary, following the usual ``-jXc`` convention.

    Examples:
        >>> str(get_capacitive_reactance(hertz(k=1), farad(u=1)))
        '[0 - 159.2j]Ω'
    """
    if f == 0:
        return ohm(cmath.inf)
    elif C == 0:
        return ohm(0)
    return ohm(1.0 / (2.0 * math.pi * hertz(f) * farad(C)) * -1j) # TODO: Is this backward? Should it be +1j?

def get_inductive_reactance(f: hertz, L: henry) -> ohm:
    """
    Get inductive reactance in ohms from frequency and inductance.

    Examples:
        >>> str(get_inductive_reactance(hertz(k=1), henry(m=1)))
        '[0 + 6.3j]Ω'
    """
    if f == 0:
        return ohm(0)
    return ohm(2.0 * math.pi * hertz(f) * henry(L) * 1j)

def get_reactance_from_impedance(Z: ohm, phase: Optional[float] = None) -> ohm:
    """
    Get reactance in ohms from complex impedance.

    Args:
        Z: Complex impedance in the form ``R + Xj``.
        phase: Optional phase angle in radians if ``Z`` only supplies magnitude.

    Examples:
        >>> get_reactance_from_impedance(ohm(10 + 5j))
        ohm(5.0)
    """
    impedance = ohm(Z)
    if phase is not None:
        impedance = ohm(cmath.rect(impedance.real, phase))
    return ohm(impedance.imag)

def get_reactance_from_susceptance(B: siemens) -> ohm:
    """
    Get reactance in ohms from susceptance in siemens.

    Examples:
        >>> get_reactance_from_susceptance(siemens(0.5))
        ohm(2.0)
    """
    return ohm(1.0 / siemens(B))

def get_susceptance_from_reactance(X: ohm) -> siemens:
    """
    Get susceptance in siemens from reactance in ohms.

    Examples:
        >>> get_susceptance_from_reactance(ohm(2))
        siemens(0.5)
    """
    return siemens(1.0 / ohm(X))

# @overload
# def get_reactance(*, f: hertz, C: farad) -> ohm: ...
# @overload
# def get_reactance(*, f: hertz, L: henry) -> ohm: ...
# @overload
# def get_reactance(*, B: siemens) -> ohm: ...
# @overload
# def get_reactance(*, Z: ohm) -> ohm: ...
# @overload
# def get_reactance(*, Z: ohm, phase: float) -> ohm: ...
