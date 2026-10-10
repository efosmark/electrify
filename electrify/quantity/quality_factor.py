import math


def quality_factor(X: float, R: float) -> float:
    """
    Provide the quality factor (Q), AKA the figure of merit.

    Since Q is based on the reactance, it is frequency-dependent.

    Args:
     * `X`:`float` — Reactance as a float value
     * `R`:`float` — Resistance

    Returns:
     * `float` — Quality Factor

    Examples
    --------
    >>> # Not yet implemented

    References
    ----------
    None.
    """
    if R == 0:
        return math.inf
    return X / R
