import math
from ..value import *
from .element import Element
from .node import Node
from ...network.proto import Resistive, HasVoltage, HasSignal, HasCurrent


class Source(Element, Resistive):
    _resistance: ohm
    _gnd: Node | None

    def __init__(self, resistance: ohm | float = 0, gnd: Node | None = None, **kwargs):
        """Initialize a new source element with the given ESR."""
        super().__init__(**kwargs)
        self._resistance = ohm(resistance)
        self._gnd = gnd

    def resistance(self) -> ohm:
        """
        Get the internal resistance of the capacitor.

        This can also represent the ESR (equivalent series resistance) for small-signals.

        Returns
        -------
         * `ohm` — Internal resistance in ohms
        """
        return self._resistance

    def conductance(self) -> siemens:
        """
        Get the element conductance.

        Returns
        -------
         * `siemens` — Conductance measured in siemens
        """
        return siemens(1 / self._resistance)


class SignalSource(Source, HasVoltage, HasSignal):
    _frequency: hertz
    _voltage_dc: volt
    _voltage_signal: volt

    def __init__(
        self,
        frequency: hertz | float,
        v_dc: volt | float = 0.0,
        v_signal_max: volt | float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._frequency = hertz(frequency)
        self._voltage_dc = volt(v_dc)
        self._voltage_signal = volt(v_signal_max)

    def voltage(self) -> volt:
        return self._voltage_dc

    def signal_level(self) -> volt:
        return self._voltage_signal

    def __str__(self):
        return '<SignalSource {}+{} @ {}>'.format(
            self._voltage_signal,
            self._voltage_dc,
            self._frequency,
        )


class VoltageSource(Source, HasVoltage):
    _voltage: volt

    def __init__(
        self,
        voltage: volt | float,
        resistance: ohm | float,
        GND: Node | None = None,
        **kwargs
    ):
        super().__init__(resistance, GND, **kwargs)
        self._voltage = volt(voltage)

    def voltage(self) -> volt:
        return self._voltage

    def __str__(self):
        return '<VoltageSource {} {}>'.format(self._voltage, self.resistance())


class CurrentSource(Source, HasCurrent):
    _current: ampere

    def __init__(
        self,
        current: ampere | float,
        resistance: ohm | float = math.inf,
        GND: Node | None = None,
        **kwargs
    ):
        """Initialize a new current source with the specified fixed current."""
        super().__init__(resistance, GND, **kwargs)
        self._current = ampere(current)

    def current(self) -> ampere:
        """
        Get the fixed current in amperes.

        Returns
        -------
         * `ampere` — The fixed current of the current-source
        """
        return self._current

    def __str__(self):
        """Get a string representation of the current-source."""
        return '<CurrentSource {} {}>'.format(self._current, self.resistance())
