r"""
Custom types to represent the various units of measure used in the project.

[SI]_
[NIST]_

 .. rubric:: Examples

>>> voltage = volt(0.500)
>>> repr(voltage)
'volt(0.5)'
>>> str(voltage)
'500 mV'

>>> resistance = ohm(2000)
>>> repr(resistance)
'ohm(2000.0)'
>>> str(resistance)
'2 kΩ'

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
    '250 µA'

    >>> volt(volt(2000) + 600)
    volt(2600.0)

"""
import cmath
from functools import cache
from typing import ClassVar, Optional, SupportsComplex, SupportsFloat, SupportsIndex, overload
from typing_extensions import Self
from .prefix import Prefix, format_prefix


class base_unit(complex):
    """Primary unit class from which all other units inherit."""

    symbol: ClassVar[str] = ""

    # def __new__(
    #     cls,
    #     value: Optional[complex | SupportsComplex | SupportsFloat | SupportsIndex] = None,
    #     **kwargs,
    # ):
    #     if value is None and len(kwargs) > 0:
    #         for k, v in kwargs.items():
    #             if k in Prefix.by_name:
    #                 value = Prefix.by_name[k](v)
    #                 break
    #             elif k in Prefix.by_symbol:
    #                 value = Prefix.by_symbol[k](v)
    #                 break
    #     if value is None:
    #         raise ValueError("Either a direct value or a prefixed value must be supplied.")
    #     return super().__new__(cls, value)

    def __str__(self) -> str:
        """Get the str representation of the unit."""
        return self.format()

    def format(self) -> str:
        """Get the formatted version of the unit."""
        return format_prefix(self, places=2, sep=" ", unit_symbol=self.symbol)

    @property
    def magnitude(self):
        """Get the polar magnitude of the value."""
        return self.polar()[0]

    @property
    def phase_angle(self):
        """Get the polar phase-angle of the value."""
        return self.polar()[1]

    @cache
    def polar(self) -> tuple[float, float]:
        return cmath.polar(self)

    @classmethod
    def from_polar(cls, magnitude: float, phase_angle: float):
        return cls(cmath.rect(magnitude, phase_angle))

    def _type_convert_div(self, __x, type_map):
        input_value = super().__truediv__(__x)
        input_type = type(__x)
        if input_type in type_map:
            return type_map[input_type](input_value)
        elif input_type == type(self) or input_type in (complex, float, int):
            return self.__class__(input_value)
        return base_unit(input_value)

    def _type_convert_mul(self, __x, type_map):
        input_value = super().__mul__(__x)
        input_type = type(__x)
        if input_type in type_map:
            return type_map[input_type](input_value)
        elif input_type == type(self) or input_type in (complex, float, int):
            return self.__class__(input_value)
        return base_unit(input_value)

    def __pow__(self, __x):
        return self.__class__(super().__pow__(__x))

    def __repr__(self):
        """Get the repr value of the unit."""
        if not self.imag:
            return f"{self.__class__.__name__}({self.real})"
        return f"{self.__class__.__name__}({self})"


_number = base_unit | complex | float | int


class ampere(base_unit):
    """Unit of electric current."""

    symbol = "A"

    @overload
    def __truediv__(self, __x: "siemens") -> "volt": ...
    @overload
    def __truediv__(self, __x: "volt") -> "siemens": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            siemens: volt,
            volt: siemens
        })

    @overload
    def __mul__(self, __x: "henry", /) -> "weber": ...
    @overload
    def __mul__(self, __x: "ohm") -> "volt": ...
    @overload
    def __mul__(self, __x: "volt") -> "watt": ...
    @overload
    def __mul__(self, __x: "weber") -> "ampere": ...
    @overload
    def __mul__(self, __x: "second") -> "coulomb": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            henry: weber,
            ohm: volt,
            volt: watt,
            weber: ampere,
            second: coulomb
        })


