from typing import overload
from ..types import *

def from_tP(t: second, P: watt) -> joule:
    """Get energy in joules from time in seconds and power in watts."""
    return joule(second(t) * watt(P))

def from_QV(Q: coulomb, V: volt) -> joule:
    """Get energy in joules from electric charge in coulombs and voltage in volts."""
    return joule(coulomb(Q) * volt(V))

def from_IU(I: ampere, U: weber) -> joule:
    """Get energy in joules from current in amperes and magnetic flux in webers."""
    return joule(ampere(I) * weber(U))

@overload
def get_energy(*, t: second, P: watt) -> joule: ...
@overload
def get_energy(*, Q: coulomb, V: volt) -> joule: ...
@overload
def get_energy(*, I: ampere, U: weber) -> joule: ...
def get_energy(**kwargs: ElectricUnit | complex | float) -> joule:
    """Calculate the electric energy in joules based on the quantities supplied."""
    ...
