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


# @V.register_solver
# def V_from_tU(t: second, U: weber) -> volt:
#     """Get voltage in volts from time in seconds and magnetic flux in webers."""
#     return volt(weber(U) / second(t))


# def voltage_divider(V_in: volt | float, R1: ohm | float, R2: ohm | float) -> volt:
#     """
#     Given two resistance values in Ohms, return the divided voltage.

#     It follows this topology:
#     ```
#     [V]---[ R1]
#             |
#             +---> result
#             |
#           [ R2]
#             |
#           [GND]
#     ```

#     Parameters
#     ----------
#      * `V_in: V` -- Input voltage
#      * `R1: R` -- Series resistance, in Ohms (Ω)
#      * `R2: R` -- Shunt resistance, in Ohms (Ω)

#     Returns
#     -------
#      * `Volt` -- Output in volts

#     Examples
#     --------
#     >>> # Not yet provided.

#     """
#     if math.isinf(R2) or R2 is None:
#         return volt(V_in)
#     if R2 == SHORT_CIRCUIT:
#         return volt(SHORT_CIRCUIT)
#     if R1 == SHORT_CIRCUIT or R1 is None:
#         return volt(V_in)
#     if R1 == OPEN_CIRCUIT:
#         return volt(OPEN_CIRCUIT)
#     return volt(V_in * (R2 / (R2 + R1)))
