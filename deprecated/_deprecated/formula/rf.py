"""
Summaried.

Examples
--------
>>> # Not yet implemented

References
----------
None.

"""
import math
from ..value.unit import hertz, RadPerSecond



# TODO: Is this needed? We can use base_unit.magnitude
def magnitude(cx: complex | float) -> float:
    """
    For a given complex number in the form x+jy, calculate the magnitude by using the Pythagorean Theorem.

    Args:
        cx (complex | float): Complex input, where the real number represents x, and the imaginary form represents y

    Returns:
     * `float` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    if cx == 0:
        return 0
    cx = cx + 0j
    return math.sqrt((cx.real**2) + (cx.imag**2))


def att_factor_db(cx: float | complex) -> float:
    """
    Attenuation factor in decibels(dB) from complex input(x+yj).

    Args:
        cx (float | complex): Complex number representing the response from H(ω)

    Returns:
     * `float` — Attenuation factor in dB

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
        Ludwig, R. (2000). RF Circuit Design (p. 208).
    """
    return 10 * math.log10(magnitude(cx)**2)


def characteristic_impedance(ind: float, cap: float, res: float = 0, hz: float = 0) -> float:
    """
    Provide the characteristic line impedance (Z0) measured in ohms (Ω).

    This value is based on the positive and negative traveling voltage and current waves,
    (V+/I+) or (V-/I-).

    Args:
        ind (float): Inductance in Henrys (H)
        cap (float): Capacitance in Farads (F)
        res (float = 0): Resistance in Ohms (Ω)
        hz (float = 0): Frequency in Hertz (Hz)

    Notes
    -----
    It cannot be used in tandem with conventional impedance. The characteristic impedance is
    independent from frequency, but the frequency can be used to calculate it when resistance
    is not 0.

    Raises
    ------
     * `ValueError` — Raised when both resistance and frequency are not present

    Returns:
     * `float` — Characteristic line impedance (Z0) measured in ohms (Ω)

    Examples
    --------
    >>> import electrify as ee
    >>> ind = ee.micro(10)
    >>> cap = ee.pico(22)
    >>> res = 1e3
    >>> freq = ee.mega(100)
    >>> Z0 = characteristic_impedance(ind, cap, res, freq)
    122

    References
    ----------
    None.
    """
    if res == 0:
        return math.sqrt(ind / cap)
    elif hz is not None:
        omega = hertz(hz).to_angular()
        return math.sqrt((res + (omega * ind)) / ((1 / res) + (omega * cap)))
    raise ValueError(
        'In order to calculate the characteristic impedance, either resistance must '
        'be zero or frequency must be specified.')


def refl_coef(Z_src: float, Z_load: float) -> float:
    """
    Get the reflection coefficient Γ0 as the ratio of the reflected voltage wave to the incident voltage wave.

    For an open line, the load impedance approachs infinity and Γ0 becomes 1. The reflected
    wave returns with the same polarity as the incident voltage. For a short circuit, the load
    impedance is seen as 0Ω and Γ0 becomes -1. The reflected wave returns with an inverted
    amplituded as the incident voltage. When the load impedance and characteristic impedance match,
    Γ0 becomes 0 and no reflection is found.

    Args:
     * `Z_src: float` — Characteristic impedance (Z0) in ohms (Ω)
     * `Z_load: float` — Load impedance in ohms (Ω)

    Returns:
     * `float` — The ratio of the reflected voltage wave to the incident voltage wave

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    return (Z_load - Z_src) / (Z_load + Z_src)