class coulomb(base_unit):
    """Unit of :term:`charge`, or quantity of electricity."""

    symbol = "C"

    @overload
    def __truediv__(self, __x: "ampere") -> "second": ...
    @overload
    def __truediv__(self, __x: "farad") -> "volt": ...
    @overload
    def __truediv__(self, __x: "volt") -> "farad": ...
    @overload
    def __truediv__(self, __x: "second") -> "ampere": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            ampere: second,
            farad: volt,
            volt: farad,
            second: ampere
        })

    @overload
    def __mul__(self, __x: "ohm") -> "weber": ...
    @overload
    def __mul__(self, __x: "volt") -> "joule": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            ohm: weber,
            volt: joule
        })


class farad(base_unit):
    """Unit of electrical :term:`capacitance`."""

    symbol = "F"

    @overload
    def __truediv__(self, __x: "siemens") -> "second": ...
    @overload
    def __truediv__(self, __x: "second") -> "siemens": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            siemens: second,
            second: siemens,
        })

    @overload
    def __mul__(self, __x: "hertz") -> "siemens": ...
    @overload
    def __mul__(self, __x: "ohm") -> "second": ...
    @overload
    def __mul__(self, __x: "volt") -> "coulomb": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            hertz: siemens,
            ohm: second,
            volt: coulomb
        })


class henry(base_unit):
    """Unit of electrical :term:`inductance`."""

    symbol = "H"

    @overload
    def __truediv__(self, __x: "ohm") -> "second": ...
    @overload
    def __truediv__(self, __x: "second") -> "ohm": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            ohm: second,
            second: ohm
        })

    @overload
    def __mul__(self, __x: "ampere") -> "weber": ...
    @overload
    def __mul__(self, __x: "hertz") -> "ohm": ...
    @overload
    def __mul__(self, __x: "siemens") -> "second": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            ampere: weber,
            hertz: ohm,
            siemens: second
        })


class hertz(base_unit):
    """Unit of :term:`frequency`."""

    symbol = "Hz"


class joule(base_unit):
    """Unit of :term:`energy`."""

    symbol = "J"

    @overload
    def __truediv__(self, __x: "ampere") -> "weber": ...
    @overload
    def __truediv__(self, __x: "weber") -> "ampere": ...
    @overload
    def __truediv__(self, __x: "coulomb") -> "volt": ...
    @overload
    def __truediv__(self, __x: "volt") -> "coulomb": ...
    @overload
    def __truediv__(self, __x: "watt") -> "second": ...
    @overload
    def __truediv__(self, __x: "second") -> "watt": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            ampere: weber,
            weber: ampere,
            coulomb: volt,
            volt: coulomb,
            watt: second,
            second: watt
        })


class metre(base_unit):
    r"""

    Primary unit of length.

    .. rubric:: SI Definition [SI_2.3.1]_

    The length of the path traveled by light in a vacuum in :math:`\frac{1}{c}` of a second, where
    :math:`c = 299,792,458`.
    """

    symbol = "m"


class ohm(base_unit):
    """Unit of electric :term:`resistance`."""

    symbol = "Ω"
    @overload
    def __truediv__(self, __x: "henry") -> "hertz": ...
    @overload
    def __truediv__(self, __x: "hertz") -> "henry": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            henry: hertz,
            hertz: henry
        })

    @overload
    def __mul__(self, __x: "ampere") -> "volt": ...
    @overload
    def __mul__(self, __x: "coulomb") -> "weber": ...
    @overload
    def __mul__(self, __x: "farad") -> "second": ...
    @overload
    def __mul__(self, __x: "second") -> "henry": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            ampere: volt,
            coulomb: weber,
            farad: second,
            second: henry
        })


class radian(base_unit):
    """Unit of angle."""

    symbol = "rad"


class RadPerSecond(base_unit):
    """Unit of :term:`angular frequency`."""

    symbol = "ω"


