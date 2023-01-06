from ..value.unit import *
from .quantity import Quantity


Q = charge = Quantity[coulomb]("Q", "charge")


@Q.solution
def Q_from_tI(t: second, I: ampere) -> coulomb:
    """Get electric charge in coulombs from time in seconds and current in amperes."""
    return coulomb(second(t) * ampere(I))


@Q.solution
def Q_from_CV(C: farad, V: volt) -> coulomb:
    """Get electric charge in coulombs from capacitance in farads and voltage in volts."""
    return coulomb(farad(C) * volt(V))


@Q.solution
def Q_from_EV(E: joule, V: volt) -> coulomb:
    """Get electric charge in coulombs from energy in joules and voltage in volts."""
    return coulomb(joule(E) / volt(V))


@Q.solution
def Q_from_RU(R: ohm, U: weber) -> coulomb:
    """Get electric charge in coulombs from resistance in ohms and magnetic flux in webers."""
    return coulomb(weber(U) / ohm(R))
