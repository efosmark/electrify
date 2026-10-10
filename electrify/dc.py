import cmath
import logging
from typing import Sequence, SupportsComplex, TypeVar, overload

from electrify import ac
from .types import *
from .constants import BOLTZMANN_CONSTANT, ELEMENTARY_CHARGE

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def voltage_divider(V_in: volt, R1: ohm, R2: ohm) -> volt:
    """
    Return the output of a two-resistor voltage divider.

    It follows this topology:
    ```
     V_in ═════╗
            ╭──╨─╮
            │ R1 │
            ╰──╥─╯
               ╠════ V_out
            ╭──╨─╮
            │ R2 │
            ╰──╥─╯
               ║
              GND
    ```

    Args:
        V_in: Input voltage.
        R1: Series resistance from the source to the output node.
        R2: Shunt resistance from the output node to ground.

    Returns:
        The voltage at the output node.

    Examples:
        >>> voltage_divider(volt(12), ohm(k=2), ohm(k=1))
        volt(4.0)
    """
    if cmath.isinf(R2) or R2 is None or R1 == 0:
        return volt(V_in)
    elif R2 == 0:
        return volt(0)
    elif R1 + R2 == 0:
        return volt(0)
    return volt(complex(V_in) * (R2 / (R2 + R1)))

def current_divider(current: ampere, Z_branch: ohm, Z_total: ohm) -> ampere:
    """
    Return the current through one branch of a parallel network.

    The branch current is computed from total current multiplied by the ratio of
    total impedance to branch impedance.

    Args:
        current: Total current entering the parallel network.
        Z_branch: Impedance of the branch being measured.
        Z_total: Equivalent impedance of the full parallel network.

    Returns:
        Current through the selected branch.

    Examples:
        >>> current_divider(ampere(1), ohm(100), ohm(50))
        ampere(0.5)
    """
    if Z_branch == 0:
        return ampere(current)
    elif Z_branch is None:
        return ampere(0)
    return ampere(complex(current) * (Z_total / Z_branch))


def voltage_drop(V_in: volt, R_value: ohm, R_total: ohm) -> volt:
    """
    Given a series of resistors, determine the voltage drop found across one of them.

    Args:
        V_in (volt): Input voltage
        R_value (ohm): Value of the resistor we're looking at
        R_total (ohm): Total sum of the resistance of the entire series

    Returns:
        volt: The drop in voltage across R_value

    Examples:
        >>> voltage_drop(volt(12), ohm(1), ohm(3))
        volt(4.0)
    """
    return volt((R_value/R_total) * V_in)

_T = TypeVar("_T", bound=ElectricUnit)
@overload
def harmonic_sum(values: Sequence[_T]) -> _T:...
@overload
def harmonic_sum(values: Sequence[complex]) -> complex:...
def harmonic_sum(values: Sequence[_T|complex]):
    """
    Return the reciprocal sum for a sequence of values.

    This is the arithmetic behind parallel resistance and series capacitance.

    Examples:
        >>> harmonic_sum([ohm(100), ohm(100)])
        ohm(50.0)
    """
    try:
        return 1.0 / sum([(1.0 / n) for n in values])
    except ZeroDivisionError:
        return complex(0.0)

def shockley_diode_equation(
  voltage: volt,
  saturation_current: ampere,
  quality_factor: float = 1.0,
  thermal_voltage: volt = volt(0.026)
  ) -> ampere:
    """
    Return diode current from the Shockley diode equation.

    Args:
        voltage: Voltage across the diode.
        saturation_current: Reverse saturation current.
        quality_factor: Ideality factor, usually between 1 and 2.
        thermal_voltage: Thermal voltage for the junction temperature.

    Returns:
        Forward current predicted by the ideal diode model.

    Examples:
        >>> current = shockley_diode_equation(volt(0.65), ampere(1e-12))
        >>> str(current)
        '72mA'
    """
    return ampere(
      saturation_current
      * (cmath.exp(voltage / (quality_factor * thermal_voltage)) - 1.0)
    )

def thermal_voltage(temperature: float) -> volt:
  r"""
    The characteristic voltage that describes the relationship between the flow of electric current
    and the electrostatic potential across a p-n junction.
    
    Equal approximately to ``25.852 mV`` at ``300 K``, which is often rounded to ``26mV`` at room 
    temperature in order to simplify equations.

    At an arbitrary temperature, it is a known constant:
    
    .. math::

        V_{T} = \frac{kT}{q}

    where,

      .. hlist::
         * :math:`k` is the :term:`Boltzmann constant`
         * :math:`T` is the absolute temperature of the ``p-n`` junction
        * :math:`q` is the :term:`elementary charge`

    Args:
        temperature: Absolute junction temperature in kelvin.

    Returns:
        Thermal voltage for the supplied temperature.
    
    Examples:
      >>> str(thermal_voltage(300))
      '25.9mV'
  """
  return volt(BOLTZMANN_CONSTANT * temperature / ELEMENTARY_CHARGE)
