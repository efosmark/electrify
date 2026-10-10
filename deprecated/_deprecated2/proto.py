"""
Typing protocols for electrical elements.

References
----------
 * https://mypy.readthedocs.io/en/stable/protocols.html
 * https://docs.python.org/3/library/typing.html#protocols
 
"""
from typing import Protocol, runtime_checkable

from electrify.network.n2.net import TwoPole
from ..value.unit import *
 

@runtime_checkable
class Resistive(Protocol):
    """Protocol describing resistive objects."""

    def resistance(self) -> ohm:
        """Get the resistance in ohms."""
        ...

    def conductance(self) -> siemens:
        """Get the conductance in siemens."""
        return siemens(1.0 / self.resistance())


@runtime_checkable
class Reactive(Protocol):
    """Protocol describing reactive objects."""

    def reactance(self, frequency: hertz | float) -> ohm:
        """Get the reactance at a given frequency."""
        ...

    def quality_factor(self, frequency: hertz | float) -> float:
        """Get the quality-factor / figure-of-merit."""
        ...

    def impedance(self, frequency: hertz | float) -> ohm:
        """Get the impedance at a given frequency."""
        ...

    def dissipation_factor(self, frequency: hertz | float) -> float:
        """Get the dissipation factor as the reciprocal of the quality factor."""
        return 1.0 / self.quality_factor(frequency)

    def susceptance(self, frequency: hertz | float) -> siemens:
        """Get the susceptance at a given frequency as the reciprocal of the reactance."""
        return siemens(1.0 / self.reactance(frequency))

    def admittance(self, frequency: hertz | float) -> siemens:
        """Get the complex admittance at a given frequency as the reciprocal of the complex impedance."""
        return siemens(1.0 / self.impedance(frequency))


@runtime_checkable
class Capacitive(Reactive, Protocol):
    """Protocol describing capacitive objects."""

    def capacitance(self) -> farad:
        """Get the capacitance measured in farads."""
        ...

    def charge(self, voltage: volt | float) -> coulomb:
        """Get the stored electric charge of the capacitor."""
        ...

    def energy(self, voltage: volt | float) -> joule:
        """Get the amount of energy in the given capacitor."""
        ...


@runtime_checkable
class Inductive(Reactive, Protocol):
    """Protocol describing inductive objects."""

    def inductance(self) -> henry:
        """Get the inductance in henrys."""
        ...

    def magnetic_flux(self, current: ampere | float) -> weber:
        ...

    def energy(self, current: ampere | float) -> joule:
        """Get the energy in an inductive element at a given current."""
        ...


@runtime_checkable
class HasVoltage(Protocol):
    """Protocol describing elements that have a DC voltage."""

    def voltage(self) -> volt:
        """Get the voltage, measured in volts."""
        ...


@runtime_checkable
class HasCurrent(Protocol):
    """Protocol describing elements that have a fixed current."""

    def current(self) -> ampere:
        """Get the fixed current, measured in amperes."""
        ...


@runtime_checkable
class HasSignal(Protocol):
    """Protocol describing objects that have a signal level."""

    def signal_level(self) -> volt:
        """Get the signal level in volts."""
        ...
