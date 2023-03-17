from ..circuit import SubCircuit
from ..element.component import PassiveComponent, Inductor, Capacitor, Resistor
from ..scanner import parse_value
from ..formula import rf

import numpy as np


class Crystal(PassiveComponent):

    def __init__(self, L, Cs, ESR, Cp, **kwargs):
        PassiveComponent.__init__(self)
        self._circuit = SubCircuit(**kwargs)
        self.L = Inductor(L)
        self.Cs = Capacitor(Cs)
        self.ESR = Resistor(ESR)
        self.Cp = Capacitor(Cp)

        self._circuit.parallel(
            self.Cp,
            [self.L, self.Cs, self.ESR]
        )

    def resistance(self):
        return self.ESR

    def impedance(self, frequency):
        return self._circuit.source.computeLoadImpedance(frequency)

    def seriesResonance(self):
        return rf.resonant_frequency(self.L.value, self.Cs.value)

    def parallelResonance(self):
        return rf.resonant_frequency(self.L.value, self.Cs.value) * np.sqrt(1 + (self.Cs.value/self.Cp.value))


crystal_11MHz = Crystal(
    L=parse_value(mH=25),
    Cs=parse_value(pF=0.008),
    ESR=30,
    Cp=parse_value(pF=2)
)

crystal_5MHz = Crystal(
    L=0.098,
    Cs=parse_value(pF=0.0134),
    ESR=12.8,
    Cp=parse_value(pF=2.275)
)
