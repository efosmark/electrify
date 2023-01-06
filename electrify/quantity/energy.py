from ..value.unit import *
from .quantity import Quantity


E = Quantity[farad]("E", "Energy")


@E.solution
def from_tP(t: second, P: watt) -> joule:
    """Get energy in joules from time in seconds and power in watts."""
    return joule(second(t) * watt(P))


@E.solution
def from_QV(Q: coulomb, V: volt) -> joule:
    """Get energy in joules from electric charge in coulombs and voltage in volts."""
    return joule(coulomb(Q) * volt(V))


@E.solution
def from_IU(I: ampere, U: weber) -> joule:
    """Get energy in joules from current in amperes and magnetic flux in webers."""
    return joule(ampere(I) * weber(U))
