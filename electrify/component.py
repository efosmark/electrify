from abc import ABC, abstractmethod
import numpy as np

from .math.rf import resistance_from_Q

from .math.inductance import inductance_from_reactance, inductive_reactance
from .math.capacitance import capacitive_reactance, capacitance_from_reactance
from .value import parse_value, format_value, from_color_code
from .constants import OPEN_CIRCUIT, SHORT_CIRCUIT, HENRY, FARAD, OHM
from .lexer import ElectrifyLexer, NumberToken, MagnitudeToken, UnitToken, matches_types


class Component(ABC):
    UNIT = ""

    def __init__(self, value=None, name=None, **kwargs):
        if name is None:
            self.name = str(hex(id(self)))[-4:]
        else:
            self.name = name
        self.value = parse_value(value, **kwargs)

    def __str__(self):
        if self.value is not None:
            return "<{}:{} ({}{})>".format(self.__class__.__name__, self.name, format_value(self.value), self.UNIT)
        return "<{}:{}>".format(self.__class__.__name__, self.name)

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def resistance(self): pass

    def conductance(self):
        return 1 / self.resistance()

    @abstractmethod
    def impedance(self, frequency): pass

    def admittance(self, frequency):
        return 1 / self.impedance(frequency)

    @classmethod
    def from_string(cls, string):
        scanner = ElectrifyLexer(string)
        tokens = scanner.scan_all()
        value = 0
        unit_type = None

        if len(tokens) == 2:
            if not matches_types(tokens, (NumberToken, UnitToken)):
                raise ValueError(
                    "Format must be [value][mag][unit] or [value][unit]. Got: '{}'".format(tokens))
            value += tokens[0].value
            unit_type = tokens[1].unit

        elif len(tokens) == 3:
            if not matches_types(tokens, (NumberToken, MagnitudeToken, UnitToken)):
                raise ValueError(
                    "Format must be [value][mag][unit] or [value][unit]. Got: '{}'".format(tokens))
            value += tokens[0].value
            value = value * tokens[1].magnitude
            unit_type = tokens[2].unit

        else:
            raise ValueError("Invalid value: '{}'".format(string))

        if unit_type == HENRY:
            e = Inductor(value)
        elif unit_type == FARAD:
            e = Capacitor(value)
        elif unit_type == OHM:
            e = Resistor(value)
        else:
            raise ValueError("Unsupported unit_type='{}'".format(unit_type))

        if not isinstance(e, Component):
            raise TypeError("The unit associated with the string '{}' is not of type {}. Received {}.".format(
                string, str(cls), type(e)))

        return e


class Node(Component):

    def __init__(self, name=None):
        self.value = 0
        self.name = str(hex(id(self)))[-4:]
        if name is not None:
            self.name = self.name + ':' + name

    def resistance(self): return 0
    def reactance(self, f): return 0
    def impedance(self, f): return 0

    def __str__(self):
        return "<Node:{}>".format(self.name)


class Terminal(Node):
    def __init__(self, element, name):
        self.value = 0
        self.element = element
        self.name = name

    def __str__(self):
        if 'name' in dir(self.element):
            return "<Terminal-{} for {}>".format(self.name, self.element.name)
        else:
            return "<Terminal-{} for {}>".format(self.name, self.element)


class Branch(Node):
    pass


class PassiveComponent(Component):
    pass


class ReactiveComponent(PassiveComponent):

    def __init__(self, value, **kwargs):
        super().__init__(value, **kwargs)

    def resistance(self, f):
        return resistance_from_Q(self.Q, self.reactance(f))

    @abstractmethod
    def reactance(self, frequency): pass

    def susceptance(self, frequency):
        return 1 / self.reactance(frequency)

    def Q(self, f):
        return self.reactance(f) / self.resistance()

    @classmethod
    @abstractmethod
    def from_reactance(cls, f, reactance): pass


class Gnd(Node):
    def __str__(self):
        return "<GROUND>"


class Resistor(PassiveComponent):
    UNIT = "Ω"

    def resistance(self):
        return self.value

    def impedance(self, f):
        return self.resistance()

    @classmethod
    def from_color_code(cls, first, second, third, forth=None):
        return cls(from_color_code(first, second, third, forth))


class Source(PassiveComponent):

    def __init__(self, ESR=0, GND=None, **kwargs):
        super().__init__(**kwargs)
        self.__ESR = ESR
        self.GND = GND

        self.LOAD = Node(name='Terminal_LOAD-{}'.format(self.name))

    def resistance(self):
        return self.__ESR

    def impedance(self, f):
        return self.resistance()


class Load(Resistor):

    def __init__(self, value, GND=None, **kwargs):
        super().__init__(value, **kwargs)
        self.GND = GND

    def __str__(self):
        return '<Load R={}Ω>'.format(format_value(self.value, places=0))


class SignalSource(Source):
    UNIT = 'Hz'

    def __init__(self, frequency, dc_voltage=0.0, v_pp=1.0, **kwargs):
        super().__init__(**kwargs)
        self.frequency = frequency
        self.dc_voltage = dc_voltage
        self.v_pp = v_pp

    def __str__(self):
        return '<SignalSource {}Hz+{}V & Vpp=>'.format(format_value(self.frequency), format_value(self.dc_voltage))


class VoltageSource(Source):
    UNIT = 'V'

    def __init__(self, voltage, **kwargs):
        super().__init__(**kwargs)
        self.voltage = voltage

    def __str__(self):
        return '<VoltageSource {}V {}Ω>'.format(format_value(self.voltage), format_value(self.resistance()))


class CurrentSource(Source):
    UNIT = 'A'

    def __init__(self, current, internal_resistance=np.inf, maximum_voltage=1e3, **kwargs):
        super().__init__(**kwargs)
        self.current = current

    def resistance(self):
        return np.inf

    def voltage(self):
        pass


class Capacitor(ReactiveComponent):
    UNIT = "F"

    def __init__(self, value=None, ESR=0, **kwargs):
        super().__init__(value, **kwargs)
        self.__ESR = ESR

    def resistance(self):
        return self.__ESR

    def reactance(self, f):
        return capacitive_reactance(f, self.value)

    def impedance(self, f):
        if f == 0:
            return OPEN_CIRCUIT
        if np.isinf(f):
            return self.resistance()
        return self.resistance() + self.reactance(f)

    @classmethod
    def from_reactance(cls, f, XC, **kwargs):
        return cls(value=capacitance_from_reactance(f, 0 - abs(XC)), **kwargs)

    def conjugate(self, f, **kwargs):
        return Inductor.from_reactance(f, abs(self.reactance(f)), **kwargs)


class Inductor(ReactiveComponent):
    UNIT = "H"

    def __init__(self, value=None, ESR=SHORT_CIRCUIT, **kwargs):
        super().__init__(value, **kwargs)
        self.__ESR = ESR

    def resistance(self):
        return self.__ESR

    def reactance(self, f):
        return inductive_reactance(f, self.value)

    def impedance(self, f):
        if f == 0:
            return self.resistance()
        if np.isinf(f):
            return OPEN_CIRCUIT
        return self.resistance() + self.reactance(f)

    @classmethod
    def from_reactance(cls, f, XL, **kwargs):
        return cls(value=inductance_from_reactance(f, abs(XL)), **kwargs)

    def conjugate(self, f, **kwargs):
        return Capacitor.from_reactance(f, -self.reactance(f), **kwargs)
