"""A single-port model of a physical resistor."""
from typing import Optional, Final

from .network import OnePortNetwork, Property
from ..value.unit import *


class Resistor(OnePortNetwork):
    """Physical representation of a resistor as a single-port network."""

    num_poles: Final[int] = 2

    resistance: Property[ohm]
    body_capacitance: Property[farad]
    interlead_capacitance: Property[farad]
    lead_inductance: Property[henry]
    internal_inductance: Property[henry]

    def __init__(
        self,
        resistance: ohm,
        body_capacitance: Optional[farad] = None,
        interlead_capacitance: Optional[farad] = None,
        lead_inductance: Optional[henry] = None,
        internal_inductance: Optional[henry] = None
    ):
        """
        Create a new single-port network resistor.

        This model allows for several physical properties to be specified, but the only required
        property is ``resistance``.

        Args:
            resistance (ohm): The resistance in ohms.
            body_capacitance (farad, optional): Internal body capacitance.
            interlead_capacitance (farad, optional): Capacitance between the component leads.
            lead_inductance (henry, optional): Inductance of each individual component lead.
            internal_inductance (henry, optional): Internal inductance in series with resisistance.
        """
        OnePortNetwork.__init__(self)
        self.resistance = Property[ohm](resistance, "resistance")
        self.body_capacitance = Property[farad](body_capacitance, "C_body")
        self.interlead_capacitance = Property[farad](interlead_capacitance, "C_interlead")
        self.internal_inductance = Property[henry](internal_inductance, "L_internal")
        self.lead_inductance_A = Property[henry](lead_inductance, "L_leadA")
        self.lead_inductance_B = Property[henry](lead_inductance, "L_leadB")
        self._build_network()

    def _build_network(self):
        self.clear()

        pole_A = +self.port(1)
        pole_B = -self.port(1)

        if self.interlead_capacitance.value() is not None:
            self.add_series([pole_A, self.interlead_capacitance, pole_B])

        if self.lead_inductance_A.value() is not None:
            pole_A = self.add_series([pole_A, self.lead_inductance_A])
            pole_B = self.add_series([pole_B, self.lead_inductance_B])

        if self.body_capacitance.value() is not None:
            self.add_parallel([self.body_capacitance], start=pole_A, end=pole_B)

        if self.internal_inductance.value() is not None:
            self.add_series([pole_A, self.internal_inductance, self.resistance, pole_B])
        else:
            self.add_series([pole_A, self.resistance, pole_B])
