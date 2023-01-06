from ..value.unit import *
from .quantity import Quantity

I = current = Quantity[ampere]("I", "current")


@I.solution
def from_RV(R: ohm, V: volt) -> ampere:
    """Get current in amperes from resistance in ohms and voltage in volts."""
    return ampere(volt(V) / ohm(R))


@I.solution
def from_PR(P: watt, R: ohm) -> ampere:
    """Get electric current in amperes from power in watts and resistance in ohms."""
    return ampere((watt(P) / ohm(R))**0.5)


@I.solution
def from_PV(P: watt, V: volt) -> ampere:
    """Get electric current in amperes from power in watts and voltage in volts."""
    return ampere(watt(P) / volt(V))


@I.solution
def from_LU(L: henry, U: weber) -> ampere:
    """Get electric current in amperes from inductance in henrys and magnetic flux in webers."""
    return ampere(weber(U) / henry(L))


@I.solution
def from_EU(E: joule, U: weber) -> ampere:
    """Get electric current in amperes from energy in joules and magnetic flux in webers."""
    return ampere(joule(E) / weber(U))
