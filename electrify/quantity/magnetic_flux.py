from typing import overload
from ..value.unit import *
from .quantity import Quantity

U = magnetic_flux = Quantity[weber]("U", "magnetic_flux")


@U.solution
def from_IL(I: ampere, L: henry) -> weber:
    """Get magnetic flux in webers from electric current in amperes and inductance in henrys."""
    return weber(ampere(I) * henry(L))


@U.solution
def from_RQ(R: ohm, Q: coulomb) -> weber:
    """Get magnetic flux in webers from resistance in ohms and electric charge in coulombs."""
    return weber(ohm(R) * coulomb(Q))


@U.solution
def from_EI(E: joule, I: ampere) -> weber:
    """Get magnetic flux in webers from energy in joules and electric current in amperes."""
    return weber(joule(E) / ampere(I))


@U.solution
def from_tV(t: second, V: volt) -> weber:
    """Get magnetic flux in webers from time in seconds and voltage in volts."""
    return weber(second(t) * volt(V))


@overload
def get_magnetic_flux(*, I: ampere, L: henry) -> weber: ...
@overload
def get_magnetic_flux(*, R: ohm, Q: coulomb) -> weber: ...
@overload
def get_magnetic_flux(*, E: joule, I: ampere) -> weber: ...
@overload
def get_magnetic_flux(*, t: second, V: volt) -> weber: ...


def get_magnetic_flux(**kwargs: base_unit | complex | float) -> weber:
    """Calculate the magnetic flux in webers based on the quantities supplied."""
    return U.get(**kwargs)
