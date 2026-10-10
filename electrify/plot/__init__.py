from .ivcurve import IVCurvePlot2D
from .bode import BodePlotManager
from .dblocator import DbLocator


def get_domain(start, stop, num_steps, max_inclusive=True) -> list:
    """
    Generate an evenly spaced numeric domain.

    Args:
        start: First value in the domain.
        stop: Upper bound for the domain.
        num_steps: Number of intervals before the optional final stop value.
        max_inclusive: Append ``stop`` when it is not already present.

    Examples:
        >>> get_domain(0, 1, 4)
        [0.0, 0.25, 0.5, 0.75, 1]
    """
    step_size = (stop - start) / float(num_steps)
    domain = [start + (x * step_size) for x in range(num_steps)]
    if max_inclusive and stop not in domain:
        domain.append(stop)
    return domain

__all__ = ["BodePlotManager", "DbLocator", "IVCurvePlot2D", "get_domain"]
