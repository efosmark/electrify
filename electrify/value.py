from cmath import isnan
import numpy as np
from matplotlib.ticker import EngFormatter

from .lexer import ElectrifyLexer, NumberToken, MagnitudeToken
from .constants import FEMTO, PICO, NANO, MICRO, MILLI, KILO, MEGA, GIGA, TERA, PETA, COLOR_CODES


def parse_value(value=None, **kwargs):
    if value is not None:
        if isinstance(value, str):
            tokens = ElectrifyLexer(value).scan_all()
            if len(tokens) == 0 or not isinstance(tokens[0], NumberToken) or not isinstance(tokens[1], MagnitudeToken):
                raise ValueError("Unparsable value: {}".format(value))
            return tokens[0].value * tokens[1].magnitude
        return value
    else:
        for key, value in kwargs.items():
            s = ElectrifyLexer(key)
            tokens = s.scan_all()
            if len(tokens) == 0 or not isinstance(tokens[0], MagnitudeToken):
                raise ValueError("Unparsable value: {}".format(value))
            return value * tokens[0].magnitude
    return None


def format_value(x, unit="", places=1) -> str:
    ''' Number formatter

    x - The input number
    '''
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return [format_value(z) for z in x]
    if isinstance(x, dict):
        return dict([(k, format_value(v)) for k, v in x.items()])
    if x is None:
        return "None"
    try:
        if np.isinf(x):
            return "INF"
        if np.isnan(x):
            return "NaN"
        if np.iscomplexobj(x):
            return "{:.2f}".format(x)
        return EngFormatter(unit, places=places, sep=" ")(x)
    except TypeError as te:
        return str(x)


def from_color_code(first, second, third, forth=None):
    if isinstance(first, str):
        first = COLOR_CODES[first]
    if isinstance(second, str):
        second = COLOR_CODES[second]
    if isinstance(third, str):
        third = COLOR_CODES[third]
    if forth is None:
        value = (first * 10) + second
        value = value * 10**third
    else:
        value = (first * 100) + (second * 10) + third
        value = value * 10**forth
    return value


def femto(value):
    return value * FEMTO


def pico(value):
    return value * PICO


def nano(value):
    return value * NANO


def micro(value):
    return value * MICRO


def milli(value):
    return value * MILLI


def kilo(value):
    return value * KILO


def mega(value):
    return value * MEGA


def giga(value):
    return value * GIGA


def tera(value):
    return value * TERA


def peta(value):
    return value * PETA
