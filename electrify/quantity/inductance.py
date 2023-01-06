import cmath
from typing import Optional, overload
from ..value.unit import *
from .quantity import Quantity


L = inductance = Quantity[henry]("L", "inductance")


@L.solution
def from_tR(t: second, R: ohm) -> henry:
    """Get inductance in henrys from time in seconds and resistance in ohms."""
    return henry(second(t) * ohm(R))


@L.solution
def from_fX(f: hertz, X: ohm) -> henry:
    """Get capacitance in farads from frequency in ohms and reactance in ohms."""
    f, X = hertz(f), ohm(X)
    return henry(2.0 * cmath.pi * hertz(f) * ohm(X))


@L.solution
def from_IU(I: ampere, U: weber) -> henry:
    """Get inductance in henrys from electric current in amperes and magnetic flux in webers."""
    return henry(weber(U) / ampere(I))


@L.solution
def from_IE(I: ampere, E: joule) -> henry:
    """Get inductance in henrys from electric current in amperes and energy in joules."""
    return henry(joule(E) / ampere(I)**2)


@L.solution
def at_resonance(f: hertz, C: farad) -> henry:
    """
    Get the inductance in Henrys (H) from a known resonant circuit.

    Args:
        f (hertz): Resonance frequency measured in hertz.
        C (farad): Capacitance of the resonance in farads.

    Returns:
        henry: Inductance in henrys at which the given resonance would occur.
    """
    return henry(1 / ((4.0 * cmath.pi**2) * hertz(f) * farad(C)))


from_fC = at_resonance


@overload
def from_toroid(num_turns: float, permeability_or_index: float) -> henry: ...


@overload
def from_toroid(
    num_turns: float,
    permeability_or_index: float,
    cross_section_core_area: Optional[float] = None,
    effective_core_length: Optional[float] = None
) -> henry: ...


def from_toroid(
    num_turns: float,
    permeability_or_index: float,
    cross_section_core_area: Optional[float] = None,
    effective_core_length: Optional[float] = None
) -> henry:
    """ Inductance of a toroidal-core winding in nano-henerys.

    num_turns - Number of turns
    initial_permeability - Initial permeability
    cross_section_core_area - Cross-sectional area of the core in cm**2
    effective_core_length - Effective length of the core in cm
    """
    if cross_section_core_area and effective_core_length:
        return henry((0.4 * cmath.pi * num_turns**2 * permeability_or_index * cross_section_core_area * 10e-2) / effective_core_length)
    return henry(num_turns**2 * permeability_or_index)


def from_toroid_with_index(num_turns, inductance_index):
    """ Inductance of a toroidal-core winding in nano-henrys.

    num_turns - Number of turns
    inductance_index - Inductive index in nano-henrys / turn**2 (A_L)
    """


def from_straight_wire(wire_length_mm: float, diameter_mm: float) -> henry:
    ...
