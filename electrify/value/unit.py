r"""
Custom types to represent the various units of measure used in the project.

[SI]_
[NIST]_

 .. rubric:: Examples

>>> voltage = volt(0.500)
>>> repr(voltage)
'volt(0.5)'
>>> str(voltage)
'500mV'

>>> resistance = ohm(2000)
>>> repr(resistance)
'ohm(2000.0)'
>>> str(resistance)
'2kΩ'

 .. rubric:: Automatic type conversion

By dividing one type by another, an automatic type conversion can occur.
This does not affect the value itself, merely the subclass of :class:`UnitType` the value takes on.

Here, we see a type conversion from ``(volt / ohm = ampere)``


    >>> voltage = volt(0.500)
    >>> resistance = ohm(2000)
    >>> current = voltage / resistance
    >>> repr(current)
    'ampere(0.00025)'
    >>> str(current)
    '250µA'

    >>> volt(volt(2000) + 600)
    volt(2600.0)

"""
from abc import ABC, abstractmethod
from typing import ClassVar, cast
from . import magnitude


class UnitType(ABC):
    """Primary unit class from which all other units inherit."""

    symbol: ClassVar[str] = ''
    div_by: ClassVar[dict[str, str]] = {}
    mul_by: ClassVar[dict[str, str]] = {}

    @abstractmethod
    def format(self) -> str:
        """Get the formatted version of the unit."""
        return magnitude.format_magnitude(cast(complex, self), places=2, unit_symbol=self.symbol)

    def __str__(self) -> str:
        """Get the str representation of the unit."""
        return self.format()

    @abstractmethod
    def __truediv__(self, __x):
        """Divide the quantity along with unit conversions."""
        ...

    @abstractmethod
    def __mul__(self, __x):
        """Get the multiple of Unit * __x."""
        ...


class CxUnitType(complex, UnitType):
    """Base class for electric or electric-related units that can have complex values."""

    def format(self) -> str:
        """Get the formatted version of the unit."""
        return magnitude.format_magnitude(self, places=2, unit_symbol=self.symbol)

    def __truediv__(self, __x):
        """Divide the quantity along with unit conversions."""
        denom_type = type(__x).__name__
        result = super().__truediv__(self.__class__(__x))
        if denom_type in self.div_by.keys():
            return globals()[self.div_by[denom_type]](result)
        return result

    def __mul__(self, __x) -> complex:
        """Get the multiple of Unit * __x."""
        return super().__mul__(__x)

    def __repr__(self):
        """Get the repr value of the unit."""
        if not self.imag:
            return f'{self.__class__.__name__}({self.real})'
        return f'{self.__class__.__name__}({self})'


class RealUnitType(float, UnitType):
    """Base class for electric or electric-related units."""

    def __truediv__(self, __x):
        """Divide the quantity along with unit conversions."""
        denom_type = str(type(__x))
        result = super().__truediv__(self.__class__(__x))
        if denom_type in self.div_by.keys():
            cls = units_by_name[self.div_by[denom_type]]
            return cls(result)
        return result

    def __mul__(self, __x) -> complex:
        """Get the multiple of Unit * __x."""
        return super().__mul__(__x)

    def __repr__(self):
        """Get the repr value of the unit."""
        return f'{self.__class__.__name__}({self})'


class ampere(CxUnitType):
    """Unit of electric current."""

    symbol = 'A'

    div_by = {
        "siemens": 'volt',
        "volt": 'siemens',
    }

    mul_by = {
        'henry': 'weber',
        'ohm': 'volt',
        'volt': 'watt',
        'weber': 'ampere',
        'second': 'coulomb'
    }


class coulomb(CxUnitType):
    """Unit of :term:`charge`, or quantity of electricity."""

    symbol = 'C'
    div_by = {
        'ampere': 'second',
        'farad': 'volt',
        'volt': 'farad',
        'second': 'ampere'
    }
    mul_by = {
        'ohm': 'weber',
        'volt': 'joule'
    }


class farad(CxUnitType):
    """Unit of electrical :term:`capacitance`."""

    symbol: ClassVar[str] = 'F'
    div_by = {
        "siemens": 'second',
        "second": 'siemens'
    }
    mul_by = {
        "frequency": 'siemens',
        "ohm": 'second',
        "volt": 'coulomb'
    }


