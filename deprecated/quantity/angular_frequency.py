from typing import overload

from ..constants import SPEED_OF_LIGHT
from ..value.unit import *
from .quantity import Quantity

angular_frequency = Quantity[RadPerSecond]("ω", "angular_frequency")

@angular_frequency.solution
def from_t(t: second) -> RadPerSecond:
    """Get angular frequency in rad/s from time in seconds."""
    return RadPerSecond()

@angular_frequency.solution
def from_frequency(frequency: hertz) -> RadPerSecond:
    return RadPerSecond(frequency / SPEED_OF_LIGHT)

# @angular_frequency.solution
# def from_wavelength(wavelength: metre) -> RadPerSecond:
#   ...

@overload
def get_angular_frequency(*, t: second) -> RadPerSecond: ...
@overload
def get_angular_frequency(*, wavelength: metre) -> RadPerSecond: ...
@overload
def get_angular_frequency(*, frequency: hertz) -> RadPerSecond: ...

def get_angular_frequency(**kwargs: base_unit | complex | float) -> RadPerSecond:
    """Calculate the angular frequency (ω) in rad/s based on the quantities supplied."""
    return angular_frequency.get(**kwargs)
