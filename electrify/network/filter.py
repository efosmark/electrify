import math
from typing import Optional
from electrify.ac import hz_center_from_bw, magnitude
from electrify.network.net import Edge, Net, Side
from electrify.types import *
from electrify.constants import BUTTERWORTH_COEF_MAX_FLAT
from electrify.component import C, L
from .network import TwoPortNetwork


def butterworth_shunt_value(num_elements:int, n:int, cutoff:hertz, z0:ohm=ohm(50)) -> float:
    coef = BUTTERWORTH_COEF_MAX_FLAT[num_elements][n]
    return magnitude(coef / z0 / (2 * math.pi * cutoff))

def butterworth_series_value(num_elements:int, n:int, cutoff:hertz, z0:ohm=ohm(50)) -> float:
    coef = BUTTERWORTH_COEF_MAX_FLAT[num_elements][n]
    return magnitude((coef * z0) / (2 * math.pi * cutoff))



class LowPassFilter(TwoPortNetwork):
    def __init__(
        self,
        cutoff: hertz,
        num_elements: int,
        characteristic_impedance:ohm = ohm(50)
    ):
        TwoPortNetwork.__init__(self)
        self.cutoff = cutoff
        self.num_elements = num_elements
        self.characteristic_impedance = characteristic_impedance
        self.ground = Edge(self.ports[1], Side.B)
        self._build_network()
    
    def _build_network(self):
        p1, p2 = self.ports[1], self.ports[2]
        
        self.connect(p2.neg, p1.neg)
        prev = Edge(p1, Side.A)

        for i in range(self.num_elements):
            if i % 2 == 0:
                cap = C(butterworth_shunt_value(self.num_elements, i, self.cutoff))
                self.connect(prev, cap)
                self.connect(cap, self.ground)
            else:
                ind = L(butterworth_series_value(self.num_elements, i, self.cutoff))
                self.connect(prev, ind)
                prev = Edge(ind, Side.B)
        self.connect(prev, p2.pos)
        

class HighPassFilter(TwoPortNetwork):
    def __init__(
        self,
        cutoff: hertz,
        num_elements: int,
        characteristic_impedance:ohm = ohm(50)
    ):
        TwoPortNetwork.__init__(self)
        self.cutoff = cutoff
        self.num_elements = num_elements
        self.characteristic_impedance = characteristic_impedance
        self.ground = Edge(self.ports[1], Side.B)
        self._build_network()
    
    def _build_network(self):
        p1, p2 = self.ports[1], self.ports[2]
        
        self.connect(p2.neg, p1.neg)
        prev = Edge(p1, Side.A)

        for i in range(self.num_elements):
            val = BUTTERWORTH_COEF_MAX_FLAT[self.num_elements][i]

            if i % 2 == 0:
                ind = L(magnitude(1 / ((val / self.characteristic_impedance) * 2 * math.pi * self.cutoff)))
                self.connect(prev, ind)
                self.connect(ind, self.ground)
            else:
                cap = C(magnitude(1 / ((val * self.characteristic_impedance) * 2 * math.pi * self.cutoff)))
                self.connect(prev, cap)
                prev = Edge(cap, Side.B)
        self.connect(prev, p2.pos)


class BandPassFilter(TwoPortNetwork):

    def __init__(self, upper, lower, num_elements=5, R0=ohm(50)):
        super().__init__()
        upper = upper * 2 * math.pi
        lower = lower * 2 * math.pi

        self.ground = Edge(self.ports[1], Side.B)
        self.num_elements = num_elements
        self.characteristic_impedance = R0
        self.center_frequency = hz_center_from_bw(lower, upper)
        self.bandwidth = upper - lower

        p1, p2 = self.ports[1], self.ports[2]
        self.connect(p2.neg, p1.neg)
        prev = Edge(p1, Side.A)
        
        for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[num_elements]):
            if i % 2 == 0:
                ind = L((val * R0) / self.bandwidth)
                cap = C(self.bandwidth / (self.center_frequency**2 * (val / R0)))
                prev = Edge(self.series(prev, ind, cap), Side.B)
            else:
                cap = C((val * R0) / self.bandwidth)
                ind = L(self.bandwidth / (self.center_frequency**2 * (val / R0)))
                self.series(cap, self.ground)
                self.series(ind, self.ground)



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
