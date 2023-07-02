"""Representations of inductors."""
import cmath

from electrify.value.sum import harmonic_sum
from ..value.unit import *
from .element import Element
from ...network.proto import Resistive, Reactive, Inductive
from ..quantity.inductance import get_inductance
from ..quantity.reactance import get_reactance


def inductor(L, Rs, Cd, Rp=None):
    return parallel(
        [Rs, L],
        Cd,
        Rp
    )


class Inductor(Element, Resistive, Reactive, Inductive):
    """
    Represents a physical inductor.

    A inductor has four main defining parameters:

        :L:      Inductive value (henry)
        :Rs:     Series resistance of the windings (ohm)
        :Rp:     Losses from the magnetic core itself due to hysteresis (ohm) (zero for air-core)
        :Cd:     Parasitic capacitance between windings (farad)


    Physical model of an air-core inductor::

                         ╭────╮
             ╔═══════════╡ Cd ╞════════╗
             ║           ╰────╯        ║   
             ║  ╭────╮   ╭─────────╮   ║ 
        ═════╩══╡ Rs ╞═══╡    L    ╞═══╩══════
                ╰────╯   ╰─────────╯



    Physical model of a magnetic-core inductor::

                         ╭────╮
             ╔═══════════╡ Cd ╞════════╗
             ║           ╰────╯        ║   
             ║  ╭────╮   ╭─────────╮   ║ 
        ═════╬══╡ Rs ╞═══╡    L    ╞═══╬══════
             ║  ╰────╯   ╰─────────╯   ║
             ║           ╭────╮        ║
             ╚═══════════╡ Rp ╞════════╝
                         ╰────╯         
    """
# ╔ ╗ ╚ ╝ ╦ ╬ ╣ ╠

    _inductance: henry
    _series_resistance: ohm
    _parasitic_capacitance: farad

    def __init__(
        self,
        inductance: henry | float,
        series_resistance: ohm | float = 0,
        parasitic_capacitance: farad | float = 0,
        **kwargs
    ):
        """Initialize a new inductor with the given parameters."""
        super().__init__(**kwargs)
        self._inductance = henry(inductance)
        self._series_resistance = ohm(series_resistance)
        self._parasitic_capacitance = farad(parasitic_capacitance)

    def inductance(self) -> henry:
        return self._inductance

    def magnetic_flux(self, current: ampere | float) -> weber:
        ...

    def resistance(self) -> ohm:
        """
        Get the wire resistance of the inductor.

        Returns:
            ohm: Series wire resistance in ohms
        """
        return self._series_resistance

    def reactance(self, frequency: hertz | float) -> ohm:
        """
        Get the :term:`inductive reactance` at a given frequency.

        The reciprocal of reactance is obtained from `susceptance()`.

        Args:
            frequency (hertz | float): Frequency input in hertz (Hz)

        Returns:
            ohm: Inductive reactance in ohms
        """
        return get_reactance(f=hertz(frequency), L=self._inductance)

    def quality_factor(self, frequency: hertz | float) -> float:
        """
        Get the Q / quality-factor / figure-of-merit of the inductor.

        The component Q is defined as the ratio of reactance to resistance. 

        Args:
            frequency (hertz | float): Frequency of interest, in hertz (Hz)

        Returns:
            float: The Q / quality-factor / figure-of-merit
        """
        return (self.reactance(frequency) / self.resistance()).real

    def impedance(self, frequency: hertz | float) -> ohm:
        """
        Get the impedance of the capacitor at a given frequency.

        Impedance is often symbolized as `Z`.

        Parameters
        ----------
        frequency (hertz|float): Frequency input in hertz (Hz)
        abs (bool): If true, Z is returned as an absolute value, rather than complex

        Returns
        -------
         * `ohm` — Absolute impedance of the capacitor at the specified frequency
        """
        paths: list[ohm] = []
        paths.append(ohm(self.resistance() + self.reactance(frequency)))
        if self._series_resistance is not None:
            paths.append(self._series_resistance)
        if self._parasitic_capacitance is not None:
            paths.append(get_reactance(
                f=hertz(frequency),
                C=self._parasitic_capacitance
            ))
        return ohm(harmonic_sum(paths))

    @classmethod
    def from_reactance(cls, frequency: hertz | float, reactance: ohm | float, **kwargs):
        """
        Initialize a new instance of an inductor whose inductance meets the reactance criteria.

        Parameters
        ----------
        frequency (hertz|float): Frequency of interest, in hertz
        reactance (ohm|float): Reactance of interest, in ohms

        """
        return cls(
            inductance=get_inductance(f=hertz(frequency), X=ohm(abs(reactance))),
            **kwargs
        )

    def energy(self, current: ampere | float) -> joule:
        """
        Get the energy stored in Joules (J) based on the inductance and current.

        Parameters
        ----------
        current (ampere|float): Current in amps (A)

        Returns
        -------
        * `joule` — Energy stored in an inductor
        """
        return get_energy(L=self._inductance, I=ampere(current))
        # return joule(0.5 * self._inductance * current**2)


class Toroid(Inductor):
    """
    A toroidal inductor.

    Examples
    --------
    >>> # Not yet provided.

    """

    def num_turns(self, inductive_index: int) -> float:
        """
        Get the number of turns wound around a toroidal-core for a given inductive index.

        inductance - Inductance in nano-henrys
        inductance_index - Inductive index in nano-henrys / turn**2 (A_L)
        """
        # TODO: Update docstring
        return cmath.sqrt(self._inductance / inductive_index).real

    @classmethod
    def from_winding(
        cls,
        num_turns: float,
        initial_permeability: float,
        cross_section_core_area: float,
        effective_core_length: float,
        **kwargs
    ):
        """
        Inductance of a toroidal-core winding in nano-henerys.

        num_turns - Number of turns
        initial_permeability - Initial permeability
        cross_section_core_area - Cross-sectional area of the core in cm**2
        effective_core_length - Effective length of the core in cm
        """
        # TODO: Update docstring
        inductance = (0.4 * 3.14159 * num_turns ** 2 * initial_permeability *
                      cross_section_core_area * 10e-2) / effective_core_length
        return cls(inductance, **kwargs)

    @classmethod
    def from_inductive_index(cls, num_turns: float, inductance_index: float, **kwargs):
        """
        Inductance of a toroidal-core winding in nano-henrys.

        num_turns - Number of turns
        inductance_index - Inductive index in nano-henrys / turn**2 (A_L)
        """
        # TODO: Update docstring
        inductance = num_turns**2 * inductance_index
        return cls(inductance, **kwargs)


class Choke(Inductor):
    """A high-impedance RF choke."""

    ...


class Transformer(Element):
    """A two-part transformer."""

    # TODO: Determine a method of supporting more dynamic transformer structures
    _primary: Inductor
    _secondary: Inductor


def ind_transformer_primary_to_secondary(Vp=None, Vs=None, Ip=None, Is=None, Zp=None, Zs=None):
    if Vp is not None and Vs is not None:
        return Vp / Vs
    elif Ip is not None and Is is not None:
        return Is / Ip
    elif Zp is not None and Zs is not None:
        return cmath.sqrt(Zp / Zs)
    raise ValueError("Must specify value pair: Vp & Vs, Ip & Is, or Zp & Zs.")
