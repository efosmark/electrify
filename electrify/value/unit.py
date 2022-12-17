"""
Custom types to represent the various units of measure used in the project.

See Also
--------
 * `quantity` - Formulas for working with various quantities (e.g. capacitance, inductance, etc)
 * `element` - Models for physical representations (e.g. capacitor, inductor, etc)

Examples
--------
>>> voltage = volt(milli=500)
>>> repr(voltage)
'volt(0.5)'
>>> str(voltage)
'500mV'

>>> resistance = ohm(kilo=2)
>>> repr(resistance)
'ohm(2000.0)'
>>> str(resistance)
'2kΩ'

# Automatic type conversion (volt / ohm = ampere)
>>> current = voltage / resistance
>>> repr(current)
'ampere(0.00025)'
>>> str(current)
'250µA'

>>> volt(Volt(kilo=2) + 600)
volt(2600.0)

References
----------
 * The International System of Units BIPM Brochure 9th Edition (2019): 5.3 Unit names, p.34
      https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
"""
from typing import Type, ClassVar, SupportsFloat
from . import magnitude


class UnitType(float, SupportsFloat):
    """Base class for electric or electric-related units."""

    symbol: ClassVar[str] = ''
    _squared = None
    div_by = ClassVar[dict[Type, Type]]
    mul_by = ClassVar[dict[Type, Type]]

    def __new__(cls, __x: float | None = None, **kwargs: float):
        """
        Create a new instance unit instance.

        Parameters
        ----------
        * `__x: float | None = None` — Initial value with no magnitude
        * `**kwargs: float`
           * If `__x` is not provided, then `kwargs` is checked for a magnitude value instead.
           * Valid argument keys are:
                - `femto` or `f` -- Applies a magnitude of `-15` to the given value.
                - `pico` or `p` -- Applies a magnitude of `-12` to the given value.
                - `nano` or `n` -- Applies a magnitude of `-9` to the given value.
                - `micro`, `u`, or `µ` -- Applies a magnitude of `-6` to the given value.
                - `milli` or `m` -- Applies a magnitude of `-3` to the given value.
                - `kilo` or `k` -- Applies a magnitude of `3` to the given value.
                - `mega` or `M` -- Applies a magnitude of `6` to the given value.
                - `giga` or `G` -- Applies a magnitude of `9` to the given value.
                - `tera` or `T` -- Applies a magnitude of `12` to the given value.
                - `peta` or `P` -- Applies a magnitude of `15` to the given value.

        Raises
        ------
         * `ValueError` — Raised if no value is provided.
        """
        if __x is None and len(kwargs) > 0:
            for key, value in kwargs.items():
                for m in magnitude.magnitudes:
                    if key in m.symbols:
                        __x = m(value)
                        break
                if __x is not None:
                    break
        if __x is None:
            raise ValueError('No initial value given.')
        return super().__new__(cls, __x)

    def format(self) -> str:
        """Get the formatted version of the unit."""
        return f'{magnitude.format_magnitude(float(self), places=2)}{self.symbol}'

    def __str__(self):
        """Get the str representation of the unit."""
        return self.format()

    def __repr__(self):
        """Get the repr value of the unit."""
        return f'{self.__class__.__name__}({float.__repr__(self)})'

    def __truediv__(self, __x: SupportsFloat) -> 'UnitType' | float:
        """
        Divide the quantity along with unit conversions.

        Parameters
        ----------
        * `x: _type_` — _description_

        Returns
        -------
        * `_type_` — _description_

        Examples
        --------
        >>> print(Ampere(1.5) / Ohm(100))
        15mV

        >>> frd = Siemens(3.2) / Hertz(kilo=100)
        >>> print(frd, type(frd))
        32µF <class 'electrify.unit.Farad'>

        """
        result = super().__truediv__(float(__x))
        return result

    def __mul__(self, __x: float) -> float:
        """Get the multiple of Unit * __x."""
        return super().__mul__(__x)


class ampere(UnitType):
    """
    The unit of electric current.

    SI Formal Definition
    --------------------
    The ampere, symbol A, is the SI unit of electric current. It is defined by taking the fixed
    numerical value of the elementary charge e to be `1.602 176 634 * 10e-19` when expressed
    in the unit C, which is equal to `A*s`, where the second is defined in terms of `∆V_Cs`.

    The effect of this definition is that one ampere is the electric current corresponding to the
    flow of `1/(1.602 176 634* 10e-19)` elementary charges per second.

    Equalities
    ----------
     * `[C "electric charge"] / [s "second"]`
     * `[C "electric charge"] * [Hz "frequency"]`
     * `[J "energy"] / [Wb "magnetic flux"]`
     * `[S "conductance"] * [V "voltage"]`
     * `[V "voltage"] * [S "conductance"]`
     * `[V "voltage"] / [Ω "resistance"]`
     * `[W "power"] / [V "voltage"]`
     * `[Wb "magnetic flux"] / [H "inductance"]`

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): p.18
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
    """

    symbol = 'A'

    div_by = {
        "siemens": "volt",
        "volt": "siemens",
    }

    mul_by = {
        'henry': 'weber',
        'ohm': 'volt',
        'volt': 'watt',
        'weber': 'ampere',
        'second': 'coulomb'
    }


