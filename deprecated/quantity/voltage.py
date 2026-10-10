from typing import overload
from ..value.unit import *
from .quantity import Quantity

V = voltage = Quantity[volt]("V", "voltage")


@V.solution
def from_IR(I: ampere, R: ohm) -> volt:
    """Get voltage in volts from current in amps and resistance in ohms."""
    return volt(ampere(I) * ohm(R))


@V.solution
def from_CQ(C: farad, Q: coulomb) -> volt:
    """Get voltage in volts from capacitance in farads and charge in coulombs."""
    return volt(coulomb(Q) / farad(C))


@V.solution
def from_EQ(E: joule, Q: coulomb) -> volt:
    """Get voltage in volts from energy in joules and charge in coulombs."""
    return volt(joule(E) / coulomb(Q))


@V.solution
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


def get_voltage(**kwargs: base_unit | complex | float) -> volt:
    """Calculate the voltage in volts based on the quantities supplied."""
    return V.get(**kwargs)


# @V.register_solver
# def V_from_tU(t: second, U: weber) -> volt:
#     """Get voltage in volts from time in seconds and magnetic flux in webers."""
#     return volt(weber(U) / second(t))

