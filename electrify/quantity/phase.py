import cmath
from ..value.unit import *
from .quantity import Quantity

phase = Quantity[float]("phase")


@phase.solution
def phase_from_RX(R: ohm, X: ohm) -> float:
    """Get phase angle in radians from resistance in ohms and reactance in ohms."""
    return cmath.atan(ohm(R) / ohm(X)).real


@phase.solution
def phase_from_Z(Z: ohm) -> float:
    """Get phase angle in radians from impedance (R+Xj) in ohms."""
    return phase_from_RX(ohm(Z.real), ohm(Z.imag))