def voltage_swr(R_ref: float, R_load: float) -> float:
    """
    Get the Voltage Standing Wave Ratio using the reference and load resistances.

    Args:
     * `R_ref: float` — Reference resistance in Ohms
     * `R_load: float` — Load resistance in Ohms

    Returns:
     * `float` — Voltage standing wave ratio (unitless)

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    refl = magnitude(refl_coef(R_ref, R_load))
    return ((1 + refl) / (1 - refl))


def return_loss_db(incident_power=None, refl_power=None, refl_coef=None, SWR=None):
    """
    Compute the ratio of reflected power to incident power, in dB.

    Args:
    incident_power :
    refl_power :
    refl_coef :
    SWR :

    References
    ----------
    i
    """
    if incident_power is not None and refl_power is not None:
        return -10 * math.log10(refl_power / incident_power)
    elif refl_coef is not None:
        return -20 * math.log10(abs(refl_coef))
    elif SWR is not None:
        return -20 * math.log10((SWR + 1) / (SWR - 1))
    raise ValueError('return_loss_db requires providing either (incident_power & refl_power),'
                     ' or refl_coef, or SWR.')


def insertion_loss_db(
    incident_power: float | None = None,
    refl_power: float | None = None,
    refl_coef: float | None = None,
    SWR: float | None = None
):
    """
    Ratio of transmitted power to incident power.

    Pt/Pi or (Pi-Pr)/Pi

    If an unmached circuit is connected to an RF source, reflections occur that result in a loss of
    power delivered to the circuit. Insertion loss approaches maximum (inf) in open-circuit and 
    short-circuit conditions. Insertion loss is 0 when the circuit and source are matched, as all 
    power is transferred to the circuit.

    Args:
     * `incident_power: _type_ = None` — _description_
     * `refl_power: _type_ = None` — _description_
     * `refl_coef: _type_ = None` — Reflection coefficient of the input
     * `SWR: _type_ = None` — _description_

    Raises
    ------
     * `ValueError` — _description_

    Returns:
     * `_type_` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    if incident_power is not None and refl_power is not None:
        return -10 * math.log10((incident_power - refl_power) / incident_power)
    elif refl_coef is not None:
        return - 10 * math.log10(1 - abs(refl_coef)**2)
    elif SWR is not None and SWR > 0:
        return 20 * math.log10((SWR + 1) * (2 * math.sqrt(SWR)))
    raise ValueError(
        'insertion_loss_db requires providing either (incident_power & refl_power),'
        ' or refl_coef, or SWR.'
    )


def insertion_loss_from_power(incident_power: float, refl_power: float):
    """
    Ratio of transmitted power to incident power.

    Pt/Pi or (Pi-Pr)/Pi

    If an unmached circuit is connected to an RF source, reflections occur that result in a loss of
    power delivered to the circuit. Insertion loss approaches maximum (inf) in open-circuit and 
    short-circuit conditions. Insertion loss is 0 when the circuit and source are matched, as all 
    power is transferred to the circuit.

    Args:
     * `incident_power: _type_ = None` — _description_
     * `refl_power: _type_ = None` — _description_
     * `refl_coef: _type_ = None` — Reflection coefficient of the input
     * `SWR: _type_ = None` — _description_

    Raises
    ------
     * `ValueError` — _description_

    Returns:
     * `_type_` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    return -10 * math.log10((incident_power - refl_power) / incident_power)


# def hz_center_from_bw(lower: float, upper: float) -> float:
#     """
#     Center frequency of a given lower and upper bound, based on the geometric mean.

#     Parameters
#     ----------
#        lower (float): Lower frequency in Hertz (Hz)
#        upper (float): Upper frequency in Hertz (Hz)

#     Returns
#     -------
#      * `float` — Geometric center frequency in Hertz (Hz)

#     Examples
#     --------
#     >>> # Not yet provided.

#     References
#     ----------
#     None.
#     """
#     return math.sqrt(lower * upper)


# def efficiency_in_db(P1=None, P2=None, V1=None, V2=None, I1=None, I2=None, Z1=None, Z2=None):
#     if P1 is not None and P2 is not None:
#         return 10 * np.log10(P1 / float(P2))
#     elif V1 is not None and V2 is not None:
#         if Z1 != Z2:
#             return 20 * np.log10((N1 * np.sqrt(Z2)) / (N2 * np.sqrt(Z1)))
#         else:
#             return 20 * np.log10(V1 / float(V2))
#     elif I1 is not None and I2 is not None:
#         if Z1 != Z2:
#             return 20 * np.log10((N1 * np.sqrt(Z1)) / (N2 * np.sqrt(Z2)))
#         else:
#             return 20 * np.log10(I1 / I2)
#     raise ValueError("")


def phase(cx: complex | float, deg: bool = False) -> float:
    """
    _summary_

    Args:
        cx (complex | float): _description_
        deg (bool = False): _description_

    Returns:
     * `float` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    if deg:
        if cx.real == 0:
            return 90
        return np.degrees(np.arctan(cx.imag / cx.real))
    if cx.real == 0:
        return 1.6
    return np.arctan(cx.imag / cx.real)


def phase_angle(cx: complex, deg: bool = True) -> float:
    """
    Given a complex input (x+yj), determine the phase angle.

    Args:
        cx (complex): Complex number representing the response from H(ω)
        deg (bool = True): _description_

    Returns:
     * `float` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    result = np.arctan(cx.imag / cx.real) if cx.real != 0 else 0
    if deg:
        return np.degrees(result)
    return result
