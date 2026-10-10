import cmath
from typing import overload
from ..types import *

def from_RX(R: ohm, X: ohm) -> ohm:
    """Get complex impedance in ohms from resistance in ohms and reactance in ohms."""
    return ohm(complex(ohm(R), X.magnitude))

def from_R_phase(R: ohm, phase: float) -> ohm:
    """Get impedance (R+Xj) from resistance in ohms and phase angle in radians."""
    magnitude = (ohm(R) / cmath.cos(phase)).real
    return ohm(cmath.rect(magnitude, phase))

def from_X_phase(X: ohm, phase: float) -> ohm:
    """Get impedance (R+Xj) from reactance in ohms and phase angle in radians."""
    magnitude = (ohm(X) / cmath.sin(phase)).real
    return ohm(cmath.rect(magnitude, phase))

def Z_from_Y(Y: siemens) -> ohm:
    """Get inductance in ohms from admittance in siemens."""
    return ohm(1.0 / siemens(Y))

def from_Z(Z: ohm) -> siemens:
    """Get admittance in siemens from impedance in ohms."""
    return siemens(1.0 / ohm(Z))

@overload
def get_impedance(*, R: ohm, X: ohm) -> ohm: ...
@overload
def get_impedance(*, R: ohm, phase: float) -> ohm: ...
@overload
def get_impedance(*, X: ohm, phase: float) -> ohm: ...
@overload
def get_impedance(*, Y: siemens) -> ohm: ...
def get_impedance(**kwargs: ElectricUnit | complex | float) -> ohm:
    """Calculate the impedance in ohms based on the quantities supplied."""
    ...
