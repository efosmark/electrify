"""
Contains functions around values related to capacitance.

Examples
--------
>>> # Not yet provided.

"""
import cmath
from ..value.unit import *
from .quantity import Quantity
from ..constants import OPEN_CIRCUIT
from ..value.unit import *


C = capacitance = Quantity[farad]("C", "capacitance")


@C.solution
def from_QV(Q: coulomb, V: volt) -> farad:
    """Get capacitance in farads from electric charge in coulombs and voltage in volts."""
    return farad(coulomb(Q) / volt(V))


@C.solution
def from_tR(t: second, R: ohm) -> farad:
    """Get capacitance in farads from time in seconds and resistance in ohms."""
    return farad(second(t) / ohm(R))


@C.solution
def from_fX(f: hertz, X: ohm) -> farad:
    """Get capacitance in farads from frequency in ohms and capacitive reactance in ohms."""
    return farad(1.0 / (2.0 * cmath.pi * hertz(f) * abs(ohm(X))))


@C.solution
def from_EQ(E: joule, Q: coulomb) -> farad:
    """Get capacitance in farads from energy in joules and electric charge in coulombs."""
    return farad(coulomb(Q)**2.0 / joule(E))


@C.solution
def from_EV(E: joule, V: volt) -> farad:
    """Get capacitance in farads from energy in joules and voltage in volts."""
    return farad(joule(E) / volt(V)**2.0)


def capacitive_reactance(freq: hertz | float, cap: farad | float) -> ohm:
    """
    Provide the reactance d (X) in ohms (Ω) at a given frequency for a given capacitance.

    Capacitive reactance, by definition, will always be a negative number.

    Parameters
    ----------
    * `freq`:`Hz` — Frequency in Hertz (Hz)
    * `cap`:`F` — Capacitance in Farads (F)

    Raises
    ------
    * `ValueError` — Raised when a negative frequency is supplied.

    Returns
    -------
    * `Ohm` — The reactance (X) in ohms (Ω) at a given frequency for a given capacitance

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    if freq < 0:
        raise ValueError('Frequency must be a positive number. Received: "{}"'.format(freq))
    if freq == 0:
        return ohm(-OPEN_CIRCUIT)
    if cap == 0:
        return ohm(0)
    return ohm(-1.0 / (2.0 * cmath.pi * freq * cap))


def capacitance_from_reactance(freq: hertz, reactance: ohm | float) -> farad:
    """
    Given a frequency (Hz) and reactance (X), provide the capacitance in Farads (F).

    Parameters
    ----------
     * `freq`:`Hz` — Frequency in Hertz (Hz)
     * `reactance`:`X` — Capacitive reactance in ohms (Ω)

    Notes
    -----
    This behaves the same whether or not this value is negative.

    Raises
    ------
     * `ValueError` — Raised when a negative frequency is supplied

    Returns
    -------
     * `F` — Capacitance in Farads (F)

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    if freq <= 0:
        raise ValueError('Frequency must be a positive number. Received: "{}"'.format(freq))
    if reactance == 0:
        return farad(0)
    return farad(abs(1 / (2 * cmath.pi * freq * abs(reactance))))
