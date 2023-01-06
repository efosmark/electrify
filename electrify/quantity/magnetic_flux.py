from ..value.unit import *
from .quantity import Quantity

U = magnetic_flux = Quantity[weber]("U", "magnetic_flux")


@U.solution
def U_from_IL(I: ampere, L: henry) -> weber:
    """Get magnetic flux in webers from electric current in amperes and inductance in henrys."""
    return weber(ampere(I) * henry(L))


@U.solution
def U_from_RQ(R: ohm, Q: coulomb) -> weber:
    """Get magnetic flux in webers from resistance in ohms and electric charge in coulombs."""
    return weber(ohm(R) * coulomb(Q))


@U.solution
def U_from_EI(E: joule, I: ampere) -> weber:
    """Get magnetic flux in webers from energy in joules and electric current in amperes."""
    return weber(joule(E) / ampere(I))


@U.solution
def U_from_tV(t: second, V: volt) -> weber:
    """Get magnetic flux in webers from time in seconds and voltage in volts."""
    return weber(second(t) * volt(V))
