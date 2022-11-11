from numbers import Number, Real
import numpy as np


def quality_factor(X: Number, R: Number):
    ''' Provides the quality factor (Q), AKA the figure of merit. Since Q is based on the reactance, it is frequency-dependent.
        X - reactance
        R - resistance
    '''
    if R == 0:
        return np.inf
    return X / R


def resistance_from_Q(Q: Number, X: Number) -> Number:
    '''
    '''
    if X == 0:
        return 0
    return Q / abs(X)


def magnitude(cx: Number) -> Number:
    ''' For a given complex number in the form x+jy, calculate the magnitude
    by using the Pythagorean Theorem.

    cx - Complex number input, where the real number represents x, and the imaginary form represents y.
    '''
    if cx == 0:
        return 0
    cx = cx + 0j
    return np.sqrt((cx.real**2) + (cx.imag**2))


def resonant_frequency(L: Number, C: Number) -> Number:
    return 1 / (2 * np.pi * np.sqrt(C * L))


def attenuation_factor(cx: Number) -> Number:
    # Exact formula from page 208:
    return np.multiply(-0.5, np.log10(magnitude(cx)**2))


def attenuation_factor_db(cx: Number) -> Number:
    ''' Attenuation factor in decibels (dB) from complex input (x+yj)

    cx - Complex number representing the response from H(ω)
    '''
    # Exact formula from page 208:
    return 10 * np.log10(magnitude(cx)**2)


def characteristic_impedance(inductance: Number, capacitance: Number, resistance: Number = 0, f: Real = None):
    ''' Provides the characteristic line impedance (Z0) measured in ohms (Ω).
    This value is based on the positive and negative traveling voltage and current waves, (V+/I+) or (V-/I-).
    It cannot be used in tandem with conventional impedance. The characteristic impedance is
    independent from frequency, but the frequency can be used to calculate it when resistance is not 0.

    inductance  - Inductance in henrys (H)
    capacitance - Capacitance in farads (F)
    resistance  - Resistance in ohms (Ω).  Default 0
    f           - Frequency in hertz (Hz). Default None
    '''
    if resistance == 0:
        return np.sqrt(inductance / capacitance)
    elif f is not None:
        omega = to_angular_frequency(f)
        return np.sqrt((resistance + (omega * inductance)) / ((1 / resistance) + (omega * capacitance)))
    raise ValueError(
        'In order to calculate the characteristic impedance, either resistance must be zero or frequency must be specified.')


def reflection_coefficient(source_impedance, load_impedance):
    ''' Provides the reflection coefficient Γ0 as the ratio of the reflected voltage wave to the incident voltage wave.
    For an open line, the load impedance approachs infinity and Γ0 becomes 1. The reflected wave returns with the same polarity as the incident voltage.
    For a short circuit, the load impedance is seen as 0Ω and Γ0 becomes -1. The reflected wave returns with an inverted amplituded as the incident voltage.
    When the load impedance and characteristic impedance match, Γ0 becomes 0 and no reflection is found.

    source_impedance         - Characteristic impedance (Z0) in ohms (Ω)
    load_impedance           - Load impedance ZL in ohms (Ω)
    '''
    return (load_impedance - source_impedance) / (load_impedance + source_impedance)


def VSWR(ref_resistance, load_resistance):
    '''

    '''
    refl = magnitude(reflection_coefficient(ref_resistance, load_resistance))
    return ((1 + refl) / (1 - refl))


def return_loss_db(incident_power=None, reflected_power=None, reflection_coefficient=None, SWR=None):
    ''' Ratio of reflected power to incident power, in dB.

    incident_power -
    reflected_power -
    reflection_coefficient -
    SWR -
    '''
    if incident_power is not None and reflected_power is not None:
        return -10 * np.log10(reflected_power / incident_power)
    elif reflection_coefficient is not None:
        return -20 * np.log10(abs(reflection_coefficient))
    elif SWR is not None:
        return -20 * np.log10((SWR+1) / (SWR-1))
    raise ValueError(
        'return_loss_db requires providing either (incident_power & reflected_power), or reflection_coefficient, or SWR.')


def insertion_loss_db(incident_power=None, reflected_power=None, reflection_coefficient=None, SWR=None):
    ''' Ratio of transmitted power to incident power. Pt/Pi or (Pi-Pr)/Pi
    If an unmached circuit is connected to an RF source, reflections occur that result in a loss of power delivered to the circuit.
    Insertion loss approaches maximum (inf) in open-circuit and short-circuit conditions.
    Insertion loss is 0 when the circuit and source are matched, as all power is transferred to the circuit.

    incident_power -
    reflected_power -
    reflection_coefficient - The input reflection coefficient
    SWR -
    '''
    if incident_power is not None and reflected_power is not None:
        return -10 * np.log10((incident_power - reflected_power) / incident_power)
    elif reflection_coefficient is not None:
        return - 10 * np.log10(1 - abs(reflection_coefficient)**2)
    elif SWR is not None:
        return 20 * np.log10((SWR+1) * (2 * np.sqrt(SWR)))
    raise ValueError(
        'insertion_loss_db requires providing either (incident_power & reflected_power), or reflection_coefficient, or SWR.')


def to_angular_frequency(f):
    ''' Converts a given frequency (f) in Hz into the angular frequency in radians.
        f - The frequency to convert, measured in hertz (Hz)
    '''
    return 2 * np.pi * f


def from_angular_frequency(f_ang):
    '''
    '''


def from_wavelength(wavelength):
    '''
    '''
    return 3e5 / float(wavelength)


def to_wavelength(f):
    return 3e5 / float(f)


def f0_from_bandwidth(lower, upper):
    ''' Center frequency of a given lower and upper bound, based on the geometric mean.
        lower - Lower frequency
        upper - Upper frequency
    '''
    return np.sqrt(lower * upper)
