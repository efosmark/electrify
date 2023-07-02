"""
Representation(s) of a capacitor.

Examples
--------
>>> c = Capacitor(farad(micro=10))

"""
from ..value.unit import *
from ..quantity.energy import get_energy
from ..quantity.charge import get_charge
from ..quantity.reactance import get_reactance
from ..quantity.inductance import get_inductance
from ..quantity.capacitance import get_capacitance


from ..formula.sum import harmonic_sum
from .element import Element
from ...network.proto import Resistive, Reactive, Capacitive


class Capacitor(Element, Resistive, Reactive, Capacitive):
    """
    Represents a physical capacitor.

    A capacitor has four main defining parameters:

        :C:      Capacitive value (farad)
        :ESR:    Equivalent series resistance (ohm)
        :ESL:    Equivalent series inductance (henry).
        :Rp:     Parallel leakage resistance (ohm)
        :Vmax:   Maximum rated voltage (volt)

    Physical model of a capacitor::

                           ╭─────╮
                      ╔════╡ Rp  ╞═════╗
                      ║    ╰─────╯     ║
            ╭─────╮   ║  ╭──────────╮  ║   ╭─────╮
        ════╡ ESR ╞═══╩══╡    C     ╞══╩═══╡ ESL ╞════
            ╰─────╯      ╰──────────╯      ╰─────╯ 

    """

    _capacitance: farad
    _equivalent_series_resistance: ohm
    _leakage_resistance: ohm
    _equivalent_series_inductance: henry

    def __init__(
        self,
        capacitance: farad | float,
        ESR: ohm | float = 0,
        ESL: henry | float = 0,
        leakage_resistance: ohm | float | None = None,
        **kwargs
    ):
        """
        Create a new instance of `Capacitor` with the given parameters.

        Args:
            capacitance (farad | float): Capacitance in farads (F).
            ESR (ohm | float, optional):
                Internal resistance of the capacitor in ohms. Defaults to 0.
                In an ideal capacitor, this is 0.
            ESL (henry | float, optional):
                Equivalent series inductance in henrys. Defaults to 0.
                In an ideal capacitor, this is 0.
            leakage_resistance (ohm | float | None, optional):
                The lead-to-lead :term:`leakage resistance`. Defaults to None.
                Sometimes known as the :term:`insulation resistance`.
                In an ideal capacitor, this is infinite.
        """
        super().__init__(**kwargs)
        self._capacitance = farad(capacitance)
        if ESR:
            self._equivalent_series_resistance = ohm(ESR)
        if ESL:
            self._equivalent_series_inductance = henry(ESL)
        if leakage_resistance:
            self._leakage_resistance = ohm(leakage_resistance)

    def capacitance(self) -> farad:
        """
        Get the capacitance in farads.

        Returns:
            farad: Capacitance of the element.
        """
        return self._capacitance

    def charge(self, voltage: volt | float) -> coulomb:
        """
        Get the stored :term:`electric charge` of the capacitor.

        Args:
            voltage (volt | float): Capacitor voltage, in volts.

        Returns:
            coulomb: Electric charge in coulombs (C).
        """
        return get_charge(C=self._capacitance, V=volt(voltage))

    def energy(self, voltage: volt | float) -> joule:
        """
        Get the quantity of :term:`energy` in the capacitor.

        Args:
            voltage (volt | float): Capacitor voltage, in volts.

        Returns:
            joule: Energy when the capacitor is at the given voltage.
        """
        return get_energy(Q=self.charge(voltage), V=volt(voltage))

    def impedance(self, frequency: hertz | float) -> ohm:
        """
        Get the complex impedance of the capacitor at a given frequency.

        Args:
            frequency (hertz | float): Frequency input in hertz.

        Returns:
            ohm: Complex impedance (R + Xj) of the capacitor at the given frequency.
        """
        result = 0 + 0j
        if self._equivalent_series_resistance is not None:
            result += self._equivalent_series_resistance

        if self._equivalent_series_inductance is not None:
            result += (get_inductance(f=frequency, X=self._equivalent_series_inductance) * 1j)

        if self._leakage_resistance:
            result += harmonic_sum([self._leakage_resistance, self.reactance(frequency) * -1j])
        else:
            result += self.reactance(frequency) * 1j

        return ohm(result)

    def quality_factor(self, frequency: hertz | float) -> complex:
        """
        Get the :term:`quality-factor` of the capacitor (also known as the "Q" or "figure-of-merit").

        The component Q is defined as the ratio of reactance to resistance.

        Args:
            frequency (hertz | float): Frequency input in hertz (Hz).

        Returns:
            float: The quality factor
        """
        return complex(self.reactance(frequency) / self.resistance())

    def reactance(self, frequency: hertz | float) -> ohm:
        """
        Get the :term:`reactance` of the capacitor at a given frequency.

        The reciprocal of reactance is obtained from :class:`Capacitor.susceptance`.

        Args:   
            frequency (hertz | float): Frequency input in hertz.

        Returns:
            ohm: Capacitive reactance in ohms.

        Example:
            >>> Capacitor(pico=22).reactance(10e6)
            TBD
        """
        return get_reactance(f=hertz(frequency), C=self._capacitance)

    def resistance(self) -> ohm:
        """
        Get the internal resistance / :term:`ESR`.

        Returns:
            ohm: The equivalent series resistance of the capacitor.
        """
        return self._equivalent_series_resistance

    @classmethod
    def from_reactance(cls, frequency: hertz | float, reactance: ohm | float, **kwargs):
        """
        Create a new instance of ``Capacitor`` that has the reactance at the given frequency.

        Args:
            frequency (hertz | float): Frequency input in hertz.
            reactance (ohm | float): Reactance input in ohms.

        Returns:
            Capacitor: A new instance based on the reactance configuration
        """
        return cls(
            capacitance=get_capacitance(f=frequency, X=reactance),
            **kwargs
        )
