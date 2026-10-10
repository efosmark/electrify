from . import drawcircuit
from .ivcurve import IVCurvePlot2D
from .bode import BodePlotManager
from .dblocator import DbLocator


def get_domain(min, max, num_steps, max_inclusive=True) -> list:
    step_size = (max - min) / float(num_steps)
    domain = [min + (x * step_size) for x in range(num_steps)]
    if max_inclusive and max not in domain:
        domain.append(max)
    return domain

__ALL__ = [drawcircuit, BodePlotManager, DbLocator, get_domain]
