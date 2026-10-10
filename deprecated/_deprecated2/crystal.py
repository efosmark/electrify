"""A single-port model of a crystal."""
from electrify.quantity import frequency
from .network import OnePortNetwork
from ..value.unit import *
import math

class Crystal(OnePortNetwork):
    """Representation of a crystal as a single-port network."""
    
    body_capacitance: farad
    series_inductance: henry
    series_capacitance: farad
    series_resistance: ohm

    def __init__(
        self,
        body_capacitance: farad,
        series_capacitance: farad,
        series_inductance: henry,
        series_resistance: ohm
    ):
        """
        Create a new single-port network crystal.

        Args:
            body_capacitance (farad): _description_
            series_capacitance (farad): _description_
            series_inductance (henry): _description_
            series_resistance (ohm): _description_
        """
        OnePortNetwork.__init__(self)
        self.body_capacitance = body_capacitance
        self.series_capacitance = series_capacitance
        self.series_inductance = series_inductance
        self.series_resistance = series_resistance
        self._build_network()

    def _build_network(self):
        self.clear()
        
        pole_A = +self.port(1)
        pole_B = -self.port(1)
        
        self.add_series([
          pole_A,
          self.series_inductance,
          self.series_capacitance,
          self.series_resistance,
          pole_B
          ])
        
        self.add_parallel([self.body_capacitance], start=pole_A, end=pole_B)


    def series_resonance(self) -> hertz:
      """
      Get the series-resonant frequency of the crystal.
      
      This looks at the series inductance and series capacitance of the crystal.

      Returns:
          hertz: The series-resonant frequency.
      """
      return frequency.from_LC(self.series_inductance, self.series_capacitance)


    def parallel_resonance(self) -> hertz:
      """
      Get the parallel-resonant frequency of the crystal.
      
      This looks at the series resonance with the ratio of the series capacitance and parallel
      capacitance.

      Returns:
          hertz: The parallel-resonant frequency.
      """
      return hertz(
        self.series_resonance() 
        * math.sqrt(
          1 + (self.series_capacitance/self.body_capacitance)
        )
      )


crystal_11MHz = Crystal(
    series_inductance=henry(milli=25),
    series_capacitance=farad(pico=0.008),
    series_resistance=ohm(30),
    body_capacitance=farad(pico=2)
)

crystal_5MHz = Crystal(
    series_inductance=henry(0.098),
    series_capacitance=farad(pico=0.0134),
    series_resistance=ohm(12.8),
    body_capacitance=farad(pico=2.275)
)
