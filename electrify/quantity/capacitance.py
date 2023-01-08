"""
Contains functions around values related to capacitance.

Examples
--------
>>> # Not yet provided.

"""
import cmath
from typing import overload
from ..value.unit import *
from .quantity import Quantity
from ..constants import OPEN_CIRCUIT
from ..value.unit import *


C = capacitance = Quantity[farad]("C", "capacitance")


@C.solution
def from_QV(Q: coulomb, V: volt) -> farad:
    """Get capacitance in farads from electric charge in coulombs and voltage in volts."""
    return farad(coulomb(Q) / volt(V))


@C.solution
def from_tR(t: second, R: ohm) -> farad:
    """Get capacitance in farads from time in seconds and resistance in ohms."""
    return farad(second(t) / ohm(R))


@C.solution
def from_fX(f: hertz, X: ohm) -> farad:
    """Get capacitance in farads from frequency in ohms and capacitive reactance in ohms."""
    if f <= 0:
        raise ValueError('Frequency must be a positive number. Received: "{}"'.format(f))
    elif X == 0:
        return farad(0)
    return farad(1.0 / (2.0 * cmath.pi * hertz(f) * abs(ohm(X))))


@C.solution
def from_EQ(E: joule, Q: coulomb) -> farad:
    """Get capacitance in farads from energy in joules and electric charge in coulombs."""
    return farad(coulomb(Q)**2.0 / joule(E))


@C.solution
def from_EV(E: joule, V: volt) -> farad:
    """Get capacitance in farads from energy in joules and voltage in volts."""
    return farad(joule(E) / volt(V)**2.0)


@overload
def get_capacitance(*, Q: coulomb, V: volt) -> farad: ...
@overload
def get_capacitance(*, t: second, R: ohm) -> farad: ...
@overload
def get_capacitance(*, f: hertz, X: ohm) -> farad: ...
@overload
def get_capacitance(*, E: joule, Q: coulomb) -> farad: ...
@overload
def get_capacitance(*, E: joule, V: volt) -> farad: ...


def get_capacitance(**kwargs: base_unit | complex | float) -> farad:
    """Calculate the capacitance in ohms based on the quantities supplied."""
    return C.get(**kwargs)
