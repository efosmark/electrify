import cmath
from typing import Optional
from ..value.unit import *
from .quantity import Quantity

X = reactance = Quantity[ohm]("X", "reactance")
B = susceptance = Quantity[siemens]("B", "susceptance")


@X.solution
def X_from_fC(f: hertz, C: farad) -> ohm:
    """Get reactance in ohms from frequency in hertz and capacitance in farads."""
    return ohm(1.0 / (2.0 * cmath.pi * hertz(f) * farad(C)))


@X.solution
def X_from_fL(f: hertz, L: henry) -> ohm:
    """Get reactance in ohms from frequency in hertz and inductance in henrys."""
    return ohm(2.0 * cmath.pi * hertz(f) * henry(L))


@X.solution
def X_from_Z(Z: ohm, phase: Optional[float] = None) -> ohm:
    """Get reactance in ohms from impedance in the form (R+Xj) in ohms."""
    if phase is not None:
        Z = ohm(cmath.rect(Z.real, phase))
    if not isinstance(Z, complex):
        raise TypeError("Z must be a complex value in the form of (R+Xj)."
                        "Otherwise, the phase angle must be supplied.")
    return ohm(Z.imag)


@X.solution
def X_from_B(B: siemens) -> ohm:
    """Get reactance in ohms from susceptance in siemens."""
    return ohm(1.0 / siemens(B))


@B.solution
def B_from_X(X: ohm) -> siemens:
    """Get susceptance in siemens from reactance in ohms."""
    return siemens(1.0 / ohm(X))
