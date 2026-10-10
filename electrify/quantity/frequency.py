import cmath
from typing import overload

from electrify.constants import SPEED_OF_LIGHT
from ..types import *

def from_t(t: second) -> hertz:
    """Get frequency in hertz from time in seconds."""
    return hertz(1.0 / second(t))

def from_LC(L: henry, C: farad) -> hertz:
    r"""
    Get frequency in hertz from inductance in henrys and capacitance in farads.
    
    .. math::

      f_R = \frac{1}{2 \pi \sqrt{LC}}

    """
    return hertz(1.0 / (2.0 * cmath.pi * cmath.sqrt(farad(C) * henry(L))))

def from_wavelength(wavelength: metre) -> hertz:
    """
    Given a wavelength (λ) measured in metres, get the frequency in hertz.
    
    The formula for this is:
    
        c / λ = Hz
        
    Args:
        wavelength (metre): Wavelength in metres.

    Returns:
        hertz: Frequency measured in hertz.
    """
    return hertz(SPEED_OF_LIGHT / wavelength)

def from_angular_f(angular_f: rad_per_sec) -> hertz:
    """
    Given an angular frequency (ω) measured in rad/s, get the frequency measured in hertz.
    
    This is performed by dividing the angular frequency by 2π since one full revolution is equal
    to 2π. For example, 2π rad/s = 1 Hz

    Args:
        angular_f (RadPerSecond): _description_

    Returns:
        hertz: Frequency measured in hertz.
    """
    return hertz(angular_f / (cmath.pi * 2.0))

@overload
def get_frequency(*, t: second) -> hertz: ...
@overload
def get_frequency(*, L: henry, C: farad) -> hertz: ...
@overload
def get_frequency(*, wavelength: metre) -> hertz: ...
@overload
def get_frequency(*, angular_f: rad_per_sec) -> hertz: ...

def get_frequency(**kwargs: ElectricUnit | complex | float) -> hertz:
    """Calculate the frequency in hertz based on the quantities supplied."""
    ...
