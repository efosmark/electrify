"""
Tools for working with electronic-related values/quantities.

This package is responsible for:
    * Units (e.g. ohms, farad, henry, etc)
    * Orders of magnitude (e.g. pico, milli, kilo, etc)
    * Values parsed from strings (e.g. `"22pF"` --> `Farad(pico=22)`)

Examples
--------
>>> # Not yet provided.

"""
import math
from .unit import units, UnitType, ampere, coulomb, farad, henry, hertz, joule, metre, ohm, RadPerSecond, siemens, second, volt, watt, weber
from .magnitude import Magnitude, magnitudes, get_magnitude, format_magnitude
from .. import scanner

[femto, pico, nano, micro, milli, one, kilo, mega, giga, tera, peta] = magnitudes


def from_string(string: str) -> UnitType:
    """
    Given an input string representing a value, convert it to the appropriate unit & magnitude.

    Parameters
    ----------
     * `string: str` — Input string representing a value (e.g. `"47nF"`)

    Raises
    ------
     * `ValueError` — The input string does not follow `[value][mag][unit]` or `[value][unit]`

    Returns
    -------
     * `UnitType` — The value as the appropriate unit & magnitude (e.g. `Farad(nano=47)`)

    Examples
    --------
    >>> # Not yet provided.
    """
    # TODO: support [value][mag] and [value]
    tlist = scanner.scan(string)
    value = 0.0
    unit_type = None

    if scanner.match(tlist, scanner.ValueUnit):
        value += tlist[0].value
        unit_type = tlist[1].unit
    elif scanner.match(tlist, scanner.ValueMagnitudeUnit):
        value += tlist[0].value
        value = value * tlist[1].magnitude
        unit_type = tlist[2].unit

    if unit_type is None:
        raise ValueError(
            "Format must be [value][mag][unit] or [value][unit]. Got: '{}'".format(tlist))

    return unit_type(value)


def format_value(x, places=0) -> str:
    """
    Given an input value, format it in a string form.

    Parameters
    ----------
     * `x: Any` — Input value
     * `places: int = 0` — Maximum number of places to show

    Returns
    -------
     * `str` — _description_

    Examples
    --------
    >>> # Not yet provided.
    """
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return "".join([format_value(z, places) for z in x])
    if isinstance(x, dict):
        return str(dict([(str(k), format_value(v, places)) for k, v in x.items()]))
    if x is None:
        return "None"
    try:
        if math.isinf(x):
            return "INF"
        if math.isnan(x):
            return "NaN"
        return format_magnitude(x, places)
    except TypeError as te:
        return str(x)


__all__ = ["from_string", "format_value", "format_magnitude", "Magnitude", "magnitudes",
           "get_magnitude", "UnitType", "units", "ampere", "coulomb", "farad", "henry", "hertz",
           "joule", "metre", "ohm", "RadPerSecond", "siemens", "second", "volt", "watt", "weber"]