class second(base_unit):
    """Unit of time."""

    symbol = "s"

    @overload
    def __mul__(self, __x: "ampere") -> "coulomb": ...
    @overload
    def __mul__(self, __x: "ohm") -> "henry": ...
    @overload
    def __mul__(self, __x: "siemens") -> "farad": ...
    @overload
    def __mul__(self, __x: "volt") -> "weber": ...
    @overload
    def __mul__(self, __x: "watt") -> "joule": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            ampere: coulomb,
            ohm: henry,
            siemens: farad,
            volt: weber,
            watt: joule
        })

    @overload
    def __truediv__(self, __x: "farad") -> "ohm": ...
    @overload
    def __truediv__(self, __x: "henry") -> "siemens": ...
    @overload
    def __truediv__(self, __x: "ohm") -> "siemens": ...
    @overload
    def __truediv__(self, __x: "siemens") -> "henry": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            farad: ohm,
            ohm: farad,
            henry: siemens,
            siemens: henry
        })


class siemens(base_unit):
    """Unit of :term:`conductance`, :term:`susceptance`, and :term:`admittance`."""

    symbol = "℧"

    @overload
    def __truediv__(self, __x: "farad") -> "hertz": ...
    @overload
    def __truediv__(self, __x: "hertz") -> "farad": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            farad: hertz,
            hertz: farad
        })

    @overload
    def __mul__(self, __x: "henry") -> "second": ...
    @overload
    def __mul__(self, __x: "volt") -> "ampere": ...
    @overload
    def __mul__(self, __x: "second") -> "farad": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            henry: second,
            volt: ampere,
            second: farad
        })


class volt(base_unit):
    """Unit of :term:`voltage`."""

    symbol = "V"

    @overload
    def __truediv__(self, __x: "ohm") -> "ampere": ...
    @overload
    def __truediv__(self, __x: "ampere") -> "ohm": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            ohm: ampere,
            ampere: ohm
        })

    @overload
    def __mul__(self, __x: "ampere") -> "watt": ...
    @overload
    def __mul__(self, __x: "coulomb") -> "joule": ...
    @overload
    def __mul__(self, __x: "farad") -> "coulomb": ...
    @overload
    def __mul__(self, __x: "siemens") -> "ampere": ...
    @overload
    def __mul__(self, __x: "second") -> "weber": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            ampere: watt,
            coulomb: joule,
            farad: coulomb,
            siemens: ampere,
            second: weber
        })


class watt(base_unit):
    """Unit of :term:`power`, equal to 1 joule per second."""

    symbol = "W"

    @overload
    def __truediv__(self, __x: "ampere") -> "volt": ...
    @overload
    def __truediv__(self, __x: "volt") -> "ampere": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            ampere: volt,
            volt: ampere
        })

    @overload
    def __mul__(self, __x: "second") -> "joule": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            second: joule
        })


class weber(base_unit):
    """Unit of magnetic flux."""

    symbol = "Wb"

    @overload
    def __truediv__(self, __x: "ampere") -> "henry": ...
    @overload
    def __truediv__(self, __x: "coulomb") -> "ohm": ...
    @overload
    def __truediv__(self, __x: "henry") -> "ampere": ...
    @overload
    def __truediv__(self, __x: "ohm") -> "coulomb": ...
    @overload
    def __truediv__(self, __x: "volt") -> "second": ...
    @overload
    def __truediv__(self, __x: "second") -> "volt": ...
    @overload
    def __truediv__(self, __x: _number): ...

    def __truediv__(self, __x):
        return self._type_convert_div(__x, {
            ampere: henry,
            coulomb: ohm,
            henry: ampere,
            ohm: coulomb,
            volt: second,
            second: volt
        })

    @overload
    def __mul__(self, __x: "ampere") -> "joule": ...
    @overload
    def __mul__(self, __x: _number): ...

    def __mul__(self, __x) -> complex:
        return self._type_convert_mul(__x, {
            ampere: joule
        })


units: list[type] = [ampere, coulomb, farad, henry, hertz, joule,
                     metre, ohm, siemens, second, volt, watt, weber]

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

__all__ = ["units", "units_by_name", "base_unit", "base_unit", "ampere", "coulomb",
           "farad", "henry", "hertz", "joule", "metre", "ohm", "RadPerSecond", "siemens", "second",
           "volt", "watt", "weber"]
