import cmath
from typing import Optional, overload
from ..value.unit import *
from .quantity import Quantity

X = reactance = Quantity[ohm]("X", "reactance")
B = susceptance = Quantity[siemens]("B", "susceptance")


@X.solution
def get_capacitive_reactance(f: hertz, C: farad) -> ohm:
    """Get reactance in ohms from frequency in hertz and capacitance in farads."""
    if f == 0:
        return ohm(0)
    elif C == 0:
        return ohm(0)
    return ohm(1.0 / (2.0 * cmath.pi * hertz(f) * farad(C)))


@X.solution
def get_inductive_reactance(f: hertz, L: henry) -> ohm:
    """Get reactance in ohms from frequency in hertz and inductance in henrys."""
    if f == 0:
        return ohm(0)
    elif L == 0:
        return ohm(cmath.inf)
    return ohm(2.0 * cmath.pi * hertz(f) * henry(L))


@X.solution
def get_reactance_from_impedance(Z: ohm, phase: Optional[float] = None) -> ohm:
    """Get reactance in ohms from impedance in the form (R+Xj) in ohms."""
    if phase is not None:
        Z = ohm(cmath.rect(Z.real, phase))
    if not isinstance(Z, complex):
        raise TypeError("Z must be a complex value in the form of (R+Xj)."
                        "Otherwise, the phase angle must be supplied.")
    return ohm(Z.imag)


@X.solution
def get_reactance_from_susceptance(B: siemens) -> ohm:
    """Get reactance in ohms from susceptance in siemens."""
    return ohm(1.0 / siemens(B))


@B.solution
def get_susceptance_from_reactance(X: ohm) -> siemens:
    """Get susceptance in siemens from reactance in ohms."""
    return siemens(1.0 / ohm(X))


@overload
def get_reactance(*, f: hertz, C: farad) -> ohm: ...
@overload
def get_reactance(*, f: hertz, L: henry) -> ohm: ...
@overload
def get_reactance(*, B: siemens) -> ohm: ...
@overload
def get_reactance(*, Z: ohm) -> ohm: ...
@overload
def get_reactance(*, Z: ohm, phase: float) -> ohm: ...


def get_reactance(**kwargs: base_unit | complex | float) -> ohm:
    """Calculate the reactance in ohms based on the quantities supplied."""
    return X.get(**kwargs)
