import cmath
import logging
import math
from .quantity.reactance import get_capacitive_reactance, get_inductive_reactance

from .types import *

def impedance(item: ohm | siemens | farad | henry | SupportsImpedance, frequency: hertz) -> ohm:
    """
    Coerce a component-like value to impedance at a frequency.

    Args:
        item: Resistance, admittance, capacitance, inductance, or an object with
            an ``impedance(frequency)`` method.
        frequency: Frequency at which reactive values should be evaluated.

    Returns:
        Equivalent impedance in ohms.

    Examples:
        >>> impedance(ohm(50), hertz(k=1))
        ohm(50.0)
        >>> impedance(siemens(0.02), hertz(k=1))
        ohm(50.0)
    """
    if isinstance(item, ohm):
        return item
    elif isinstance(item, siemens):
        return ohm(1/item)
    elif isinstance(item, farad):
        return get_capacitive_reactance(frequency, item)
    elif isinstance(item, henry):
        return get_inductive_reactance(frequency, item)
    return item.impedance(frequency)

def characteristic_impedance(ind: henry, cap: farad, res: ohm = ohm(0), f: hertz = hertz(0)):
    """
    Provide the characteristic line impedance (Z0) measured in ohms (Ω).

    This value is based on the positive and negative traveling voltage and current waves,
    (V+/I+) or (V-/I-).
    
    It cannot be used in tandem with conventional impedance. The characteristic impedance is
    independent from frequency, but the frequency can be used to calculate it when resistance
    is not 0.

    Args:
        ind (float): Inductance in Henrys (H)
        cap (float): Capacitance in Farads (F)
        res (float = 0): Resistance in Ohms (Ω)
        hz (float = 0): Frequency in Hertz (Hz)

    Raises:
        ValueError : Raised when both resistance and frequency are not present

    Returns:
        float : Characteristic line impedance (Z0) measured in ohms (Ω)

    Examples:
    
      >>> ind = henry(u=10)
      >>> cap = farad(p=22)
      >>> res = ohm(1000)
      >>> freq = hertz(M=100)
      >>> Z0 = characteristic_impedance(ind, cap, res, freq)
      >>> round(Z0.real, 1)
      1000.0
      
    """
    if res == 0:
        return cmath.sqrt(ind / cap)
    elif f is not None:
        omega = 1 #hertz(hz).to_angular()
        return cmath.sqrt((res + (omega * ind)) / ((1 / res) + (omega * cap)))
    raise ValueError(
        'In order to calculate the characteristic impedance, either resistance must '
        'be zero or frequency must be specified.')

def refl_coef(Z_src: ohm, Z_load: ohm) -> float:
    """
    Get the reflection coefficient Γ0 as the ratio of the reflected voltage wave to the incident voltage wave.

    For an open line, the load impedance approachs infinity and Γ0 becomes 1. The reflected
    wave returns with the same polarity as the incident voltage. For a short circuit, the load
    impedance is seen as 0Ω and Γ0 becomes -1. The reflected wave returns with an inverted
    amplituded as the incident voltage. When the load impedance and characteristic impedance match,
    Γ0 becomes 0 and no reflection is found.

    Args:
        Z_src (float): Characteristic impedance (Z0) in ohms (Ω)
        Z_load (float): Load impedance in ohms (Ω)

    Returns:
        float: The ratio of the reflected voltage wave to the incident voltage wave

    Examples:
        >>> refl_coef(ohm(50), ohm(75))
        ohm(0.2)
    """
    return (Z_load - Z_src) / (Z_load + Z_src)

def voltage_swr(R_ref: ohm, R_load: ohm) -> float:
    """
    Get the Voltage Standing Wave Ratio using the reference and load resistances.

    Args:
        R_ref (float): Reference resistance in Ohms
        R_load (float): Load resistance in Ohms

    Examples:
        >>> round(voltage_swr(ohm(50), ohm(75)), 1)
        1.5
    """
    refl = magnitude(refl_coef(R_ref, R_load))
    return ((1 + refl) / (1 - refl))

