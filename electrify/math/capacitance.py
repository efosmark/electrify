import numpy as np

from .rf import magnitude
from .common import series_resistance, parallel_resistance
from ..constants import OPEN_CIRCUIT


def series_capacitance(*args):
    return parallel_resistance(*args)


def parallel_capacitance(*args):
    return series_resistance(*args)


def capacitive_reactance(f, cap):
    ''' Provides the reactance (X) in ohms (Ω) at a given frequency for a given capacitance.
        Capacitive reactance will always be a negative number.

    f    - Frequency in hertz (Hz)
    cap  - Capacitance in farads (F)
    '''
    if f < 0:
        raise ValueError(
            'Frequency must be a positive number. Received: "{}"'.format(f))
    if f == 0:
        return -OPEN_CIRCUIT
    if cap == 0:
        return 0
    return (1 / (2 * np.pi * f * cap)) * -1j


def capacitance_from_reactance(f, X):
    ''' Provides the capacitance in farads (F) for a given frequency and reactance value.

    f - Frequency in hertz (Hz)
    X - Capacitive reactance in ohms (Ω). This behaves the same whether or not this value is negative.
    '''
    if f <= 0:
        raise ValueError(
            'Frequency must be a positive number. Received: "{}"'.format(f))
    if X == 0:
        return 0
    return abs(1 / (2 * np.pi * f * magnitude(X)))


def capacitance_from_charge(charge, voltage):
    ''' Provides the capacitance in farads (F) for a given charge at a voltage.

    charge   - Capacitive charge measured in coloumbs (C)
    voltage  - Voltage measured in volts (V)
    '''
    return charge / voltage


def capacitive_charge(capacitance, voltage):
    ''' Computes the charge in coulombs (C) based on the capacitance and voltage.

    capacitance - Capacitance in farads (F)
    voltage     - voltage in volts (V)
    '''
    return capacitance * voltage


def capacitive_energy(capacitance, voltage):
    ''' Provides the energy stored in a capacitor in joules (J) based on the capacitance and voltage.

    capacitance - Capacitance in farads (F)
    voltage     - Voltage in volts (V)
    '''
    return 0.5 * capacitance * voltage**2
