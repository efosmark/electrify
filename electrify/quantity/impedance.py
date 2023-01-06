import cmath
from ..value.unit import *
from .quantity import Quantity

Z = impedance = Quantity[ohm]("Z", "impedance")
Y = admittance = Quantity[siemens]("Y", "admittance")


@Z.solution
def from_RX(R: ohm, X: ohm) -> ohm:
    """Get complex impedance in ohms from resistance in ohms and reactance in ohms."""
    return ohm(complex(ohm(R), ohm(X)))


@Z.solution
def from_R_phase(R: ohm, phase: float) -> ohm:
    """Get impedance (R+Xj) from resistance in ohms and phase angle in radians."""
    magnitude = (ohm(R) / cmath.cos(phase)).real
    return ohm(cmath.rect(magnitude, phase))


@Z.solution
def from_X_phase(X: ohm, phase: float) -> ohm:
    """Get impedance (R+Xj) from reactance in ohms and phase angle in radians."""
    magnitude = (ohm(X) / cmath.sin(phase)).real
    return ohm(cmath.rect(magnitude, phase))


@Z.solution
def Z_from_Y(Y: siemens) -> ohm:
    """Get inductance in ohms from admittance in siemens."""
    return ohm(1.0 / siemens(Y))


@Y.solution
def Y_from_Z(Z: ohm) -> siemens:
    """Get admittance in siemens from impedance in ohms."""
    return siemens(1.0 / ohm(Z))
