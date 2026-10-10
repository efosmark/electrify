import cmath
from typing import overload
from ..value.unit import *
from .quantity import Quantity

phase = Quantity[float]("phase")


@phase.solution
def from_RX(R: ohm, X: ohm) -> float:
    """Get phase angle in radians from resistance in ohms and reactance in ohms."""
    return cmath.atan(ohm(R) / ohm(X)).real


@phase.solution
def from_Z(Z: ohm) -> float:
    """Get phase angle in radians from impedance (R+Xj) in ohms."""
    return from_RX(ohm(Z.real), ohm(Z.imag))


@overload
def get_phase(*, R: ohm, X: ohm) -> float: ...
@overload
def get_phase(*, Z: ohm) -> float: ...


def get_phase(**kwargs: base_unit | complex | float) -> float:
    """Calculate the phase angle in radians based on the quantities supplied."""
    return phase.get(**kwargs)
