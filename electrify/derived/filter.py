import numpy as np

from ..math import f0_from_bandwidth
from ..circuit import SubCircuit
from ..component import Resistor, Inductor, Capacitor


BUTTERWORTH_COEF_MAX_FLAT = {
    1: [2.0000],
    2: [1.414, 1.414],
    3: [1, 2, 1],
    4: [0.7654, 1.85, 1.85, 0.7654],
    5: [0.618, 1.618, 2, 1.618, 0.618],
    6: [0.5176, 1.414, 1.932, 1.932, 1.1414, 0.5176],
    7: [0.445, 1.247, 1.802, 2, 1.802, 1.247, 0.445],
    8: [0.3902, 1.1111, 1.6629, 1.9615, 1.9615, 1.6629, 1.1111, 0.3902],
    9: [0.3473, 1.0, 1.5321, 1.8794, 2.0, 1.897, 1.5321, 1.0, 0.3473],
    10: [0.3129, 0.9080, 1.4142, 1.7820, 1.9754, 1.9754, 1.7820, 1.4142, 0.9080, 0.3129]
}

BUTTERWORTH_COEF_LINEAR_PHASE = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: []
}


class LowPassFilter(SubCircuit):

    def __init__(self, cutoffFrequency, num=5, R0=50, seriesFirst=False, name=None):
        if name is None:
            name = "LPF_"+str(hex(id(self)))[-4:]
        SubCircuit.__init__(self, name=name)
        self._numComponents = num
        self._characteristicImpedance = R0
        self._cutoffFrequency = cutoffFrequency
        for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[num]):
            L = val * R0
            C = val / R0
            if i % 2 == int(seriesFirst):
                self.shunt(Capacitor(C / (2 * np.pi * cutoffFrequency)))
            else:
                self.series(Inductor(L / (2 * np.pi * cutoffFrequency)))
        # self.end()


class HighPassFilter(SubCircuit):

    def __init__(self, cutoffFrequency, num=5, R0=50, seriesFirst=False, name=None):
        if name is None:
            name = "HPF_"+str(hex(id(self)))[-4:]
        SubCircuit.__init__(self, name=name)
        self._numComponents = num
        self._characteristicImpedance = R0
        self._cutoffFrequency = cutoffFrequency

        for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[num]):
            L = val * R0
            C = val / R0
            if i % 2 == int(seriesFirst):
                self.series(Capacitor(1 / (L * 2 * np.pi * cutoffFrequency)))
            else:
                self.shunt(Inductor(1 / (C * 2 * np.pi * cutoffFrequency)))
        # self.end()


class BandPassFilter(SubCircuit):

    def __init__(self, upper, lower, num=5, R0=50, seriesFirst=False, name=None):
        if name is None:
            name = "BPF_"+str(hex(id(self)))[-4:]
        SubCircuit.__init__(self, name=name)
        upper = upper * 2 * np.pi
        lower = lower * 2 * np.pi

        self._numComponents = num
        self._characteristicImpedance = R0
        self._centerFrequency = f0_from_bandwidth(lower, upper)
        self._bandwidth = upper - lower

        for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[num]):
            L = val * R0
            C = val / R0
            if i % 2 == int(seriesFirst):
                self.series(
                    Inductor(L / self._bandwidth),
                    Capacitor(self._bandwidth / (self._centerFrequency**2 * L))
                )
            else:
                self.shunt(Capacitor(C / self._bandwidth))
                self.shunt(Inductor(self._bandwidth /
                           (self._centerFrequency**2 * C)))
        # self.end()

    def bandwidth(self):
        return self._bandwidth

    def centerFrequency(self):
        return self._centerFrequency


class BandStopFilter(SubCircuit):

    def __init__(self, upper, lower, num=5, R0=50, seriesFirst=False, name=None):
        if name is None:
            name = "BSF_"+str(hex(id(self)))[-4:]
        SubCircuit.__init__(self, name=name)
        upper = upper * 2 * np.pi
        lower = lower * 2 * np.pi

        self._numComponents = num
        self._characteristicImpedance = R0
        self._centerFrequency = f0_from_bandwidth(lower, upper)
        self._bandwidth = upper - lower

        for i, val in enumerate(BUTTERWORTH_COEF_MAX_FLAT[num]):
            L = val * R0
            C = val / R0
            if i % 2 == int(seriesFirst):
                self.parallel(
                    Capacitor(1 / (self._bandwidth * L), ESR=2.0),
                    Inductor((self._bandwidth * L) /
                             self._centerFrequency**2, ESR=2.0)
                )
            else:
                self.shunt(
                    Inductor(1 / (self._bandwidth * C), ESR=2.0),
                    Capacitor((self._bandwidth * C) /
                              self._centerFrequency**2, ESR=2.0)
                )
        # self.end()

    def bandwidth(self):
        return self._bandwidth

    def centerFrequency(self):
        return self._centerFrequency
