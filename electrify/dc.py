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
    Given two resistance values in Ohms, return the divided voltage.

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

    Parameters
    ----------
     * `V_in: V` -- Input voltage
     * `R1: R` -- Series resistance, in Ohms (Ω)
     * `R2: R` -- Shunt resistance, in Ohms (Ω)
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
    Given a current at a branch, determine how much of it will go to a branch.

    Args:
        current (ampere): _description_
        Z_branch (ohm): _description_
        Z_total (ohm): _description_

    Returns:
        ampere: _description_
    """
    if Z_branch == 0:
        return ampere(current)
    elif Z_branch is None:
        return ampere(0)
    return ampere(complex(current) * (Z_total / Z_branch))


def voltage_drop(V_in:volt, R_value:ohm, R_total:ohm) -> volt:
    """
    Given a series of resistors, determine the voltage drop found across one of them.

    Args:
        V_in (volt): Input voltage
        R_value (ohm): Value of the resistor we're looking at
        R_total (ohm): Total sum of the resistance of the entire series

    Returns:
        volt: The drop in voltage across R_value
    """
    return volt((R_value/R_total) * V_in)

_T = TypeVar("_T", bound=ElectricUnit)
@overload
def harmonic_sum(values: Sequence[_T]) -> _T:...
@overload
def harmonic_sum(values: Sequence[complex]) -> complex:...
def harmonic_sum(values: Sequence[_T|complex]):
    """Given a list of values, get the reciprocal of the sum of the reciprocal of all values."""
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
    """_summary_

    Args:
        voltage (volt): _description_
        saturation_current (ampere): _description_
        quality_factor (float, optional): _description_. Defaults to 1.0.
        thermal_voltage (volt, optional): _description_. Defaults to volt(0.026).

    Returns:
        ampere: _description_
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
         * :math:`q` isP the :term:`elementary charge`

    Args:
        temperature (float): _description_

    Returns:
        volt: _description_
    
    Examples:
      >>> d
  """
  return volt(BOLTZMANN_CONSTANT * temperature / ELEMENTARY_CHARGE)
