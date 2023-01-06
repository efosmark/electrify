import cmath
from typing import Optional
from ..value.unit import *
from .quantity import Quantity

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