class henry(CxUnitType):
    """Unit of electrical :term:`inductance`."""

    symbol = 'H'
    div_by = {
        "ohm": "second",
        "second": 'ohm'
    }
    mul_by = {
        "ampere": 'weber',
        "frequency": 'ohm',
        "siemens": 'second'
    }


class hertz(UnitType):
    """Unit of :term:`frequency`."""

    symbol = 'Hz'
    mul_by = {
        "farad": 'siemens',
        "henry": 'ohm',
        "second": 'complex',
    }


class joule(CxUnitType):
    """Unit of :term:`energy`."""

    symbol = 'J'
    div_by = {
        "ampere": 'weber',
        "weber": 'ampere',
        "coulomb": 'volt',
        "volt": 'coulomb',
        "watt": 'second',
        "second": 'watt'
    }


class metre(UnitType):
    r"""
    Primary unit of length.

    .. rubric:: SI Definition [SI_2.3.1]_

    The length of the path traveled by light in a vacuum in :math:`\frac{1}{c}` of a second, where
    :math:`c = 299,792,458`.
    """

    symbol = 'm'


class ohm(CxUnitType):
    """Unit of electric :term:`resistance`."""

    symbol = 'Ω'
    div_by = {
        "henry": 'hertz',
        "hertz": 'henry'
    }
    mul_by = {
        "ampere": 'volt',
        "coulomb": 'weber',
        "farad": 'second',
        "siemens": 'complex',
        "second": 'henry'
    }


class RadPerSecond(UnitType):
    """Unit of :term:`angular frequency`."""

    symbol = 'ω'


class second(UnitType):
    """Unit of time."""

    symbol = 's'
    mul_by = {
        "ampere": 'coulomb',
        "frequency": 'complex',
        "ohm": 'henry',
        "siemens": 'farad',
        "volt": 'weber',
        "watt": 'joule'
    }
    div_by = {
        "farad": 'ohm',
        "henry": 'siemens',
        "ohm": 'farad',
        "siemens": 'henry'
    }


class siemens(CxUnitType):
    """Unit of :term:`conductance`, :term:`susceptance`, and :term:`admittance`."""

    symbol = '℧'
    div_by = {
        "farad": 'hertz',
        "hertz": 'farad'
    }
    mul_by = {
        "henry": 'second',
        "ohm": 'complex',
        "volt": 'ampere',
        "second": 'farad',
    }


class volt(CxUnitType):
    """Unit of :term:`voltage`."""

    symbol = 'V'
    div_by = {
        'ohm': 'ampere',
        'ampere': 'ohm'
    }
    mul_by = {
        "ampere": 'watt',
        "coulomb": 'joule',
        "farad": 'coulomb',
        "siemens": 'ampere',
        "second": 'weber'
    }


class watt(CxUnitType):
    """Unit of :term:`power`, equal to 1 joule per second."""

    symbol = 'W'
    div_by = {
        'ampere': 'volt',
        'volt': 'ampere'
    }
    mul_by = {
        "second": 'joule'
    }


class weber(CxUnitType):
    """Unit of magnetic flux."""

    symbol = 'Wb'
    div_by = {
        "ampere": 'henry',
        "coulomb": 'ohm',
        "henry": 'ampere',
        "ohm": 'coulomb',
        "volt": 'second',
        "second": 'volt'
    }
    mul_by = {
        "ampere": 'joule'
    }


units = [CxUnitType, ampere, coulomb, farad, henry, hertz, joule,
         metre, ohm, RadPerSecond, siemens, second, volt, watt, weber]

units_by_name = {
    "ampere": ampere,
    "coulomb": coulomb,
    "farad": farad,
    "henry": henry,
    "hertz": hertz,
    "joule": joule,
    "metre": metre,
    "ohm": ohm,
    "siemens": siemens,
    "second": second,
    "volt": volt,
    "watt": watt,
    "weber": weber
}

__all__ = ['units', 'units_by_name', 'UnitType', 'CxUnitType', 'RealUnitType', 'ampere', 'coulomb',
           'farad', 'henry', 'hertz', 'joule', 'metre', 'ohm', 'RadPerSecond', 'siemens', 'second',
           'volt', 'watt', 'weber']
