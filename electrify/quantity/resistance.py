import cmath
from typing import Optional, overload
from ..value.unit import *
from .quantity import Quantity
from ..constants import COLOR_CODES as CC

R = resistance = Quantity[ohm]("R", "resistance")
G = conductance = Quantity[siemens]("G", "conductance")


@R.solution
def R_from_IV(I: ampere, V: volt) -> ohm:
    """Get resistance in ohms from electric current in amperes and voltage in volts."""
    return ohm(volt(V) / ampere(I))


@R.solution
def R_from_tL(t: second, L: henry) -> ohm:
    return ohm(henry(L) / second(t))


@R.solution
def R_from_tC(t: second, C: farad) -> ohm:
    return ohm(second(t) / farad(C))


@R.solution
def R_from_PV(P: watt, V: volt) -> ohm:
    """Get resistance in ohms from power in watts and voltage in volts."""
    return ohm(volt(V)**2 / watt(P))


@R.solution
def R_from_IP(I: ampere, P: watt) -> ohm:
    """Get resistance in ohms from electric current in amperes and power in watts."""
    return ohm(watt(P) / ampere(I)**2)


@R.solution
def R_from_QU(Q: coulomb, U: weber) -> ohm:
    """Get resistance in ohms from electric charge in coulombs and magnetic flux in webers."""
    return ohm(weber(U) / coulomb(Q))


@R.solution
def R_from_Z(Z: ohm, phase: Optional[float] = None) -> ohm:
    """Get reactance in ohms from impedance in the form (R+Xj) in ohms."""
    if phase is not None:
        Z = ohm(cmath.rect(Z.real, phase))
    if not isinstance(Z, complex):
        raise TypeError("Z must be a complex value in the form of (R+Xj)."
                        "Otherwise, the phase angle must be supplied.")
    return ohm(Z.real)


@R.solution
def R_from_G(G: siemens) -> ohm:
    """Get resistance in ohms from conductance in siemens."""
    return ohm(1.0 / siemens(G))


@G.solution
def G_from_R(R: ohm) -> siemens:
    """Get conductance in siemens from resistance in ohms."""
    return siemens(1.0 / ohm(R))


@overload
def get_resistance(*, I: ampere, V: volt) -> ohm: ...
@overload
def get_resistance(*, P: watt, V: volt) -> ohm: ...
@overload
def get_resistance(*, I: ampere, P: watt) -> ohm: ...
@overload
def get_resistance(*, Q: coulomb, U: weber) -> ohm: ...
@overload
def get_resistance(*, Z: ohm) -> ohm: ...
@overload
def get_resistance(*, Z: ohm, phase: float) -> ohm: ...
@overload
def get_resistance(*, G: siemens) -> ohm: ...


def get_resistance(**kwargs: base_unit | complex | float) -> ohm:
    """Calculate electric resistance in ohms based on the inputted quantities."""
    return R.get(**kwargs)


@overload
def from_color_code(first: str, second: str, third: str) -> ohm: ...
@overload
def from_color_code(first: str, second: str, third: str, forth: str | None) -> ohm: ...


def from_color_code(first: str, second: str, third: str, forth: Optional[str | None] = None) -> ohm:
    """
    Create a new `Resistor` with a resistance value defined by the color codes.

    ```
        Code     Digit
        ------   ------
        black    0
        brown    1
        red      2
        orange   3
        yellow   4
        green    5
        blue     6
        violet   7
        gray     8
        white    9
        gold     0.1
        silver   0.01
    ```

    Parameters
    ----------
        * `first: str` — First color code band
        * `second: str` — Second color code band
        * `third: str` — Third color code band
        * `forth: str | None = None` — Optional forth color code band
    """
    if forth is None:
        value = (CC[first] * 10) + CC[second]
        return ohm(value * (10**CC[third]))
    value = (CC[first] * 100) + (CC[second] * 10) + CC[third]
    return ohm(value * (10**CC[forth]))
