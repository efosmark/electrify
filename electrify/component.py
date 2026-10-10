from typing import SupportsComplex, SupportsFloat
from electrify.value import format_value
from electrify.types import ElectricUnit, ohm, farad, henry, volt, hertz, SupportsImpedance
from electrify.quantity.reactance import get_capacitive_reactance, get_inductive_reactance

class ElectricComponent(ElectricUnit):
    """Base class for unit-valued circuit components."""
    
    def __hash__(self):
        return hash(id(self))
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{format_value(self)}')"

class R(ElectricComponent, ohm):
    """
    Resistor component.

    Examples:
        >>> R(ohm(k=1)).impedance(hertz(k=10))
        ohm(1000.0)
    """

    def impedance(self, frequency: hertz) -> ohm:
        """Return the fixed resistance, independent of frequency."""
        return ohm(self)

class C(ElectricComponent, farad):
    """
    Capacitor component.

    Examples:
        >>> str(C(n=100).impedance(hertz(k=1)))
        '[0 - 1.6jk]Ω'
    """

    def impedance(self, frequency: hertz) -> ohm:
        """Return capacitive reactance at ``frequency``."""
        return get_capacitive_reactance(frequency, self)

class L(ElectricComponent, henry):
    """
    Inductor component.

    Examples:
        >>> str(L(m=1).impedance(hertz(k=1)))
        '[0 + 6.3j]Ω'
    """

    def impedance(self, frequency: hertz) -> ohm:
        """Return inductive reactance at ``frequency``."""
        return get_inductive_reactance(frequency, self)

class V(ElectricComponent, volt):
    """Voltage source with an equivalent series resistance."""

    ESR:ohm|SupportsImpedance
    
    def __init__(self, input:SupportsComplex|SupportsFloat, ESR:ohm|SupportsImpedance=ohm(0)):
        super(volt).__init__(input)
        self.ESR = ESR
    
    def impedance(self, frequency:hertz) -> ohm:
        """Return the source equivalent series resistance at ``frequency``."""
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
