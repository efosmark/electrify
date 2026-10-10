"""
Common electrical formulas.

Examples
--------
>>> from electrify.types import farad, ohm
>>> sum_series([ohm(10), ohm(20)])
ohm(30.0)
>>> sum_parallel([ohm(100), ohm(100)])
ohm(50.0)
>>> str(sum_parallel([farad(n=47), farad(n=100)]))
'147nF'

"""
from typing import Sequence, TypeVar, cast, overload
from .types import *

def _infer_sum_type(values: Sequence) -> type[ohm] | type[farad] | type[henry] | type[siemens]:
    if len(values) == 0:
        raise ValueError("Cannot infer sum type on an empty sequence.")
    if not isinstance(values[0], (ohm, farad, henry, siemens)):
        raise TypeError(
            "Unit cannot be inferred."
            "Either ensure the sequence only has ohm|farad|henry, or specify sum_type."
        )
    return type(values[0])

_T = TypeVar("_T", bound=ElectricUnit)

@overload
def harmonic_sum(values: Sequence[_T]) -> _T:...
@overload
def harmonic_sum(values: Sequence[complex]) -> complex:...
def harmonic_sum(values: Sequence[_T|complex]) -> _T|complex:
    """
    Given a list of values, get the reciprocal of the sum of the reciprocal of all values.

    Args:
        values (Sequence[complex]): Sequence of numeric values

    Returns:
        complex: Inverse of the sum of the inverse of each value
    """
    try:
        return cast(_T, 1.0 / sum([1.0 / n for n in values]))
    except ZeroDivisionError:
        return 0.0

def sum_parallel_resistance(values: Sequence[ohm]) -> ohm:
    return ohm(harmonic_sum(values))

sum_parallel_reactance = sum_parallel_resistance
sum_parallel_impedance = sum_parallel_resistance

def sum_parallel_inductance(values: Sequence[complex]) -> henry:
    return henry(harmonic_sum(values))
def sum_parallel_capacitance(values: Sequence[complex]) -> farad:
    return farad(sum(values))
def sum_parallel_conductance(values: Sequence[complex]) -> siemens:
    return siemens(sum(values))

sum_parallel_susceptance = sum_parallel_conductance
sum_parallel_admittance = sum_parallel_conductance

@overload
def sum_parallel(values: Sequence[ohm]) -> ohm: ...
@overload
def sum_parallel(values: Sequence[farad]) -> farad: ...
@overload
def sum_parallel(values: Sequence[henry]) -> henry: ...
def sum_parallel(values: Sequence, sum_type=None):
    """
    Perform a parallel sum of an arbitrary sequence of quantities.

    Since the type of values cannot be inferred from a sequence type, ``sum_type`` must be provided
    as well, with a value of ``ohm``, ``farad``, or ``henry``.
    """
    if sum_type is None:
        sum_type = _infer_sum_type(values)

    if sum_type is ohm:
        return sum_parallel_resistance(values)
    elif sum_type is henry:
        return henry(harmonic_sum(values))
    elif sum_type is farad:
        return farad(sum(values))
    raise TypeError("sum_type must be ohm, henry, or farad.")

# END PARALLEL
# BEGIN SERIES

def sum_series_resistance(values: Sequence[complex]) -> ohm:
    return ohm(sum(values))

sum_series_reactance = sum_series_resistance
sum_series_impedance = sum_series_resistance

def sum_series_inductance(values: Sequence[complex]) -> henry:
    return henry(sum(values))
def sum_series_capacitance(values: Sequence[complex]) -> farad:
    return farad(harmonic_sum(values))
def sum_series_conductance(values: Sequence[complex]) -> siemens:
    return siemens(harmonic_sum(values))

sum_series_susceptance = sum_series_conductance
sum_series_admittance = sum_series_conductance

@overload
def sum_series(values: Sequence[ohm]) -> ohm: ...
@overload
def sum_series(values: Sequence[farad]) -> farad: ...
@overload
def sum_series(values: Sequence[henry]) -> henry: ...
def sum_series(values: Sequence, sum_type=None):
    """
    Perform a series sum of an arbitrary sequence of quantities.

    Since the type of values cannot be inferred from a sequence type, ``sum_type`` must be provided
    as well, with a value of ``ohm``, ``farad``, or ``henry``.

    ** Example **

    >>> from electrify.types import farad, ohm

    >>> cap_values : list[farad] = [farad(u=10), farad(n=100), farad(n=10)]
    >>> x = sum_series(cap_values)
    >>> str(x)
    '9.1nF'

    >>> resistor_values : list[ohm] = [ohm(k=5), ohm(10), ohm(M=1)]
    >>> sum_series(resistor_values)
    ohm(1005010.0)

    """
    if sum_type is None:
        sum_type = _infer_sum_type(values)

    if sum_type is ohm:
        return ohm(sum(values))
    elif sum_type is henry:
        return henry(sum(values))
    elif sum_type is farad:
        return farad(harmonic_sum(values))
    raise TypeError("sum_type must be ohm, henry, or farad.")
