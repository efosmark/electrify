import electrify as e
from electrify.math.ac import phase
from electrify.math.rf import magnitude
from electrify.math.common import voltage_divider
import numpy as np


def attenuation_factor(cx):
    ''' Attenuation factor in decibels (dB) from complex input (x+yj)

    cx - Complex number representing the response from H(ω)
    '''
    # Exact formula from page 208:
    return 10 * np.log10(magnitude(cx)**2)


def voltage_gain(V1, V2, Z1=1.0, Z2=1.0):
    return (V1 * np.sqrt(Z2)) / (V2 * np.sqrt(Z1))


def voltage_gain_db(V1, V2, Z1, Z2):
    return 10 * np.log10(magnitude(voltage_gain(V1, V2, Z1, Z2))**2)


def voltage_phase(V1, V2, Z1, Z2):
    return phase(voltage_gain(V1, V2, Z1, Z2))


def complex_power(V, C):
    return V * C  # * np.cos(phase(V) - phase(C))


def power_gain(V1, C1, V2, C2):
    return 10 * np.log10(
        complex_power(V1, C1) / complex_power(V2, C2)
    )


def transducer_gain(VL, RL, VIN, RS):
    '''

    References:
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    '''
    return ((VL**2) / RL) * ((4 * RS)/(VIN**2))


def available_power(VIN, RS):
    '''

    References:
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    '''
    return (VIN**2.0) / (4.0 * RS)


def load_power(RS, RL):
    '''

    References:
        Hayward, W.H. (1982). Introduction to Radio Frequency Design (p. 19).
    '''
    return 4.0 * RS * RL


def insertion_loss(RS, RL):
    '''

    References:
        Hardy, J.K. (1978). High Frequency Circuit Design (pp. 67, 112).
             Reston Publishing, LLC.
    '''
    return 20.0 * np.log10(magnitude(load_power(RS, RL) / available_power(RS, RL)))
    # return 20 * np.log10(R_parallel / (R_parallel + R_source))

###

###


def voltage_gain_db(f, c):
    sln = c.solve(f=f, source=c.source_node, load=c.load_node)
    V_in = voltage_divider(
        sln[c.source_node]['voltage'],    # V_source
        sln[c.source_node]['res_self'],   # R_source
        sln[c.load_node]['res_self']      # R_load
    )
    V_load = sln[c.load_node]['voltage']  # V_load
    if V_load == 0:
        return 0, 0
    gain = V_load / V_in
    return ((20 * np.log10(gain)).real), e.math.phase_angle(gain, deg=True)


def current_gain_db(f, c):
    sln = c.solve(f=f, source=c.source_node, load=c.load_node)

    C_source = magnitude(sln[c.source_node]['current']) - magnitude(sln[c.source_node]['current_self'])
    C_load = magnitude(sln[c.load_node]['current_self'])

    return (20 * np.log10(C_load / C_source)) if C_source != 0 else 0


def power_gain_db(f, c):
    sln = c.solve(f=f, source=c.source_node, load=c.load_node)

    src_v = sln[c.source_node]['voltage']
    src_z = sln[c.load_node]['res_self'] * 4.0
    S = src_v**2 / src_z

    load_v = sln[c.load_node]['voltage']
    load_z = sln[c.load_node]['res_self']
    L = load_v**2 / load_z

    return 10 * np.log10(L / S)


def power_gain2_db(f, c):
    sln = c.solve(f=f, source=c.source_node, load=c.load_node)
    Gt = transducer_gain(
        VL=sln[c.load_node]['voltage'],
        RL=sln[c.load_node]['res_self'],
        VIN=sln[c.source_node]['voltage'],
        RS=sln[c.source_node]['res_self']
    )
    return 10 * np.log10(Gt)
