import numpy as np
from ..common import parallel_resistance


def rc_filter_cutoff(RS: float, RL: float, C: float) -> float:
    """
    Determine the 3-dB cutoff for a RC filter with the given parameters.

    ```
        [RS]---+----+
               |    |
              [C]  [RL]
               |    |
               G    G
    ```

    > The 3-dB point occurs when the reactance of the capacitor is equal to
    the parallel combination of the source and load resistances.

    Parameters
    ----------
     * `RS: float` — _description_
     * `RL: float` — _description_
     * `C: float` — _description_

    Returns
    -------
     * `float` — _description_

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
        Hardy, J.K. (1978). Filters. High frequency circuit design (pp. 99-101).
             Reston Publishing, LLC.
    """
    R = parallel_resistance([RS, RL])
    return 1.0 / (2 * np.pi * R * C)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
