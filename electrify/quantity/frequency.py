import cmath
from typing import overload
from ..value.unit import *
from .quantity import Quantity

f = frequency = Quantity[hertz]("f", "frequency")


@f.solution
def from_t(t: second) -> hertz:
    """Get frequency in hertz from time in seconds."""
    return hertz(1.0 / second(t))


@f.solution
def from_LC(L: henry, C: farad) -> hertz:
    """Get frequency in hertz from inductance in henrys and capacitance in farads."""
    return hertz(1.0 / (2.0 * cmath.pi * cmath.sqrt(farad(C) * henry(L))))


@f.solution
def from_wavelength(wavelength: metre) -> hertz:
    return hertz()


@f.solution
def from_angular_f(angular_f: RadPerSecond) -> hertz:
    return hertz()


@overload
def get_frequency(*, t: second) -> hertz: ...
@overload
def get_frequency(*, L: henry, C: farad) -> hertz: ...
@overload
def get_frequency(*, wavelength: metre) -> hertz: ...
@overload
def get_frequency(*, angular_f: RadPerSecond) -> hertz: ...


def get_frequency(**kwargs: base_unit | complex | float) -> hertz:
    """Calculate the frequency in hertz based on the quantities supplied."""
    return f.get(**kwargs)
