import math, cmath

from electrify.util import logfunc

from .constants import BOLTZMANN_CONSTANT, ELEMENTARY_CHARGE
from .value.unit import *
from .quantity.reactance import get_capacitive_reactance, get_inductive_reactance

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def attenuation_factor(cx: complex) -> float:
    """
    Attenuation factor in decibels (dB) from complex input `(x+yj)`.

    Args:
        cx (complex): Complex number representing the response from H(ω)

    """
    return 10 * cmath.log10(cx**2)


#@logfunc(logger)
def current_divider(current: ampere, Z_branch: ohm, Z_total: ohm) -> ampere:
    """
    Given a current at a branch, determine how much of it will go to a branch.

    Args:
        current (ampere): _description_
        Z_branch (ohm): _description_
        Z_total (ohm): _description_

    Returns:
        ampere: _description_
    """
    if Z_branch == 0:
        return current
    return ampere(complex(current) * (Z_total / Z_branch))


#@logfunc(logger)
def voltage_divider(V_in: volt | float, R1: ohm | float, R2: ohm | float) -> volt:
    """
    Given two resistance values in Ohms, return the divided voltage.

    It follows this topology:
    ```
    [V]---[ R1]
            |
            +---> result
            |
          [ R2]
            |
          [GND]
    ```

    Parameters
    ----------
     * `V_in: V` -- Input voltage
     * `R1: R` -- Series resistance, in Ohms (Ω)
     * `R2: R` -- Shunt resistance, in Ohms (Ω)

    Returns
    -------
     * `Volt` -- Output in volts

    Examples
    --------
    >>> # Not yet provided.

    """
    if cmath.isinf(R2) or R2 is None:
        return volt(V_in)
    if R2 == 0:
        return volt(0)
    if R1 == 0:
        return volt(V_in)
    if cmath.isinf(R1):
        return volt(0)
    #logger.debug('(R2 + R1)  ' + str((R2 + R1)))
    #logger.debug('(R2 / (R2 + R1))  ' + str((R2 / (R2 + R1))))
    #cmath.
    
    R2 = magnitude(R2)
    R1 = magnitude(R1)
    return volt(complex(V_in) * (R2 / (R2 + R1)))


def get_item_impedance(item, frequency: hertz) -> ohm:
    if isinstance(item, ohm):
        return item
    elif isinstance(item, farad):
        return get_capacitive_reactance(frequency, item)
    elif isinstance(item, henry):
        return get_inductive_reactance(frequency, item)
    return ohm(0 + 0j)


