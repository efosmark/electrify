from typing import SupportsComplex, SupportsFloat
from electrify.value import format_value
from electrify.types import ElectricUnit, ohm, farad, henry, volt, hertz, SupportsImpedance
from electrify.quantity.reactance import get_capacitive_reactance, get_inductive_reactance

class ElectricComponent(ElectricUnit):
    
    def __hash__(self):
        return hash(id(self))
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{format_value(self)}')"

class R(ElectricComponent, ohm):
    def impedance(self, frequency:hertz) -> ohm:
        return ohm(self)

class C(ElectricComponent, farad):
    def impedance(self, frequency:hertz) -> ohm:
        return get_capacitive_reactance(frequency, self)

class L(ElectricComponent, henry):
    def impedance(self, frequency:hertz) -> ohm:
        return get_inductive_reactance(frequency, self)

class V(ElectricComponent, volt):
    ESR:ohm|SupportsImpedance
    
    def __init__(self, input:SupportsComplex|SupportsFloat, ESR:ohm|SupportsImpedance=ohm(0)):
        super(volt).__init__(input)
        self.ESR = ESR
    
    def impedance(self, frequency:hertz) -> ohm:
        if isinstance(self.ESR, ohm):
            return self.ESR
        return self.ESR.impedance(frequency)


# TODO:
#  - Constant current source
#  - Signal source
#  - Diode
#  - Transistor
#  - Transformer
#  - Transmission line
#  - Assertion


#
