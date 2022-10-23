import numpy as np
from ..constants import OPEN_CIRCUIT, SHORT_CIRCUIT


def sum_parallel(args):
    total = 0
    for n in args:
        if n == OPEN_CIRCUIT or n == None:
            continue
        if n == SHORT_CIRCUIT:
            return SHORT_CIRCUIT
        total += 1/n
    if total == SHORT_CIRCUIT:
        return SHORT_CIRCUIT
    if total == None or total == OPEN_CIRCUIT:
        return OPEN_CIRCUIT
    return 1 / total


def decade(value):
    return np.floor(np.log10(value))


def series_resistance(*args):
    return np.sum(args)


def parallel_resistance(*args):
    return sum_parallel(args)


def voltage_divider(V, R1, R2):
    '''
    [V]---[R1]
           |
           +--->>> OUT
           |
          [R2]
           |
         [GND]
    '''
    if R2 == np.inf or R2 is None:
        return V
    if R2 == SHORT_CIRCUIT:
        return SHORT_CIRCUIT
    if R1 == SHORT_CIRCUIT or R1 is None:
        return V
    if R1 == OPEN_CIRCUIT:
        return OPEN_CIRCUIT
    return V * (R2 / (R2 + R1))
    return np.multiply(V, np.divide(R2, (R1 + R2)))


def reverse_voltage_divider(Vout, R1, R2):
    if R1 == SHORT_CIRCUIT or R2 == OPEN_CIRCUIT:
        return Vout
    if R2 == SHORT_CIRCUIT or R1 == OPEN_CIRCUIT:
        return 0.0
    return (Vout * ((R1 + R2) / R2))


def efficiency_in_db(P1=None, P2=None, V1=None, V2=None, I1=None, I2=None, Z1=None, Z2=None):
    if P1 is not None and P2 is not None:
        return 10 * np.log10(P1/float(P2))
    elif V1 is not None and V2 is not None:
        if Z1 != Z2:
            return 20 * np.log10((N1 * np.sqrt(Z2)) / (N2 * np.sqrt(Z1)))
        else:
            return 20 * np.log10(V1 / float(V2))
    elif I1 is not None and I2 is not None:
        if Z1 != Z2:
            return 20 * np.log10((N1 * np.sqrt(Z1)) / (N2 * np.sqrt(Z2)))
        else:
            return 20 * np.log10(I1 / I2)
    raise ValueError("")
