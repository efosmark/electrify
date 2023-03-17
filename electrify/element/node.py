from ..value.unit import *
from .element import Element


class Node(Element):
    def resistance(self) -> ohm: return ohm(0)
    def reactance(self, frequency: hertz | float) -> ohm: return ohm(0)
    def impedance(self, frequency: hertz | float) -> ohm: return ohm(0)

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


class Gnd(Node):
    def __str__(self):
        return "<GROUND>"
