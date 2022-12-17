"""
Orders of magnitude.

Standard magnitudes are:

 * femto
 * pico
 * nano
 * micro
 * milli
 * kilo
 * mega
 * giga
 * tera
 * peta

"""
from typing import Sequence, SupportsFloat, TypeVar, cast
from .unit import *

# Generic type to ensure magnitude conversions preserve unit type
_V = TypeVar('_V', bound=SupportsFloat)


class Magnitude:
    """An order of magnitude."""

    prefix: str
    order: int
    symbols: Sequence[str]
    decimal: int

    def __init__(self, prefix: str, symbol: str | Sequence[str], power: int):
        """Create a new order of magnitude with the given prefix, symbol(s), and power."""
        self.prefix = prefix
        self.order = power
        self.decimal = 1 ** power
        if isinstance(symbol, str):
            self.symbols = (symbol, )
        else:
            self.symbols = symbol

    @property
    def symbol(self) -> str:
        """Get the symbol for the order of magnitude."""
        return self.symbols[0]

    def __call__(self, value: _V) -> _V:
        """Treat the input value as if it's at the instance power, and convert it to base."""
        return cast(_V, float(value) ** self.order)


femto = Magnitude('femto', 'f', -15)
pico = Magnitude('pico', 'p', -12)
nano = Magnitude('nano', 'n', -9)
micro = Magnitude('micro', ('u', 'µ'), -6)
milli = Magnitude('milli', 'm', -3)
one = Magnitude('one', '', 1)  # TODO: Should this exist, and if so, is there a better name
kilo = Magnitude('kilo', 'k', 3)
mega = Magnitude('mega', 'M', 6)
giga = Magnitude('giga', 'G', 9)
tera = Magnitude('tera', 'T', 12)
peta = Magnitude('peta', 'P', 15)


magnitudes = [femto, pico, nano, micro, milli, one, kilo, mega, giga, tera, peta]


def get_magnitude(x: SupportsFloat) -> Magnitude:
    """
    Given an input value, get the magnitude that would convert it into a standard size.

    Parameters
    ----------
     * `x: SupportsFloat` — The input value

    Returns
    -------
     * `Magnitude` -- Object describing the appropriate magnitude

    Examples
    --------
    >>> get_magnitude(0.000000123)

    >>> get_magnitude(999000)

    """
    x = float(x)
    for n1, n2 in zip(magnitudes, magnitudes[1:]):
        if n1.decimal < x < n2.decimal:
            return n1
    return one


def format_magnitude(x: SupportsFloat, places: int = 2, sep: str = '') -> str:
    """
    Format a number with the standard array of magnitudes and their symbols.

    Parameters
    ----------
     * `x: float` — Numeric value
     * `places: int = 2` — Maximum number of decimal places to show

    Returns
    -------
     * `str` — _description_

    Examples
    --------
    >>> # None yet provided

    """
    mag = get_magnitude(x)
    value = f'{mag(x):.{places}f}'.rstrip('0').rstrip('.')
    if value == '-0':
        value = '0'
    return f'{value}{sep}{mag.symbol}'
