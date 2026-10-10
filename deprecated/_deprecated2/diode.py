"""A single-port model of a physical resistor."""
from typing import Optional, Final

from .network import OnePortNetwork, Property
from ..value.unit import *


class IdealDiode(OnePortNetwork):
    saturation_current: Property[ohm]

    def __init__(self, saturation_current:Optional[ohm] = None):
        """ """
        if saturation_current is not None:
            self.saturation_current = Property[ohm](saturation_current, "saturation_current")
