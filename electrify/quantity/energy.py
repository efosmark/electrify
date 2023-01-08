from typing import overload
from ..value.unit import *
from .quantity import Quantity


E = Quantity[joule]("E", "Energy")


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


@overload
def get_energy(*, t: second, P: watt) -> joule: ...
@overload
def get_energy(*, Q: coulomb, V: volt) -> joule: ...
@overload
def get_energy(*, I: ampere, U: weber) -> joule: ...


def get_energy(**kwargs: base_unit | complex | float) -> joule:
    """Calculate the electric energy in joules based on the quantities supplied."""
    return E.get(**kwargs)