def return_loss_db(
  incident_power:watt|None=None,
  refl_power:watt|None=None,
  refl_coef:float|None=None,
  SWR:float|None=None
) -> float:
    """
    Compute the ratio of reflected power to incident power, in dB.

    Supply either incident/reflected powers, a reflection coefficient, or SWR.

    Examples:
        >>> round(return_loss_db(refl_coef=0.2), 2)
        13.98
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
    incident_power: watt | None = None,
    refl_power: watt | None = None,
    refl_coef: float | None = None,
    SWR: float | None = None
):
    """
    Ratio of transmitted power to incident power.

    .. math::
       
       Pt/Pi or (Pi-Pr)/Pi

    If an unmached circuit is connected to an RF source, reflections occur that result in a loss of
    power delivered to the circuit. Insertion loss approaches maximum (inf) in open-circuit and 
    short-circuit conditions. Insertion loss is 0 when the circuit and source are matched, as all 
    power is transferred to the circuit.

    Args:
        incident_power: Power sent toward the load.
        refl_power: Power reflected by the load.
        refl_coef: Reflection coefficient of the input.
        SWR: Voltage standing wave ratio.

    Examples:
        >>> round(insertion_loss_db(refl_coef=0.2), 3)
        0.177
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

def insertion_loss_from_power(incident_power: watt, refl_power: watt):
    """
    Ratio of transmitted power to incident power.

    .. math::
    
       Pt/Pi or (Pi-Pr)/Pi

    If an unmached circuit is connected to an RF source, reflections occur that result in a loss of
    power delivered to the circuit. Insertion loss approaches maximum (inf) in open-circuit and 
    short-circuit conditions. Insertion loss is 0 when the circuit and source are matched, as all 
    power is transferred to the circuit.
    """
    return -10.0 * math.log10((incident_power - refl_power) / incident_power)

def insertion_loss(V_src: volt, R_src: ohm, R_load: ohm) -> complex:
    """
    Compute the insertion loss when matching a source and load.

    Args:
        R_src (float): Source resistance, in Ohms
        R_load (float): Load resistance, in Ohms

    Returns:
        float:

    References:
        Hardy, J.K. (1978). High Frequency Circuit Design (pp. 67, 112).
    
    """
    return load_power(R_src, R_load) / available_power(V_src, R_load)

def to_db(cx: complex | float) -> float:
    """
    Convert a magnitude-like value to decibels.

    Examples:
        >>> to_db(10)
        20.0
    """
    return 20.0 * math.log10(magnitude(cx))

def magnitude(cx) -> float:
    """
    Return the magnitude of a real or complex value.

    Args:
        cx: Real or complex value.

    Returns:
        Absolute magnitude.

    Examples:
        >>> magnitude(3 + 4j)
        5.0
    """
    if cx == 0:
        return 0
    cx = cx + 0j
    return math.sqrt((cx.real**2) + (cx.imag**2))

def hz_center_from_bw(lower: hertz, upper: hertz) -> hertz:
    """
    Center frequency of a given lower and upper bound, based on the geometric mean.

    Args:
        lower (float): Lower frequency in Hertz (Hz)
        upper (float): Upper frequency in Hertz (Hz)

    Returns:
        float: Geometric center frequency in Hertz (Hz)

    Examples:
        >>> hz_center_from_bw(hertz(M=1), hertz(M=4))
        hertz(2000000.0)
    """
    return hertz(math.sqrt(hertz(lower).real * hertz(upper).real))

def attenuation_factor(cx) -> float:
    """
    Attenuation factor in decibels(dB) from complex input (x+yj).

    Args:
        cx (float | complex): Complex number representing the response from H(ω)

    Returns:
        float : Attenuation factor in dB

    Examples:
        >>> attenuation_factor(100)
        20.0
    
    References:
        Ludwig, R. (2000). RF Circuit Design (p. 208).
    """
    return 10.0 * math.log10(magnitude(cx))

def rc_filter_cutoff(RS: ohm, RL: ohm, C: farad) -> hertz:
    """
    Determine the 3-dB cutoff for a RC filter with the given parameters.

        [RS]---+----+
               |    |
              [C]  [RL]
               |    |
               G    G

    > The 3-dB point occurs when the reactance of the capacitor is equal to
    the parallel combination of the source and load resistances.

    Args:
        RS: Source resistance.
        RL: Load resistance.
        C: Shunt capacitance.

    Examples:
        >>> str(rc_filter_cutoff(ohm(k=1), ohm(k=1), farad(n=100)))
        '3.2kHz'

    References:
        Hardy, J.K. (1978). Filters. High frequency circuit design (pp. 99-101).
             Reston Publishing, LLC.
    """
    return hertz(1.0 / (2 * math.pi * (RS|RL) * C))

