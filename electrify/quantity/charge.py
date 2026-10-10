from typing import overload
from ..types import *

def from_tI(t: second, I: ampere) -> coulomb:
    """Get electric charge in coulombs from time in seconds and current in amperes."""
    return coulomb(second(t) * ampere(I))

def from_CV(C: farad, V: volt) -> coulomb:
    """Get electric charge in coulombs from capacitance in farads and voltage in volts."""
    return coulomb(farad(C) * volt(V))

def from_EV(E: joule, V: volt) -> coulomb:
    """Get electric charge in coulombs from energy in joules and voltage in volts."""
    return coulomb(joule(E) / volt(V))

def from_RU(R: ohm, U: weber) -> coulomb:
    """Get electric charge in coulombs from resistance in ohms and magnetic flux in webers."""
    return coulomb(weber(U) / ohm(R))

@overload
def get_charge(*, t: second, I: ampere) -> coulomb: ...
@overload
def get_charge(*, C: farad, V: volt) -> coulomb: ...
@overload
def get_charge(*, E: joule, V: volt) -> coulomb: ...
@overload
def get_charge(*, R: ohm, U: weber) -> coulomb: ...
def get_charge(**kwargs: ElectricUnit | complex | float) -> coulomb:
    """Calculate the electric charge in coulombs based on the quantities supplied."""
    ...
