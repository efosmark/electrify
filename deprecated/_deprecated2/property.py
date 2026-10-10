"""property import Resistance
    from .f
The base classes for multi-port networks.

Available variants are:

 - `OnePortNetwork`
 - `TwoPortNetwork`

Beyond that, a custom multi-port network can be created by subclassing either of those
variants, or by subclassing `PortNetwork` and specifying the number of ports directly.
"""
from typing import Any, ClassVar, Generic, Optional, TypeVar
from electrify.value.unit1 import *


_T = TypeVar("_T")


class Property(Generic[_T]):
    """Representation of a property of type _T."""

    value: Optional[_T] = None
    
    def __init__(self, value: Optional[_T] = None, name: Optional[str] = None):
        """Create a new property with a value and/or name."""
        self.value = value
        if name is None:
            name = f'{type(self.value).__name__}'
        self.name = name

    def __repr__(self):
        return f'<{self.__class__.__name__} ({self.value})>'


class Pole(Property[None]):
    """In a port network, a port is made up of two poles."""
    
    symbol: ClassVar[str]

    def __repr__(self):
        return f"{self.__class__.__name__}(port={self.__class__.__name__})"

    def __str__(self):
        return f'<port-.{self.__class__.__name__}>'


class PositivePole(Pole):
    """The positive (+) pole of a port."""
    
    symbol:ClassVar[str] = '+'


class NegativePole(Pole):
    """The negative (-) pole of a port."""
    
    symbol:ClassVar[str] = '-'


class Capacitance(Property[farad]): ...

class Inductance(Property[henry]): ...

class Resistance(Property[ohm]): ...

class Impedance(Property[ohm]): ...

class Voltage(Property[volt]): ...

class Current(Property[ampere]): ...

class Signal(Property):
    frequency: hertz
    amplitude: volt
    phase: Optional[RadPerSecond]
    
    def __init__(
        self,
        frequency:hertz|float,
        amplitude:volt|float = 1.0,
        phase:Optional[RadPerSecond|float] = None
    ):
        self.frequency = hertz(frequency)
        self.amplitude = volt(amplitude)
        if phase:
            self.phase = RadPerSecond(phase)
