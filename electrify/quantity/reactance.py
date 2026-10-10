import cmath, math
from typing import Optional
from ..types import *

def get_capacitive_reactance(f: hertz, C: farad) -> ohm:
    """Get reactance in ohms from frequency in hertz and capacitance in farads."""
    print(f'get_capacitive_reactance({f}, {C})')
    if f == 0:
        return ohm(cmath.inf)
    elif C == 0:
        return ohm(0)
    return ohm(1.0 / (2.0 * math.pi * hertz(f) * farad(C)) * -1j) # TODO: Is this backward? Should it be +1j?

def get_inductive_reactance(f: hertz, L: henry) -> ohm:
    """Get reactance in ohms from frequency in hertz and inductance in henrys."""
    if f == 0:
        return ohm(0)
    return ohm(2.0 * math.pi * hertz(f) * henry(L) * 1j)

def get_reactance_from_impedance(Z: ohm, phase: Optional[float] = None) -> ohm:
    """Get reactance in ohms from impedance in the form (R+Xj) in ohms."""
    if phase is not None:
        Z = ohm(cmath.rect(Z.real, phase))
    if not isinstance(Z, complex):
        raise TypeError("Z must be a complex value in the form of (R+Xj)."
                        "Otherwise, the phase angle must be supplied.")
    return ohm(Z.imag)

def get_reactance_from_susceptance(B: siemens) -> ohm:
    """Get reactance in ohms from susceptance in siemens."""
    return ohm(1.0 / siemens(B))

def get_susceptance_from_reactance(X: ohm) -> siemens:
    """Get susceptance in siemens from reactance in ohms."""
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
