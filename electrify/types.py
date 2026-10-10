import cmath
from numbers import Complex
from typing import *
from .prefix import Prefix, format_prefix

class ElectricUnit(Complex):
    """Primary unit class from which all other units inherit."""

    symbol: ClassVar[str] = ""
    _value: Final[complex]
    
    @overload
    def __init__(self, *, p:float):...
    @overload
    def __init__(self, *, n:float):...
    @overload
    def __init__(self, *, u:float):...
    @overload
    def __init__(self, *, m:float):...
    @overload
    def __init__(self, *, k:float):...
    @overload
    def __init__(self, *, M:float):...
    @overload
    def __init__(self, *, G:float):...
    @overload
    def __init__(self, *, T:float):...
    @overload
    def __init__(self, value:SupportsComplex | SupportsFloat):...
    def __init__(
        self,
        value: Optional[SupportsComplex | SupportsFloat] = None,
        **kwargs,
    ):
        if value is None and len(kwargs) > 0:
            for k, v in kwargs.items():
                if k in Prefix.by_name:
                    value = Prefix.by_name[k](v)
                    break
                elif k in Prefix.by_symbol:
                    value = Prefix.by_symbol[k](v)
                    break
        if value is None:
            raise ValueError("Either a direct value or a prefixed value must be supplied.")
        self._value = complex(value)

    def __str__(self) -> str:
        return format_prefix(self, places=1, sep="", unit_symbol=self.symbol)

    def __repr__(self):
        if not self.imag:
            return f"{self.__class__.__name__}({self.real})"
        return f"{self.__class__.__name__}({self})"
    
    def __complex__(self) -> complex:
        return self._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __add__(self, other: complex|Self) -> Self:
        return self.__class__(self._value + other)

    def __radd__(self, other: complex|Self) -> Self:
        return self.__class__(other + self._value)

    def __neg__(self) -> Self:
        return self.__class__(-self._value)

    def __pos__(self) -> Self:
        return self.__class__(+self._value)

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        return self._value * other

    def __rmul__(self, other):
        return other * self._value

    def __truediv__(self, other):
        """self / other: Should promote to float when necessary."""
        return self._value / other

    def __rtruediv__(self, other):
        return self.__class__(other / self._value)

    def __pow__(self, exponent):
        return self._value**exponent

    def __rpow__(self, base):
        return self.__class__(base ** self._value)

    def __abs__(self) -> float:
        return self.magnitude

    def __eq__(self, other) -> bool:
        return self._value == other

    @property
    def real(self) -> float:
        """Retrieve the real component of this number."""
        return self._value.real

    @property
    def imag(self) -> float:
        """Retrieve the imaginary component of this number."""
        return self._value.imag

    def conjugate(self) -> Self:
        """(x+y*i).conjugate() returns (x-y*i)."""
        return self.__class__(self._value.conjugate())

    def _sum(self, other: complex|Self) -> Self:
        return self.__class__(self._value + other)
    
    def _harmonic_sum(self, other:complex|Self) -> Self:
        return 1.0 / ((1/self) + (1/other))
    
    @property
    def polar(self) -> tuple[float, float]:
        """Get the polar form of the unit."""
        return cmath.polar(self._value)

    @property
    def magnitude(self):
        """Get the polar magnitude of the value."""
        return self.polar[0]

    @property
    def phase_angle(self):
        """Get the polar phase-angle of the value."""
        return self.polar[1]

    @classmethod
    def from_polar(cls, magnitude: float, phase_angle: float) -> Self:
        """Given a polar form, get a unit with the complex value."""
        return cls(cmath.rect(magnitude, phase_angle))

class ampere(ElectricUnit):
    """Unit of electric current."""

    symbol = "A"

class coulomb(ElectricUnit):
    """Unit of :term:`charge`, or quantity of electricity."""

    symbol = "C"

class farad(ElectricUnit):
    """Unit of electrical :term:`capacitance`."""

    symbol = "F"
    
    def __or__(self, other:complex|Self) -> Self:
        return self._sum(other)
    
    def __and__(self, other:complex|Self) -> Self:
        return self._harmonic_sum(other)

class henry(ElectricUnit):
    """Unit of electrical :term:`inductance`."""

    symbol = "H"
    
    def __or__(self, other:complex|Self) -> Self:
        return self._harmonic_sum(other)
    
    def __and__(self, other:complex|Self) -> Self:
        return self._sum(other)

class hertz(ElectricUnit):
    """Unit of :term:`frequency`."""

    symbol = "Hz"

class joule(ElectricUnit):
    """Unit of :term:`energy`."""

    symbol = "J"

class metre(ElectricUnit):
    r"""

    Primary unit of length.

    .. rubric:: SI Definition [SI_2.3.1]_

    The length of the path traveled by light in a vacuum in :math:`\frac{1}{c}` of a second, where
    :math:`c = 299,792,458`.
    """

    symbol = "m"

class ohm(ElectricUnit):
    """Unit of electric :term:`resistance`."""

    symbol = "Ω"
    
    def __or__(self, other:complex|Self) -> Self:
        return self._harmonic_sum(other)
    
    def __and__(self, other:complex|Self) -> Self:
        return self._sum(other)

class radian(ElectricUnit):
    """Unit of angle."""

    symbol = "rad"

class rad_per_sec(ElectricUnit):
    """Unit of :term:`angular frequency`."""

    symbol = "rad/s"

class second(ElectricUnit):
    """Unit of time."""

    symbol = "s"

class siemens(ElectricUnit):
    """Unit of :term:`conductance`, :term:`susceptance`, and :term:`admittance`."""

    symbol = "S" # ℧
    def __or__(self, other:complex|Self) -> Self:
        return self._sum(other)
    
    def __and__(self, other:complex|Self) -> Self:
        return self._harmonic_sum(other)

class volt(ElectricUnit):
    """Unit of :term:`voltage`."""

    symbol = "V"

class watt(ElectricUnit):
    """Unit of :term:`power`, equal to 1 joule per second."""

    symbol = "W"

class weber(ElectricUnit):
    """Unit of magnetic flux."""

    symbol = "Wb"


@runtime_checkable
class SupportsImpedance(Protocol):
    def impedance(self, frequency:hertz) -> ohm:...


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

_T = TypeVar('_T', ampere, coulomb, farad, henry, hertz, joule, metre, ohm, rad_per_sec, siemens, second, volt, watt, weber)
number = _T|complex

__all__ = ["units", "units_by_name", "ElectricUnit", "ampere", "coulomb",
           "farad", "henry", "hertz", "joule", "metre", "ohm", "rad_per_sec", "siemens", "second",
           "volt", "watt", "weber", "number", "SupportsImpedance"]
