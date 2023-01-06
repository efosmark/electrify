from ..value.unit import *
from .quantity import Quantity

t = time = Quantity[second]("t", "time")


@t.solution
def t_from_f(f: hertz) -> second:
    """Get time in seconds from frequency in hertz."""
    return second(1.0 / hertz(f))


@t.solution
def t_from_RC(C: farad, R: ohm) -> second:
    """Get time in seconds from capacitance in farads and resistance in ohms."""
    return second(farad(C) * ohm(R))


@t.solution
def t_from_LC(L: henry, R: ohm) -> second:
    """Get time in seconds from inductance in henrys and resistance in ohms."""
    return second(henry(L) / ohm(R))


@t.solution
def t_from_IQ(I: ampere, Q: coulomb) -> second:
    """Get time in seconds from electric current in amperes and electric charge in coulombs."""
    return second(coulomb(Q) / ampere(I))


@t.solution
def t_from_UV(U: weber, V: volt) -> second:
    """Get time in seconds from magnetic flux in webers and voltage in volts."""
    return second(weber(U) / volt(V))


# @t.register_solver
# def t_from_EP(E: joule, P: watt) -> second:
#     return second(joule(E) / watt(P))