class coulomb(UnitType):
    """
    Unit of charge, or quantity of electricity.

    SI Formal Definition
    --------------------
    The coulomb is the quantity of electricity carried in 1 second by a current of 1 ampere.

    Equalities
    ----------
     * `[A "current"] * [s "second"]`
     * `[V "voltage"] * [F "capacitance"]`
     * `[J "energy"] / [V "voltage"]`
     * `[Wb "magnetic flux"] / [Ω "resistance"]`
     * `≈ 6,241,509,074,460,762,607.776 e`, where one elementary charge (`e`) is equal  to
       `1.602176634 * 10e-19 C`. This can also be expressed as `160.2176634 zC` (zeptocoulombs)
       of charge.
     * A capacitor of one farad can hold one coulomb at a drop of one volt.
     * One ampere-hour equals 3,600 coulombs

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): 2.2 Definition of the
         SI, p.13
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
     * The International System of Units BIPM Brochure 9th Edition (2019): Appendix 1, p.46
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
    """

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


class farad(UnitType):
    """
    The unit of electrical capacitance, or the measure of a body's ability to store an electric  charge.

    One farad is measured when one coulomb of charge is changed between the plates by one volt.
    Or, worded differently, 1 farad is measured when one coulomb of charge is stored across a
    voltage potential of one volt.

    Equalities
    ----------
    * `[C "electric charge"] / [V "voltage"]`
    * `[S "conductance"] * [s "second"]`
    * `[S "conductance"] / [Hz "frequency"]`
    * `[s "second"] / [Ω "resistance"]`
    * `[A "current"] * [s "seconds"] / [V "voltage"]`
    * `[C "charge"]^2 / [J "energy"]`
    * `[J "energy"] / [V "voltage"]^2`
    * `[s "seconds"]^2 / [H "inductance"]`
    * `[W "power"] * [s "seconds"] / [V "voltage"]^2`

    References
    ----------
    None.
    """

    symbol: ClassVar[str] = 'F'
    div_by = {
        "siemens": "second",
        "second": "siemens"
    }
    mul_by = {
        "frequency": "siemens",
        "ohm": "second",
        "volt": "coulomb"
    }


class henry(UnitType):
    """
    Unit of measure for electrical inductance.

    An inductance of one henry is measured when a changing current of 1A/s results in 1 volt
    measured between the to points.

    SI Definition
    -------------
    The henry is the inductance of a closed circuit in which an electromotive force of 1 volt is
    produced when the electric current in the circuit varies uniformly at the rate of 1 ampere per
    second.

    Equalities
    ----------
     * `[Ω "resistance"] * [s "second"]`
     * `[s "second"] * [Ω "resistance"]`
     * `[s "second"] / [S "conductance"]`
     * `[Wb "magnetic flux"] / [A "current"]`
     * `[Ω "resistance"] / [Hz "frequency"]`
     * `[V "voltage"] * [s "seconds"] / [A "current"]`
     * `[J "energy"] / [A "current"]^2`
     * `[s "seconds"]^2 / [F "capacitance]`

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): Appendix 1, p.46
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
     * Guide for the Use of the International System of Units (SI) (2008)
        https://physics.nist.gov/cuu/pdf/sp811.pdf
    """

    symbol = 'H'
    div_by = {
        "ohm": "second",
        "second": "ohm"
    }
    mul_by = {
        "ampere": "weber",
        "frequency": "ohm",
        "siemens": "second"
    }


class hertz(UnitType):
    """
    Unit of measure of frequency.

    One hertz is equal to one cycle per second. It can be thought of as the "reciprocal second".
    In angular frequency measured in radians per second, one hertz equals `2*pi rad/s`.

    Equalities
    ----------
     * `1 / [s "second"]`
     * `[Ω "resistance"] / [H "inductance"]`
     * `[S "conductance"] / [F "capacitance"]`
     * `[ω "angular frequency"] / (2*pi rad/s)`
    """

    symbol = 'Hz'
    mul_by = {
        "farad": "siemens",
        "henry": "ohm",
        "second": "float",
    }

    def to_angular(self) -> "RadPerSecond":
        """
        Convert a frequency in Hz into the angular frequency in radians.

        Returns
        -------
        `RadPerSec` — Angular frequency in radians/second

        See Also
        --------
        * `hz_from_afreq` -- reverse of this function

        Examples
        --------
        >>> # Not yet provided.

        References
        ----------
        None.
        """
        return RadPerSecond(6.28 * float(self))

    def to_wavelength(self) -> "metre":
        """
        Given a frequency in Hertz, return the wavelength in meters.

        Parameters
        ----------
        * `hz: float` — _description_

        Returns
        -------
        * `float` — _description_

        Examples
        --------
        >>> # Not yet provided.

        References
        ----------
        None.
        """
        return metre(3e5 / float(self))


