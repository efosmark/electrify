from typing import overload
from ..types import *
from .quantity import Quantity

def from_IR(I: ampere, R: ohm) -> volt:
    """Get voltage in volts from current in amps and resistance in ohms."""
    return volt(ampere(I) * ohm(R))

def from_CQ(C: farad, Q: coulomb) -> volt:
    """Get voltage in volts from capacitance in farads and charge in coulombs."""
    return volt(coulomb(Q) / farad(C))

def from_EQ(E: joule, Q: coulomb) -> volt:
    """Get voltage in volts from energy in joules and charge in coulombs."""
    return volt(joule(E) / coulomb(Q))

def from_IP(I: ampere, P: watt) -> volt:
    """Get voltage in volts from current in amperes and power in watts."""
    return volt(watt(P) / ampere(I))

@overload
def get_voltage(*, I: ampere, R: ohm) -> volt: ...
@overload
def get_voltage(*, C: farad, Q: coulomb) -> volt: ...
@overload
def get_voltage(*, E: joule, Q: coulomb) -> volt: ...
@overload
def get_voltage(*, I: ampere, P: watt) -> volt: ...
def get_voltage(**kwargs: ElectricUnit | complex | float) -> volt:
    """Calculate the voltage in volts based on the quantities supplied."""
    ...


# @V.register_solver
# def V_from_tU(t: second, U: weber) -> volt:
#     """Get voltage in volts from time in seconds and magnetic flux in webers."""
#     return volt(weber(U) / second(t))
