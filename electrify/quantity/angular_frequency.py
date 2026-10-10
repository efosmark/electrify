from typing import overload

from ..constants import SPEED_OF_LIGHT
from ..types import *

def from_t(t: second) -> rad_per_sec:
    """Get angular frequency in rad/s from time in seconds."""
    return rad_per_sec()

def from_frequency(frequency: hertz) -> rad_per_sec:
    return rad_per_sec(frequency / SPEED_OF_LIGHT)

# @angular_frequency.solution
# def from_wavelength(wavelength: metre) -> RadPerSecond:
#   ...

@overload
def get_angular_frequency(*, t: second) -> rad_per_sec: ...
@overload
def get_angular_frequency(*, wavelength: metre) -> rad_per_sec: ...
@overload
def get_angular_frequency(*, frequency: hertz) -> rad_per_sec: ...
def get_angular_frequency(**kwargs: ElectricUnit | complex | float) -> rad_per_sec:
    """Calculate the angular frequency (ω) in rad/s based on the quantities supplied."""
    ...