class joule(UnitType):
    """
    Unit of energy.

    SI Definition
    -------------
    A unit of electrical energy equal to the work done when a current of one ampere is passed
    through a resistance of one ohm for one second.

    Equalities
    ----------
     * `[A "current"] * [Wb "magnetic flux"]`
     * `[V "voltage"] * [C "electric charge"]`
     * `[W "power"] * [s "second"]`

    References
    ----------
     * Guide for the Use of the International System of Units (SI) (2008)
           https://physics.nist.gov/cuu/pdf/sp811.pdf
    """

    symbol = 'J'
    div_by = {
        "ampere": "weber",
        "weber": "ampere",
        "coulomb": "volt",
        "volt": "coulomb",
        "watt": "second",
        "second": "watt"
    }


class metre(UnitType):
    """
    Primary unit of length.

    SI Definition
    -------------
    The length of the path traveled by light in a vacuum in `1/c` of a second, where
    c = `299 792 458`.
    """

    symbol = 'm'


class ohm(UnitType):
    """
    The unit of measure for electrical resistance.

    This can be described using Ohm's Law (`["voltage"] = ["current"] * ["resistance"]`), which
    can be rewritten to define 1 ohm as `[V "voltage"] / [A "current"]`.

    Definitions
    -----------
     * `1 / [S "conductance"]`
     * `[H "inductance"] * [Hz "frequency"]`
     * `[H "inductance"] / [s "second"]`
     * `[V "voltage"] / [A "current"]`
     * `[Wb "magnetic flux"] / [C "electric charge"]`
     * `[s "second"] / [F "capacitance"]`
     * `([J "energy"] * [s "seconds"]) / [C "charge"]^2`
     * `[V "volts"]^2 / [W "power"]`
     * `[W "power"] / [A "current"]^2`
     * `[J "energy"] / ([s "seconds"] * [A "current"]^2)`

    SI Formal Definition
    --------------------
    The ohm is the electric resistance between two points of a conductor when a
    constant potential difference of 1 volt, applied to these points, produces in the conductor a
    current of 1 ampere, the conductor not being the seat of any electromotive force.

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): Appendix 1, p.46
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf

    """

    symbol = 'Ω'
    div_by = {
        "henry": "frequency",
        "frequency": "henry"
    }
    mul_by = {
        "ampere": "volt",
        "coulomb": "weber",
        "farad": "second",
        "siemens": "float",
        "second": "henry"
    }


class RadPerSecond(UnitType):
    """Unit of angular frequency."""

    symbol = 'ω'

    def to_hertz(self) -> "hertz":
        """
        Get the frequency in cycles-per-second measured in hertz (Hz).

        Returns
        -------
        `Hertz` — Frequency measured in hertz (Hz)

        See Also
        --------
        * `afreq_from_hz` -- reverse of this function

        Examples
        --------
        >>> # Not yet provided.

        References
        ----------
        None.
        """
        return hertz(float(self) / 2 * 3.14)


class second(UnitType):
    """
    Unit of time.

    ```
    Quantity       Seconds
    --------   -----------
    Second               1
    Minute              60
    Hour             3 600
    Day             86 400
    Year        31 536 000
    ```

    SI Definition
    -------------
    The second is defined by taking the fixed numerical value of the caesium frequency, `ΔvCs`, the
    unperturbed ground-state hyperfine transition frequency of the caesium-133 atom, to be
    `9 192 631 770 Hz` which is equal to s-1.

    Equalities
    ----------
    * `1 / [Hz "frequency"]`
    * `[C "electric charge"] / [A "current"]`
    * `[F "capacitance"] * [Ω "resistance"]`
    * `[F "capacitance"] / [S "conductance"]`
    * `[H "inductance"] * [S "conductance"]`
    * `[H "inductance"] / [Ω "resistance"]`
    * `[J "energy"] / [W "power"]`
    * `[Wb "magnetic flux"] / [V "voltage"]`

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): p.130
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf

    """

    symbol = 's'
    mul_by = {
        "ampere": "coulomb",
        "frequency": "float",
        "ohm": "henry",
        "siemens": "farad",
        "volt": "weber",
        "watt": "joule"
    }
    div_by = {
        "farad": "ohm",
        "henry": "siemens",
        "ohm": "farad",
        "siemens": "henry"
    }


