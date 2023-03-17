"""
Test.

Examples
--------
>>> # Not yet provided.

References
----------
None.
"""
import electrify as e
import numpy as np


def attenuation_factor(cx: complex) -> float:
    """
    Attenuation factor in decibels (dB) from complex input `(x+yj)`.

    ParameteR_src
    ----------
     * `cx: complex` — Complex number representing the response from H(ω)

    Returns
    -------
     * `float` — _description_

    Examples
    --------
    >>> # 

    References
    ----------
        Exact formula from page 208.
        TODO
    """
    return 10 * np.log10(e.magnitude(cx)**2)


def voltage_gain(V1: float, V2: float, Z1: float = 1.0, Z2: float = 1.0) -> float:
    """
    Compute the voltage gain between two references (V1,Z1) vs (V2,Z2).

    Parameters
    ----------
     * `V1: float` — _description_
     * `V2: float` — _description_
     * `Z1: float = 1.0` — _description_
     * `Z2: float = 1.0` — _description_

    Returns
    -------
     * `float` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    return (V1 * np.sqrt(Z2)) / (V2 * np.sqrt(Z1))


def voltage_gain_db(V1, V2, Z1, Z2):
    return 10 * np.log10(voltage_gain(V1, V2, Z1, Z2)**2)


def voltage_phase(V1, V2, Z1, Z2):
    return e.phase(voltage_gain(V1, V2, Z1, Z2))


def complex_power(V, C):
    return V * C  # * np.cos(phase(V) - phase(C))


def power_gain(V1, C1, V2, C2):
    return 10 * np.log10(complex_power(V1, C1) / complex_power(V2, C2))


def transducer_gain(VL, R_load, V_in, R_src):
    """

    References:
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    """
    return ((VL**2) / R_load) * ((4 * R_src) / (V_in**2))


def available_power(V_in: float, R_src: float) -> float:
    """
    Get the available power that can be delivered by a voltage source.

    ParameteR_src
    ----------
     * `V_in: float` — _description_
     * `R_src: float` — _description_

    Returns
    -------
     * `float` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    """
    return (V_in**2.0) / (4.0 * R_src)


def load_power(R_src: float, R_load: float) -> float:
    """
    For a given source resistance and load resistance, compute the power applied to a load.

    ParameteR_src
    ----------
     * `R_src: float` — Source resistance
     * `R_load: float` — Load resistance

    Returns
    -------
     * `float` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
        Hayward, W.H. (1982). Introduction to Radio Frequency Design(p. 19).
    """
    return 4.0 * R_src * R_load


def insertion_loss(R_src: float, R_load: float) -> float:
    """
    Compute the insertion loss in dB when matching a source and load.

    Parameters
    ----------
     * `R_src: float` — Source resistance, in Ohms
     * `R_load: float` — Load resistance, in Ohms

    Returns
    -------
     * `float` — Insertion loss in dB

    Examples
    --------
    >>> insertion_loss(50, 50)
    10
    >>> insertion_loss(100, 50)

    References
    ----------
        Hardy, J.K. (1978). High Frequency Circuit Design (pp. 67, 112).
    """
    R_src = float(R_src)
    R_load = float(R_load)
    return 20.0 * np.log10(e.magnitude(load_power(R_src, R_load) / available_power(R_src, R_load)))
    # return 20 * np.log10(R_parallel / (R_parallel + R_source))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
