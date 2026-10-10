# """
# Tools for working with electronic-related values/quantities.

# This package is responsible for:

#  * Units (e.g. ohms, farad, henry, etc)
#  * Orders of magnitude (e.g. pico, milli, kilo, etc)
#  * Values parsed from strings (e.g. `"22pF"` --> `farad(22e-12)`)

# """
import cmath
from typing import Sequence

from .types import units, units_by_name, ElectricUnit
from .prefix import Prefix, all_prefixes, get_appropriate_prefix, format_prefix
from . import parsetext

[ampere, coulomb, farad, henry, hertz, joule,
 metre, ohm, siemens, second, volt, watt, weber] = units

[femto, pico, nano, micro, milli, one, kilo, mega, giga, tera, peta] = all_prefixes


def from_string(string: str) -> ElectricUnit | float | complex:
    """
    Given an input string representing a value, convert it to the appropriate unit & magnitude.

    Args:
        string (str): Input string representing a value (e.g. `"47nF"`)

    Raises:
        ValueError: The input string does not follow the expected format.
        TypeError: An unknown unit has been found.

    Returns:
        UnitType: The value as the appropriate unit & magnitude (e.g. `farad(0.000047)`)

    Examples:
        **Value, Magnitude, Unit**

        >>> v = from_string('121pF')
        >>> repr(v)
        'farad(1.21e-10)'
        >>> str(v)
        '121pF'
        >>> type(v)
        <class 'electrify.value.unit.farad'>

        **Value, Unit**

        >>> v = from_string('880Ω')
        >>> repr(v)
        'ohm(880.0)'
        >>> type(v)
        <class 'electrify.value.unit.ohm'>

        **Value, Magnitude**
        No unit defaults to ``float`` or ``complex``.

        >>> v = from_string('154.2k')
        >>> repr(v)
        '154200.0'
        >>> type(v)
        <class 'float'>

        **Value only**

        >>> v = from_string('220')
        >>> repr(v)
        '220.0'
        >>> type(v)
        <class 'float'>
    """
    tlist = parsetext.scan(string)
    value = 0.0
    unit_type = None

    if parsetext.match(tlist, (parsetext.NumberToken,)):
        value += tlist[0].value

    elif parsetext.match(tlist, (parsetext.NumberToken, parsetext.MagnitudeToken)):
        value += tlist[0].value
        value = value * tlist[1].magnitude

    elif parsetext.match(tlist, (parsetext.NumberToken, parsetext.UnitToken)):
        value += tlist[0].value
        unit_type = tlist[1].id

    elif parsetext.match(tlist, (parsetext.NumberToken, parsetext.MagnitudeToken, parsetext.UnitToken)):
        value += tlist[0].value
        value = value * tlist[1].magnitude
        unit_type = tlist[2].id

    else:
        raise ValueError(
            "Format must be [value][mag][unit] or [value][unit]. Got: '{}'".format(tlist)
        )

    if unit_type is None:
        return float(value)
    elif unit_type in units_by_name:
        return units_by_name[unit_type](value)
    raise TypeError('Unknown unit: {}'.format(unit_type))


def format_value(x, places=0) -> str:
    """
    Given an input value, format it in a string form.

    This should take in to account unit types and optimal unit prefix magnitudes.

    Args:
        x (_type_): Input value
        places (int, optional): Maximum number of places to show. Defaults to 0.

    Returns:
        str: Formatted version of the input value.
    """
    if isinstance(x, str):
        return x
    if isinstance(x, Sequence):
        return "".join([format_value(z, places) for z in x])
    if isinstance(x, dict):
        return str(dict([(str(k), format_value(v, places)) for k, v in x.items()]))
    if x is None:
        return "None"
    if isinstance(x, ElectricUnit):
        return str(x)
    try:
        if cmath.isinf(x):
            return "INF"
        if cmath.isnan(x):
            return "NaN"
        return format_prefix(x, places)
    except TypeError:
        return str(x)


__all__ = ["from_string", "format_value"]
