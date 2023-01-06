from ..value.unit import *
from .quantity import Quantity

P = power = Quantity[watt]("P", "power")


@P.solution
def P_from_IV(I: ampere, V: volt) -> watt:
    """Get power in watts from electric current in amperes and voltage in volts."""
    return watt(ampere(I) * volt(V))


@P.solution
def P_from_IR(I: ampere, R: ohm) -> watt:
    """Get power in watts from electric current in amperes and resistance in ohms."""
    return watt(ampere(I)**2 * ohm(R))


@P.solution
def P_from_RV(R: ohm, V: volt) -> watt:
    """Get power in watts from electric resistance in ohms and voltage in volts."""
    return watt(volt(V)**2 / ohm(R))


@P.solution
def P_from_tE(t: second, E: joule) -> watt:
    """Get power in watts from time in seconds and energy in joules."""
    return watt(joule(E) / second(t))
