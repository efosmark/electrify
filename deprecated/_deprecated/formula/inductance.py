from ..value import *
import numpy as np

from .rf import magnitude


def mutual_inductance(aiding_inductance=0, opposing_inductance=0):
    return (aiding_inductance - opposing_inductance) / 4.0


def inductive_coupling_coefficient(
    L_first: henry | float,
    L_second: henry | float,
    L_mutual: henry | float
) -> float:
    """
    Get the coefficient of two inductively-coupled RF coils that are providing transformer action.

    All arguments must share the same unit and magnitude.

    Args:
     * `L_first: henry|float` — Self-inductance of the first inductor, in Henrys (H)
     * `L_second: henry|float` — Self-inductance of the second inductor, in Henrys (H)
     * `L_mutual: henry|float` — Mutual-inductance of the interacting fields, in Henrys (H)

    Returns:
     * `float` — The coupling coefficient describing th

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """
    return float(L_mutual) / np.sqrt(L_first * float(L_second))
