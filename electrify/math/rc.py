import numpy as np
from .common import parallel_resistance


def rc_filter_cutoff(RS, RL, C):
    '''

    References:
        Hardy, J.K. (1978). Filters. High frequency circuit design (pp. 99-101).
             Reston Publishing, LLC.
    '''
    R = parallel_resistance(RS, RL)
    return 1 / (2 * np.pi * R * C)
