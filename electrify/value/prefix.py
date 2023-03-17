"""
Orders of magnitude.

This module provides the orders of magnitude defined by the SI prefixes as callable objects.
It also handles formatting of numbers to their most appropriate magnitude.
"""
from typing import Sequence, SupportsFloat, TypeVar, cast, ClassVar
from typing_extensions import Self

# Generic type to ensure magnitude conversions preserve unit type
_V = TypeVar('_V', bound=SupportsFloat)


class Prefix:
    """An order of magnitude."""

    name: str
    order: int
    symbols: Sequence[str]
    decimal: int

    by_symbol: ClassVar[dict[str, Self]] = {}
    by_name: ClassVar[dict[str, Self]] = {}

    def __new__(cls, name: str, symbol: str | Sequence[str], power: int):
        """Create a new order of magnitude with the given prefix, symbol(s), and power."""
        if name in cls.by_name:
            raise NameError(f"A prefix already exists with the name '{name}'.")

        obj = super(Prefix, cls).__new__(cls)
        obj.name = name
        obj.order = power
        obj.decimal = 10**power

        if isinstance(symbol, str):
            obj.symbols = (symbol, )
        else:
            obj.symbols = symbol

        for s in obj.symbols:
            if s in cls.by_symbol:
                raise NameError(f"A prefix already exists with the symbol '{s}'.")
            cls.by_symbol[s] = obj

        return obj

    @property
    def symbol(self) -> str:
        """Get the symbol for the order of magnitude."""
        return self.symbols[0]

    def __repr__(self) -> str:
        """Get the string representation."""
        return (f'Prefix(name="{self.name}", '
                f'symbol={list(self.symbols)}, '
                f'power={self.order})')

    def __call__(self, value: _V) -> _V:
        """Treat the input value as if it's at the instance power, and convert it to base."""
        return cast(_V, float(value) / (10**self.order))


# Standard SI prefixes used in electrical systems
femto = Prefix('femto', 'f', -15)
pico = Prefix('pico', 'p', -12)
nano = Prefix('nano', 'n', -9)
micro = Prefix('micro', ('µ', 'u'), -6)
milli = Prefix('milli', 'm', -3)
one = Prefix('one', '', 0)
kilo = Prefix('kilo', 'k', 3)
mega = Prefix('mega', 'M', 6)
giga = Prefix('giga', 'G', 9)
tera = Prefix('tera', 'T', 12)
peta = Prefix('peta', 'P', 15)

all_prefixes = [femto, pico, nano, micro, milli, one, kilo, mega, giga, tera, peta]


def get_appropriate_prefix(x: float) -> Prefix:
    """
    Given an input value, get the magnitude that would convert it into a standard size.

    Args:
        x (float): The input value

    Returns:
        Prefix: Object describing the appropriate magnitude

    Examples:
        >>> get_appropriate_prefix(0.000000123)
        Prefix(name="nano", symbol=['n'], power=-9)

        >>> get_appropriate_prefix(999000)
        Prefix(name="kilo", symbol=['k'], power=3)

        >>> get_appropriate_prefix(-2.2e-14)
        Prefix(name="femto", symbol=['f'], power=-15)
    """
    x = abs(x)
    for n1, n2 in zip(all_prefixes, all_prefixes[1:]):
        if n1.decimal <= x < n2.decimal:
            return n1
    return one


def _fmt(x, places, sep, unit_symbol, isimag=False):
    mag = get_appropriate_prefix(x)
    value = f'{mag(x):.{places}f}'.rstrip('0').rstrip('.')
    if value == '-0':
        value = '0'
    if isimag:
        return f'{value}j{sep}{mag.symbol}{unit_symbol}'
    return f'{value}{sep}{mag.symbol}{unit_symbol}'


def format_prefix(x: float | complex, places: int = 2, sep: str = '', unit_symbol='') -> str:
    """
    Format a number with the standard array of magnitudes and their symbols.

    Args:
        x (float | complex): Numeric value
        places (int, optional): Maximum number of decimal places to show. Defaults to 2.
        sep (str, optional): Separation between value and prefix. Defaults to ''.
        unit_symbol (str, optional): If a specific unit is being formatted, its symbol can be 
                                     applied directly. Defaults to ''.

    Returns:
        str: Formatted numeric value with magnitude prefixes applied.

    Examples:
        >>> format_prefix(999000)
        '999k'

        >>> format_prefix(complex(1.87e6, -22e-10))
        '1.87M - [2.2j]n'

        >>> format_prefix(complex(4.7e3, -22e-10), unit_symbol="Ω")
        '4.7kΩ - [2.2j]nΩ'

        >>> format_prefix(6.8e-6, unit_symbol="F")
        '6.8µF'

        >>> value = 798531
        >>> format_prefix(value, places=0)
        '799k'
        >>> format_prefix(value, places=1)
        '798.5k'
        >>> format_prefix(value, places=2)
        '798.53k'
        >>> format_prefix(value, places=3)
        '798.531k'
    """
    if isinstance(x, complex) and x.imag != 0:
        real = _fmt(x.real, places, sep, unit_symbol)
        imag = _fmt(abs(x.imag), places, sep, unit_symbol, isimag=True)
        sign = "-" if x.imag < 0 else "+"
        return f'{real} {sign} {imag}'
    if isinstance(x, complex):
        x = x.real
    return _fmt(x, places, sep, unit_symbol)
