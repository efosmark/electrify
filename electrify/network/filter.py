import cmath
from typing import Optional
from electrify.constants import BUTTERWORTH_COEF_MAX_FLAT
from electrify.network.property import Capacitance, Inductance, Resistance
from electrify.value.unit import *
from .network import NegativePole, Property, TwoPortNetwork


class LowPassFilter(TwoPortNetwork):
    def __init__(
        self,
        cutoff: hertz,
        num_elements: int,
        characteristic_impedance:ohm = ohm(50),
        com: Optional[NegativePole] = None
    ):
        TwoPortNetwork.__init__(self)
        if com is not None:
            self.port(1).neg = com 
        self.cutoff = cutoff
        self.num_elements = num_elements
        self.characteristic_impedance = characteristic_impedance
        self._build_network()

    def _build_network(self):
        self.com = Property[None](None, "GND")
        
        p1 = self.port(1)
        p2 = self.port(2)
        
        self.add_edge(p2.neg, p1.neg)
        
        source_resistance = Resistance(ohm(50))
        self.add_edge(p1.pos, source_resistance)
        prev = source_resistance

        for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[self.num_elements]):
            if i % 2 == 0:
                C = val / self.characteristic_impedance / (2 * cmath.pi * self.cutoff)
                cap = Capacitance(farad(C))
                self.add_series([prev, cap, p1.neg])
            else:
                L = (val * self.characteristic_impedance) / (2 * cmath.pi * self.cutoff)
                ind = Inductance(henry(L))
                self.add_series([prev, ind])
                prev = ind
        self.add_edge(prev, p2.pos)
        

# class HighPassFilter(SubCircuit):

#     def __init__(self, cutoffFrequency, num=5, R0=50, seriesFirst=False, name=None):
#         if name is None:
#             name = "HPF_"+str(hex(id(self)))[-4:]
#         SubCircuit.__init__(self, name=name)
#         self._numComponents = num
#         self._characteristicImpedance = R0
#         self._cutoffFrequency = cutoffFrequency

#         for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[num]):
#             L = val * R0
#             C = val / R0
#             if i % 2 == int(seriesFirst):
#                 self.series(Capacitor(1 / (L * 2 * np.pi * cutoffFrequency)))
#             else:
#                 self.shunt(Inductor(1 / (C * 2 * np.pi * cutoffFrequency)))
#         # self.end()


# class BandPassFilter(SubCircuit):

#     def __init__(self, upper, lower, num=5, R0=50, seriesFirst=False, name=None):
#         if name is None:
#             name = "BPF_"+str(hex(id(self)))[-4:]
#         SubCircuit.__init__(self, name=name)
#         upper = upper * 2 * np.pi
#         lower = lower * 2 * np.pi

#         self._numComponents = num
#         self._characteristicImpedance = R0
#         self._centerFrequency = f0_from_bandwidth(lower, upper)
#         self._bandwidth = upper - lower

#         for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[num]):
#             L = val * R0
#             C = val / R0
#             if i % 2 == int(seriesFirst):
#                 self.series(
#                     Inductor(L / self._bandwidth),
#                     Capacitor(self._bandwidth / (self._centerFrequency**2 * L))
#                 )
#             else:
#                 self.shunt(Capacitor(C / self._bandwidth))
#                 self.shunt(Inductor(self._bandwidth /
#                            (self._centerFrequency**2 * C)))
#         # self.end()

#     def bandwidth(self):
#         return self._bandwidth

#     def centerFrequency(self):
#         return self._centerFrequency


# class BandStopFilter(SubCircuit):

#     def __init__(self, upper, lower, num=5, R0=50, seriesFirst=False, name=None):
#         if name is None:
#             name = "BSF_"+str(hex(id(self)))[-4:]
#         SubCircuit.__init__(self, name=name)
#         upper = upper * 2 * np.pi
#         lower = lower * 2 * np.pi

#         self._numComponents = num
#         self._characteristicImpedance = R0
#         self._centerFrequency = f0_from_bandwidth(lower, upper)
#         self._bandwidth = upper - lower

#         for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[num]):
#             L = val * R0
#             C = val / R0
#             if i % 2 == int(seriesFirst):
#                 self.parallel(
#                     Capacitor(1 / (self._bandwidth * L), ESR=2.0),
#                     Inductor((self._bandwidth * L) /
#                              self._centerFrequency**2, ESR=2.0)
#                 )
#             else:
#                 self.shunt(
#                     Inductor(1 / (self._bandwidth * C), ESR=2.0),
#                     Capacitor((self._bandwidth * C) /
#                               self._centerFrequency**2, ESR=2.0)
#                 )
#         # self.end()

#     def bandwidth(self):
#         return self._bandwidth

#     def centerFrequency(self):
#         return self._centerFrequency