class siemens(UnitType):
    """
    The unit of conductance, susceptance, and admittance.

    These are the reciprocals of resistance, reactance, and impedance, meaning that
    `1℧ = 1/Ω`

    ```
    Quantity (Ω)     Reciprocal (℧)
    --------------   ---------------
    Resistance (R)   Conductance (G)
    Reactance  (X)   Susceptance (B)
    Impedance  (Z)   Admittance  (Y)
    ```

    One siemens of DC conductance is measured when an increase of electric current of one ampere
    is seen for every increase of one volt. Or in other words, 1 siemens = 1 ampere increase per 1
    volt increase.

    Equalities
    ----------
     * `[A "current"] / [V "voltage"]`
     * `1 / [Ω "resistance"]`
     * `[F "capacitance"] / [s "seconds"]`
     * `[F "capacitance"] * [Hz "frequency"]`
     * `[s "second"] / [H "inductance"]`

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): 2.3.4 Derived Units, p.23
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
    """

    symbol = '℧'
    div_by = {
        "farad": "frequency",
        "frequency": "farad"
    }
    mul_by = {
        "henry": "second",
        "ohm": "float",
        "volt": "ampere",
        "second": "farad",
    }


class volt(UnitType):
    """
    The unit of voltage (electric potential difference).

    Equalities
    ----------
     * `[A "current"] * [Ω "resistance"]`
     * `[A "current"] / [S "conductance"]`
     * `[C "electric charge"] / [F "capacitance"]`
     * `[J "energy"] / [C "electric charge"]`
     * `[W "power"] / [A "current"]`
     * `[Wb "magnetic flux"] * [Hz "frequency"]`
     * `[Wb "magnetic flux"] / [s "seconds"]`

    SI Formal Definition
    --------------------
    The volt is the potential difference between two points of a conducting wire carrying a
    constant current of 1 ampere, when the power dissipated between these points is equal to 1
    watt.

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): Appendix 1, p.46
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf

    """

    symbol = 'V'
    div_by = {
        'ohm': 'ampere',
        'ampere': 'ohm'
    }
    mul_by = {
        "ampere": "watt",
        "coulomb": "joule",
        "farad": "coulomb",
        "siemens": "ampere",
        "second": "weber"
    }


class watt(UnitType):
    """
    The unit of power, equal to 1 joule per second.

    This unit provides a means to quantify the rate of the transfer of energy.

    Definitions
    -----------
     * `[A "current"] * [V "voltage"]`
     * `[J "energy"] / [s "second"]`
     * `[J "energy"] [Hz "frequency"]`
     * `[A "current"]^2 * [R "resistance"]`
     * `[V "voltage"]^2 / [R "resistance"]`

    SI Formal Definition
    --------------------
    The watt is the power which in one second gives rise to energy of 1 joule.

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): Appendix 1, p.46
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
    """

    symbol = 'W'
    div_by = {
        'ampere': 'volt',
        'volt': 'ampere'
    }
    mul_by = {
        "second": "Joule"
    }


class weber(UnitType):
    """
    Unit of magnetic flux.

    It is also referred to as a volt-second.

    SI Definition
    -------------
    The weber is the magnetic flux which, linking a circuit of one turn, would produce in it an
    electromotive force of 1 volt if it were reduced to zero at a uniform rate in 1 second.

    Equalities
    ----------
     * `[A "current"] * [H "inductance"]`
     * `[C "electric charge"] * [Ω "resistance"]`
     * `[H "inductance"] * [A "current"]`
     * `[J "energy"] / [A "current"]`
     * `[Ω "resistance"] * [C "electric charge"]`
     * `[V "voltage"] * [s "second"]`
     * `[T "magnetic flux density"] / [m "meter"]^2`

    References
    ----------
     * The International System of Units BIPM Brochure 9th Edition (2019): Appendix 1, p.46
         https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
     * Guide for the Use of the International System of Units (SI) (2008)
         https://physics.nist.gov/cuu/pdf/sp811.pdf
    """

    symbol = 'Wb'
    div_by = {
        "ampere": "henry",
        "coulomb": "ohm",
        "henry": "ampere",
        "ohm": "coulomb",
        "volt": "second",
        "second": "volt"
    }
    mul_by = {
        "ampere": "joule"
    }


units = [UnitType, ampere, coulomb, farad, henry, hertz, joule,
         metre, ohm, RadPerSecond, siemens, second, volt, watt, weber]

__all__ = ['units', 'UnitType', 'ampere', 'coulomb', 'farad', 'henry', 'hertz', 'joule', 'metre',
           'ohm', 'RadPerSecond', 'siemens', 'second', 'volt', 'watt', 'weber']