def voltage_gain(V1: volt, Z1: ohm, V2: volt, Z2: ohm) -> float:
    """
    Compute voltage gain between two voltage/impedance references.

    Examples:
        >>> voltage_gain(volt(2), ohm(50), volt(1), ohm(50))
        (2+0j)
    """
    return (V1 * cmath.sqrt(Z2)) / (V2 * cmath.sqrt(Z1))

def voltage_gain_db(V1: volt, Z1: ohm, V2: volt, Z2: ohm):
    """Return voltage gain in dB between two voltage/impedance references."""
    return 10.0 * cmath.log10(voltage_gain(V1, Z1, V2, Z2)**2)

def voltage_phase(V1: volt, Z1: ohm, V2: volt, Z2: ohm):
    """Return the phase angle of voltage gain between two references."""
    return phase(voltage_gain(V1, Z1, V2, Z2))

def complex_power(V, I):
    """Return complex power from voltage and current."""
    return V * I * cmath.cos(phase(V) - phase(I))

def power_gain_db(V1, I1, V2, I2):
    """Return power gain in dB between two voltage/current references."""
    return 10.0 * math.log10(complex_power(V1, I1) / complex_power(V2, I2))

def transducer_gain(v_src: volt, z_src: ohm, v_load: volt, z_load: ohm) -> complex:
    """
    Return transducer gain from source/load voltage and impedance.

    References:
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    """
    return ((v_load**2) / z_load) * ((4.0 * z_src) / (v_src**2))

# def transducer_gain_db(v_src:volt, z_src:ohm, v_load:volt, z_load:ohm):
#     """

#     References:
#         Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
#     """
#     gain_factor = transducer_gain(v_src, z_src, v_load, z_load)
#     return 10.0 * math.log10(magnitude(gain_factor))

def available_power(V_in: volt, R_src: ohm) -> watt:
    """
    Get the available power that can be delivered by a voltage source.

    Args:
        V_in: Source voltage.
        R_src: Source resistance.

    Examples:
        >>> available_power(volt(10), ohm(50))
        watt(0.5)
     
    References:
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    """
    return watt((V_in**2.0) / (4.0 * R_src))

def load_power(R_src: ohm, R_load: ohm) -> watt:
    """
    For a given source resistance and load resistance, compute the power applied to a load.

    Ref: Hayward, W.H. (1982). Introduction to Radio Frequency Design(p. 19).

    Args:
        R_src: Source resistance.
        R_load: Load resistance.

    Returns:
        The power applied to the load, in watts.
    """
    return watt(4.0 * R_src * R_load)

def efficiency_in_db(P1=None, P2=None, V1=None, V2=None, I1=None, I2=None, Z1=None, Z2=None):
    # if P1 is not None and P2 is not None:
    #     return 10 * math.log10(P1 / float(P2))
    # elif V1 is not None and V2 is not None:
    #     if Z1 != Z2:
    #         return 20 * math.log10((N1 * math.sqrt(Z2)) / (N2 * math.sqrt(Z1)))
    #     else:
    #         return 20 * math.log10(V1 / float(V2))
    # elif I1 is not None and I2 is not None:
    #     if Z1 != Z2:
    #         return 20 * math.log10((N1 * math.sqrt(Z1)) / (N2 * math.sqrt(Z2)))
    #     else:
    #         return 20 * math.log10(I1 / I2)
    raise ValueError("")

def phase(cx: complex | float, deg: bool = True) -> float:
    """
    Return the phase angle of a real or complex value.

    Args:
        cx: Real or complex input.
        deg: Return degrees when true; radians when false.

    Returns:
        Phase angle.

    Examples:
        >>> phase(1 + 1j)
        45.0
    """
    if deg:
        if cx.real == 0:
            return 90
        return math.degrees(math.atan(cx.imag / cx.real))
    if cx.real == 0:
        return 1.6
    return math.atan(cx.imag / cx.real)

def phase_angle(cx: complex, deg: bool = True) -> float:
    """
    Given a complex input (x+yj), determine the phase angle.

    Args:
        cx (complex): Complex number representing the response from H(ω)
        deg: Return degrees when true; radians when false.

    Returns:
        Phase angle.

    Examples:
        >>> phase_angle(1 + 1j)
        45.0
    """
    result = math.atan(cx.imag / cx.real) if cx.real != 0 else 0
    if deg:
        return math.degrees(result)
    return result
