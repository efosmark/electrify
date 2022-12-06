"""
Contains functions around values related to capacitance.

Examples
--------
>>> # Not yet provided.

"""
import numpy as np

from .rf import magnitude
from .common import series_resistance, parallel_resistance
from ..constants import OPEN_CIRCUIT


def series_capacitance(*args) -> float:
    """
    For the given list of arguments, sum them as if they are capacitances in series.

    This is an alias for `rf.parallel_resistance`.

    Parameters
    ----------
     * `*args` — List of values that are to be summed.

    Returns
    -------
     * `float` — Summed value of all arguments as a series of capacitances.

    Examples
    --------
    >>> # Not yet provided.

    """
    return parallel_resistance(*args)


def parallel_capacitance(*args) -> float:
    """
    For the given list of arguments, sum them as if they are capacitances in parallel.

    This is an alias for `rf.series_resistance`.

    Parameters
    ----------
     * `*args` — List of values that are to be summed.

    Returns
    -------
     * `float` — Summed value of all arguments as a parallel of capacitances.

    Examples
    --------
    >>> # Not yet provided.

    """
    return series_resistance(*args)


def capacitive_reactance(freq: float, cap: float) -> float:
    """
    Provide the reactance (X) in ohms (Ω) at a given frequency for a given capacitance.

    Capacitive reactance, by definition, will always be a negative number.

    Parameters
    ----------
     * `freq`:`float` — Frequency in Hertz (Hz)
     * `cap`:`float` — Capacitance in Farads (F)

    Raises
    ------
     * `ValueError` — Raised when a negative frequency is supplied.

    Returns
    -------
     * `float` — The reactance (X) in ohms (Ω) at a given frequency for a given capacitance

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
        return -OPEN_CIRCUIT
    if cap == 0:
        return 0
    return (1 / (2 * np.pi * freq * cap)) * -1j


def capacitance_from_reactance(Hz: float, X: float) -> float:
    """
    Given a frequency (Hz) and reactance (X), provide the capacitance in Farads (F).

    Parameters
    ----------
     * `Hz`:`float` — Frequency in Hertz (Hz)
     * `X`:`float` — Capacitive reactance in ohms (Ω)

    Notes
    -----
    This behaves the same whether or not this value is negative.

    Raises
    ------
     * `ValueError` — Raised when a negative frequency is supplied

    Returns
    -------
     * `float` — Capacitance in Farads (F)

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    if Hz <= 0:
        raise ValueError('Frequency must be a positive number. Received: "{}"'.format(Hz))
    if X == 0:
        return 0
    return abs(1 / (2 * np.pi * Hz * magnitude(X)))


def capacitance_from_charge(charge: float, voltage: float) -> float:
    """
    Given a charge and a voltage, provide the capacitance in Farads (F).

    Parameters
    ----------
     * `charge`:`float` — Capacitive charge measured in Coloumbs (C)
     * `voltage`:`float` — Voltage measured in volts (V)

    Returns
    -------
     * `float` — Capacitance in Farads (F)

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    return charge / voltage


def capacitive_charge(capacitance: float, voltage: float) -> float:
    """
    Compute the charge in coulombs (C) based on the capacitance and voltage.

    Parameters
    ----------
     * `capacitance`:`float` — Capacitance in farads (F)
     * `voltage`:`float` — Voltage in volts (V)

    Returns
    -------
     * `float` — Capacitive charge, in coulombs (C)

    Examples
    --------
    >>> assert True

    References
    ----------
    None.
    """
    return capacitance * voltage


def capacitive_energy(cap: float, voltage: float) -> float:
    """
    Provide the energy stored in a capacitor in joules (J) based on the capacitance and voltage.

    Parameters
    ----------
     * `cap`:`float` — Capacitance in farads (F)
     * `voltage`:`float` — Voltage in volts (V)

    Returns
    -------
     * `float` — Energy stored in a capacitor in joules (J)

    Examples
    --------
    >>> import electrify as ee
    >>> capacitive_energy(ee.micro(10), 10)
    0.0005

    References
    ----------
    None.
    """
    return 0.5 * cap * voltage**2


if __name__ == "__main__":
    import doctest
    doctest.testmod()
