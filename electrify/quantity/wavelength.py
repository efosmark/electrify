import cmath
from typing import overload

from ..constants import SPEED_OF_LIGHT
from ..value.unit import *
from .quantity import Quantity

wavelength = Quantity[metre]("λ", "wavelength")

@wavelength.solution
def from_t(t: second) -> metre:
    """Get frequency in hertz from time in seconds."""
    return metre(1.0 / t / SPEED_OF_LIGHT)

@wavelength.solution
def from_frequency(frequency: hertz) -> metre:
    """
    Given a frequency measured in hertz, get the wavelength (λ) in metres.
    
    The formula for this is:
    
        λ = Hz / c
        
    Args:
        frequency (hertz): Frequency in hertz

    Returns:
        metre: Wavelength (λ) measured in metres.
    """
    return metre(frequency / SPEED_OF_LIGHT)

@wavelength.solution
def from_angular_f(angular_f: RadPerSecond) -> metre:
    """
    Given an angular frequency (ω) measured in rad/s, get the wavelength (λ) in metres.
    
    This is performed by dividing the angular frequency by 2π*c.

    Args:
        angular_f (RadPerSecond): _description_

    Returns:
        metre: Wavelength (λ) measured in metres.
    """
    return metre(angular_f / (cmath.pi * 2.0) / SPEED_OF_LIGHT)

@overload
def get_wavelength(*, t: second) -> metre: ...
@overload
def get_wavelength(*, f: hertz) -> metre: ...
@overload
def get_wavelength(*, angular_f: RadPerSecond) -> metre: ...

def get_wavelength(**kwargs: base_unit | complex | float) -> metre:
    """Calculate the wavelength in metres based on the quantities supplied."""
    return wavelength.get(**kwargs)
