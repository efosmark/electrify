"""
Elements pertaining to circuit loads / sinks.

Loads should behave like single-port elements, with a hidden reference to ground.
#TODO: This can be done better.
"""
from ..value import *
from .node import Node
from .element import Element


class ResistiveLoad(Element):
    """Element representing a circuit load that's perfectly resistive."""

    resistance: ohm
    gnd: Node | None

    def __init__(self, resistance: ohm | float, gnd: Node | None = None, **kwargs):
        """Initialize a resistive load with the given resistance in ohms."""
        super().__init__(**kwargs)
        self._resistance = ohm(resistance)
        self.gnd = gnd

    def __str__(self):
        """Get a string representation of the resistive load."""
        return '<Load R={}>'.format(self._resistance)
