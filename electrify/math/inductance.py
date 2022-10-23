import numpy as np

from .common import series_resistance, parallel_resistance
from .rf import magnitude


def series_inductance(*args, mutual_inductance=0):
    if mutual_inductance == 0:
        return series_resistance(*args)
    total_mutual_inductance = (len(args) * abs(mutual_inductance))
    if mutual_inductance < 0:
        total_mutual_inductance = 0 - total_mutual_inductance
    return series_resistance(*args) + total_mutual_inductance


def parallel_inductance(*args, mutual_inductance=0):
    return parallel_resistance(*[ind + mutual_inductance for ind in args])


def mutual_inductance(aiding_inductance=0, opposing_inductance=0):
    return (aiding_inductance - opposing_inductance) / 4.0


def coupling_coefficient(L1, L2, mutual_inductance):
    ''' The coefficient of two inductively-coupled RF coils that are providing transformer action.
    All arguments must share the same unit and magnitude.

    L1                - Self-inductance of the first inductor
    L2                - Self-inductance of the second inductor
    mutual_inductance - Mutual inductance of the interacting fields.
    '''
    return mutual_inductance / float(np.sqrt(L1 * L2))


def inductive_reactance(freq, ind):
    ''' Provides the reactance (X) in ohms (Ω) at a given frequency for a given inductance.
    Inductive reactance will always be a positive number, unless the frequency is 0Hz, in which
    case the reactance is 0.

    freq - Frequency in hertz (Hz)
    ind  - Inductance in henrys (H)
    '''
    if freq <= 0:
        raise ValueError('Frequency must be a positive number. Received: "{}"'.format(freq))
    if freq == 0:
        return 0
    return 2 * np.pi * freq * ind * 1j


def inductance_from_reactance(f, X):
    ''' Provides the inductance in henrys (H) for a given frequency and reactance value.

    f - Frequency in hertz (Hz)
    X - Inductive reactance in ohms (Ω). This behaves the same whether or not this value is negative.
    '''
    if f <= 0:
        raise ValueError('Frequency must be a positive number. Received: "{}"'.format(f))
    return magnitude(abs(X)) / (2 * np.pi * f)


def inductance_from_resonance(f, C):
    ''' The inductance calculated from a known resonant circuit.

    f - Frequency in hertz (Hz)
    C - Capacitance of the resonant circuit
    '''
    return 1 / ((4.0 * np.pi**2) * f * C)


def inductive_energy(inductance, current):
    ''' Provides the energy stored in an inductor in joules (J) based on the inductance and current.

    inductance - Inductance in henrys (H)
    current    - Current in amps (A)
    '''
    return 0.5 * inductance * current**2


def primary_to_secondary(Vp=None, Vs=None, Ip=None, Is=None, Zp=None, Zs=None):
    if Vp is not None and Vs is not None:
        return Vp / Vs
    elif Ip is not None and Is is not None:
        return Is / Ip
    elif Zp is not None and Zs is not None:
        return np.sqrt(Zp / Zs)
    raise ValueError("Must specify value pair: Vp & Vs, Ip & Is, or Zp & Zs.")


def toroidal_inductance(num_turns, initial_permeability, cross_section_core_area, effective_core_length):
    ''' Inductance of a toroidal-core winding in nano-henerys.

    num_turns - Number of turns
    initial_permeability - Initial permeability
    cross_section_core_area - Cross-sectional area of the core in cm**2
    effective_core_length - Effective length of the core in cm
    '''
    return (0.4 * np.pi * num_turns**2 * initial_permeability * cross_section_core_area * 10e-2) / effective_core_length


def toroidal_inductance_from_index(num_turns, inductance_index):
    ''' Inductance of a toroidal-core winding in nano-henrys.

    num_turns - Number of turns
    inductance_index - Inductive index in nano-henrys / turn**2 (A_L)
    '''
    return num_turns**2 * inductance_index


def num_turns_from_index(inductance, inductive_index):
    ''' Number of turns wound around a toroidal-core for a given inductive index.

    inductance - Inductance in nano-henrys
    inductance_index - Inductive index in nano-henrys / turn**2 (A_L)
    '''
    return np.sqrt(inductance / inductive_index)
