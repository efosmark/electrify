"""A single-port model of a physical resistor."""
from typing import Optional

from .network import OnePortNetwork
from .property import NegativePole, PositivePole, Voltage, Resistance, Current
from ..value.unit import *

class Source(OnePortNetwork):
    ...

class VoltageSource(Source):

    voltage: Voltage
    series_resistance: Resistance
    
    v_out: PositivePole
    ground: NegativePole

    def __init__(
        self,
        voltage: volt,
        series_resistance: ohm
    ):
        Source.__init__(self)
        self.voltage = Voltage(voltage)
        self.series_resistance = Resistance(series_resistance, "self_impedance")

        self.v_out, self.ground = self.port(1)
        
        self.add_edge(self.ground, self.voltage)
        self.add_edge(self.voltage, self.series_resistance)
        self.add_edge(self.series_resistance, self.v_out)  


class CurrentSource(Source):

    current: Current
