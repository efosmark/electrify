"""
Passive resistive elements.

Examples
--------
>>> # Not yet provided.

References
----------
None.
"""
import math
from typing import Optional

from ..value.unit import *
from ..quantity.reactance import get_capacitive_reactance, get_inductive_reactance
from ..quantity.current import get_current
from ..quantity.resistance import from_color_code
from .element import Element
from ...network.proto import Resistive, Reactive


class _Topology(list):

    def __init__(self, *args):
        list.__init__(self, args)


class series(_Topology):
    ...


class parallel(_Topology):
    ...


class SimpleElement:
    pass


class SimpleResistor(SimpleElement):
    resistance: ohm
    body_capacitance: Optional[farad]
    interlead_capacitance: Optional[farad]
    lead_inductance: Optional[henry]
    internal_inductance: Optional[henry]
    power_rating: Optional[watt]

    def __init__(
        self,
        resistance: ohm,
        body_capacitance: Optional[farad],
        interlead_capacitance: Optional[farad],
        lead_inductance: Optional[henry],
        internal_inductance: Optional[henry],
        power_rating: Optional[watt]
    ):
        self.resistance = resistance
        self.body_capacitance = body_capacitance
        self.interlead_capacitance = interlead_capacitance
        self.lead_inductance = lead_inductance
        self.internal_inductance = internal_inductance
        self.power_rating = power_rating

    def __call__(self):
        result = self.resistance
        if self.body_capacitance is not None:
            result = parallel(result, self.body_capacitance)
        if self.lead_inductance is not None:
            result = series(
                self.lead_inductance,
                result,
                self.lead_inductance
            )

        if self.interlead_capacitance is not None:
            result = parallel(result, self.interlead_capacitance)
        return result


class Resistor(Element, Resistive, Reactive):
    """
    A physical resistor.

    A resistor has four main defining parameters:

    :R:      Primary resistive value in ohms.
    :Ca:     Charge separation in farads.
    :Cb:     Interlead capacitance in farads.
    :L:      Lead inductances in henrys.


    For a high-frequency wire-wound style resistor, there's an additional inductive property
    to account for the inductance added by the windings:

    Examples
    --------
    >>> res = Resistor(100)
    >>> res
    <Resistor>

    >>> res.resistance()
    ohm(100)

    """

    _resistance: ohm
    _body_capacitance: Optional[farad]
    _lead_inductance: Optional[henry]
    _power_rating: Optional[watt]

    def __init__(
        self,
        resistance: ohm | float = 0,
        body_capacitance: farad | float = 0,
        lead_inductance: henry | float = 0,
        power_rating: watt | float | None = None,
        **kwargs
    ):
        """
        Create a new instance of `Resistor` with the given parameters.

        Parameters
        ----------
        resistance (ohm|float = 0): Internal resistance of the element

        """
        super().__init__(**kwargs)
        self._resistance = ohm(resistance)
        if body_capacitance:
            self._body_capacitance = farad(body_capacitance)
        if lead_inductance:
            self._lead_inductance = henry(lead_inductance)
        if power_rating:
            self._power_rating = watt(power_rating)

    def resistance(self) -> ohm:
        """
        Get the element resistance.

        Returns
        -------
         * `ohm` — Resistance value in ohms
        """
        return self._resistance

    def power_rating(self) -> watt | None:
        return self._power_rating

    def current_rating(self) -> ampere | None:
        if not self._power_rating:
            return None
        return get_current(P=self._power_rating, R=self._resistance)

    @classmethod
    def from_color_code(
        cls,
        first: str,
        second: str,
        third: str,
        forth: Optional[str] = None,
        **kwargs
    ):
        """
        Create a new `Resistor` with a resistance value defined by the color codes.

        Parameters
        ----------
        first (str): First color code band
        second (str): Second color code band
        third (str): Third color code band
        forth (str | None = None): Optional forth color code band

        Returns
        -------
         * `Resistor` — New instance of `Resistor`
        """
        return cls(
            resistance=from_color_code(first, second, third, forth),
            **kwargs
        )

    def reactance(self, frequency: hertz | float) -> ohm:
        """
        Get the reactance of the RF resistor at a given frequency.

        A positive value represents inductive reactance, whereas a negative value represents
        capacitive reactance. A value of exactly 0 indicates the element is resonant or perfectly
        resistive.

        Reactance is often symbolized as `X`.
        The reciprocal of reactance is obtained from `susceptance()`.

        Args:
            frequency (hertz | float): Frequency input in hertz

        Returns:
            ohm: Reactance in ohms
        """
        result = 0
        if self._lead_inductance:
            result = get_inductive_reactance(hertz(frequency), self._lead_inductance)
        if self._body_capacitance:
            result = result - get_capacitive_reactance(hertz(frequency), self._body_capacitance)
        return ohm(result)

    def quality_factor(self, frequency: hertz | float) -> float:
        """
        Get the Q / quality-factor / figure-of-merit of the RF resistor.

        Parameters
        ----------
        frequency (hertz|float): _description_

        Returns
        -------
         * `float` — The Q / quality-factor / figure-of-merit

        Examples
        --------
        >>> # Not yet provided.

        References
        ----------
        None.
        """
        return self.reactance(frequency) / self.resistance()

    def impedance(self, frequency: hertz | float) -> ohm:
        """
        Get the impedance at a given frequency.

        Impedance is often symbolized as `Z`.

        Args:
            frequency (hertz | float): Frequency input in hertz

        Returns:
            ohm: Absolute impedance of the RF resistor at the specified frequency
        """
        if frequency == 0:
            return ohm(math.inf)
        if math.isinf(frequency):
            return self.resistance()
        return ohm(self.resistance() + self.reactance(frequency))