def rc_filter_cutoff(RS: float, RL: float, C: float) -> float:
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
        RS (float): _description_
        RL (float): _description_
        C (float): _description_

    References:
        Hardy, J.K. (1978). Filters. High frequency circuit design (pp. 99-101).
             Reston Publishing, LLC.
    """
    R = 1 #parallel_resistance([RS, RL])
    return 1.0 / (2 * math.pi * R * C)


def voltage_gain(V1: float, V2: float, Z1: float = 1.0, Z2: float = 1.0) -> complex:
    """
    Compute the voltage gain between two references (V1,Z1) vs (V2,Z2).

    """
    return (V1 * cmath.sqrt(Z2)) / (V2 * cmath.sqrt(Z1))


def voltage_gain_db(V1, V2, Z1, Z2):
    return 10 * cmath.log10(voltage_gain(V1, V2, Z1, Z2)**2)


def voltage_phase(V1, V2, Z1, Z2):
    return phase(voltage_gain(V1, V2, Z1, Z2))


def complex_power(V, C):
    return V * C  # * np.cos(phase(V) - phase(C))


def power_gain(V1, C1, V2, C2):
    return 10 * cmath.log10(complex_power(V1, C1) / complex_power(V2, C2))


def transducer_gain(VL, R_load, V_in, R_src):
    """

    References:
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    """
    return ((VL**2) / R_load) * ((4 * R_src) / (V_in**2))


def available_power(V_in: float, R_src: float) -> float:
    """
    Get the available power that can be delivered by a voltage source.

    Args:
        V_in (float): _description_
        R_src (float): _description_
     
    References:
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    """
    return (V_in**2.0) / (4.0 * R_src)


def load_power(R_src: float, R_load: float) -> float:
  """
    For a given source resistance and load resistance, compute the power applied to a load.

    Ref: Hayward, W.H. (1982). Introduction to Radio Frequency Design(p. 19).

  Args:
      R_src (float): Source resistance
      R_load (float): Load resistance

  Returns:
      float: The power applied to the load, in watts
  """
  return 4.0 * R_src * R_load


def insertion_loss(R_src: float, R_load: float) -> float:
    """
    Compute the insertion loss in dB when matching a source and load.

    Ref: Hardy, J.K. (1978). High Frequency Circuit Design (pp. 67, 112).

    Args:
        R_src (float): Source resistance, in Ohms
        R_load (float): Load resistance, in Ohms

    Returns:
        float: Insertion loss in dB

    Examples:
    
        >>> insertion_loss(50, 50)
        10
        >>> insertion_loss(100, 50)
    
    """
    R_src = float(R_src)
    R_load = float(R_load)
    return 20.0 * math.log10(magnitude(load_power(R_src, R_load) / available_power(R_src, R_load)))

def magnitude(cx: complex | float) -> float:
  """
  For a given complex number in the form (X+jY), calculate the magnitude via the 
  Pythagorean Theorem.

  Args:
      cx (complex | float): Complex input (X+jY)

  Returns:
      float: _description_
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
        float : Attenuation factor in dB
    
    References:
        Ludwig, R. (2000). RF Circuit Design (p. 208).
    """
    return 10.0 * math.log10(magnitude(cx)**2)


def characteristic_impedance(ind: float, cap: float, res: float = 0, hz: float = 0) -> float:
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
    
      >>> import electrify as ee
      >>> ind = ee.micro(10)
      >>> cap = ee.pico(22)
      >>> res = 1e3
      >>> freq = ee.mega(100)
      >>> Z0 = characteristic_impedance(ind, cap, res, freq)
      122
      
    """
    if res == 0:
        return math.sqrt(ind / cap)
    elif hz is not None:
        omega = 1 #hertz(hz).to_angular()
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
        Z_src (float): Characteristic impedance (Z0) in ohms (Ω)
        Z_load (float): Load impedance in ohms (Ω)

    Returns:
        float: The ratio of the reflected voltage wave to the incident voltage wave

    """
    return (Z_load - Z_src) / (Z_load + Z_src)


def voltage_swr(R_ref: float, R_load: float) -> float:
    """
    Get the Voltage Standing Wave Ratio using the reference and load resistances.

    Args:
        R_ref (float): Reference resistance in Ohms
        R_load (float): Load resistance in Ohms

    """
    refl = magnitude(refl_coef(R_ref, R_load))
    return ((1 + refl) / (1 - refl))


def return_loss_db(
  incident_power=None,
  refl_power=None,
  refl_coef=None,
  SWR=None
):
    """
    Compute the ratio of reflected power to incident power, in dB.

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

    .. math::
       
       Pt/Pi or (Pi-Pr)/Pi

    If an unmached circuit is connected to an RF source, reflections occur that result in a loss of
    power delivered to the circuit. Insertion loss approaches maximum (inf) in open-circuit and 
    short-circuit conditions. Insertion loss is 0 when the circuit and source are matched, as all 
    power is transferred to the circuit.

    Args:
        incident_power (_type_ = None): _description_
        refl_power (_type_ = None): _description_
        refl_coef (_type_ = None): Reflection coefficient of the input
        SWR (_type_ = None): _description_
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

    .. math::
    
       Pt/Pi or (Pi-Pr)/Pi

    If an unmached circuit is connected to an RF source, reflections occur that result in a loss of
    power delivered to the circuit. Insertion loss approaches maximum (inf) in open-circuit and 
    short-circuit conditions. Insertion loss is 0 when the circuit and source are matched, as all 
    power is transferred to the circuit.
    """
    return -10 * math.log10((incident_power - refl_power) / incident_power)


def hz_center_from_bw(lower: float, upper: float) -> float:
    """
    Center frequency of a given lower and upper bound, based on the geometric mean.

    Args:
        lower (float): Lower frequency in Hertz (Hz)
        upper (float): Upper frequency in Hertz (Hz)

    Returns:
        float: Geometric center frequency in Hertz (Hz)

    Examples:

        >>> # Not yet provided.
    """
    return math.sqrt(lower * upper)


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


def phase(cx: complex | float, deg: bool = False) -> float:
    """
    _summary_

    Args:
        cx (complex | float): _description_
        deg (bool = False): _description_

    Returns:
        float: _description_

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
        deg (bool = True): _description_

    Returns:
        float: _description_

    """
    result = math.atan(cx.imag / cx.real) if cx.real != 0 else 0
    if deg:
        return math.degrees(result)
    return result


def shockley_diode_equation(
  voltage: volt,
  saturation_current: ampere,
  quality_factor: float = 1.0,
  thermal_voltage: volt = volt(0.026)
  ) -> ampere:
  return ampere(
    saturation_current
    * (cmath.exp(voltage / (quality_factor * thermal_voltage)) - 1.0)
  )


def thermal_voltage(temperature: float) -> volt:
  r"""
    The characteristic voltage that describes the relationship between the flow of electric current
    and the electrostatic potential across a p-n junction.
    
    Equal approximately to ``25.852 mV`` at ``300 K``, which is often rounded to ``26mV`` at room 
    temperature in order to simplify equations.

    At an arbitrary temperature, it is a known constant:
    
    .. math::

        V_{T} = \frac{kT}{q}

    where,

      .. hlist::
         * :math:`k` is the :term:`Boltzmann constant`
         * :math:`T` is the absolute temperature of the ``p-n`` junction
         * :math:`q` isP the :term:`elementary charge`

    Args:
        temperature (float): _description_

    Returns:
        volt: _description_
    
    Examples:
      >>> d
  """
  return volt(BOLTZMANN_CONSTANT * temperature / ELEMENTARY_CHARGE)
