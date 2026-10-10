from typing import overload
from ..types import *

def from_f(f: hertz) -> second:
    """Get time in seconds from frequency in hertz."""
    return second(1.0 / hertz(f))

def from_RC(C: farad, R: ohm) -> second:
    """Get time in seconds from capacitance in farads and resistance in ohms."""
    return second(farad(C) * ohm(R))

def from_LC(L: henry, R: ohm) -> second:
    """Get time in seconds from inductance in henrys and resistance in ohms."""
    return second(henry(L) / ohm(R))

def from_IQ(I: ampere, Q: coulomb) -> second:
    """Get time in seconds from electric current in amperes and electric charge in coulombs."""
    return second(coulomb(Q) / ampere(I))

def from_UV(U: weber, V: volt) -> second:
    """Get time in seconds from magnetic flux in webers and voltage in volts."""
    return second(weber(U) / volt(V))

@overload
def get_duration(*, f: hertz) -> second: ...
@overload
def get_duration(*, C: farad, R: ohm) -> second: ...
@overload
def get_duration(*, L: henry, R: ohm) -> second: ...
@overload
def get_duration(*, I: ampere, Q: coulomb) -> second: ...
@overload
def get_duration(*, U: weber, V: volt) -> second: ...
def get_duration(**kwargs: ElectricUnit | complex | float) -> second:
    """Calculate the duration in seconds based on the quantities supplied."""
    ...
