"""
The base classes for multi-port networks.

Available variants are:

 - `OnePortNetwork`
 - `TwoPortNetwork`

Beyond that, a custom multi-port network can be created by subclassing either of those
variants, or by subclassing `PortNetwork` and specifying the number of ports directly.
"""
import enum
from functools import cache
from typing import Callable, ClassVar, Generic, Optional, Sequence, TypeVar
import networkx as nx

from .dag import SolvableDAG
from ..value.unit import *


_T = TypeVar("_T")
_U = TypeVar("_U")


ImpedanceCallable = Callable[[hertz], ohm]
CurrentCallable = Callable[[hertz], ampere]
VoltageCallable = Callable[[hertz], volt]


class Polarity(enum.Enum):
    """Enum for denoting polarity."""

    POSITIVE = enum.auto()
    NEGATIVE = enum.auto()


class Property(Generic[_T]):
    """Representation of a property of type _T."""

    _value: Optional[_T] = None

    def __init__(self, value: Optional[_T], name: Optional[str] = None):
        """Create a new property with a value and/or name."""
        self._value = value
        if name is None:
            name = f'Property[{type(self._value).__name__}]'
        self.name = name

    def value(self) -> Optional[_T]:
        """Get the value of the property."""
        return self._value

    def __repr__(self):
        return f'<{self.name} ({self._value})>'


class Pole(Property[Polarity]):
    """
    In a port network, a port is made up of two poles.

    This pole can have either a polarity of `polarity.POSITIVE`, or `polarity.NEGATIVE`.
    A port should have one of each.
    """

    port: 'Port'

    def __init__(self, port: 'Port', polarity: Polarity):
        """Create a new pole with the given polarity for the given port."""
        self.port = port
        self._value = polarity

        pole = ('P' if polarity is Polarity.POSITIVE else 'N')
        self.name = f'port_{self.port.port_id}_{pole}'

    def __repr__(self):
        return self.name

    def __str__(self):
        return f'<Pole({self._value}) of port {self.port.port_id}>'


class Port:
    """
    Representation of a network port.

    A port comprises two poles, which can be accessed at <instance>.pos for the Polarity.POSITIVE
    pole, and <instance>.neg for the Polarity.NEGATIVE pole.

    A shorthand is available which utilizes the ``__pos__`` and ``__neg__`` methods.

    >>> port = new Port(network, 1)
    >>> positive_pole = +port
    >>> negative_pole = -port

    A port should never be an element inside of the graph that represents the network.
    Instead, it should always be referenced toward one of its two poles.
    """

    network: 'PortNetwork'
    port_id: int
    pos: Pole
    neg: Pole

    def __init__(self, network: 'PortNetwork', port_id: int):
        """Create a new port for the given network."""
        self.network = network
        self.port_id = port_id
        self.pos = Pole(self, Polarity.POSITIVE)
        self.neg = Pole(self, Polarity.NEGATIVE)

    def __pos__(self) -> Pole:
        return self.pos

    def __neg__(self) -> Pole:
        return self.neg

    def __repr__(self):
        return f'Port(port_id={self.port_id})'

    def __str__(self):
        return f'<{self.__repr__()} at {hex(id(self))}>'


class PortNetwork(nx.Graph):
    """
    An abstract representation of a port network.

    When subclassing, the `num_ports` class variable must be specified, and equal
    to the number of ports that comprises the network. The ports will be automatically
    created during the initialization of the network, and will be available at ``<instance>.ports``.
    """

    num_ports: ClassVar[int]
    ports: dict[int, Port]
    solutions: dict[tuple, SolvableDAG]

    def __init__(self):
        """Create a new port network with the number of ports equal to cls.num_ports."""
        nx.Graph.__init__(self)
        self.solutions = {}
        self.ports = {}
        for i in range(self.num_ports):
            port_id = i + 1
            new_port = Port(self, port_id)
            self.ports[port_id] = new_port

    def __repr__(self):
        return f'{self.__class__.__name__}(num_ports={self.num_ports})'

    def __str__(self):
        return f'<{self.__repr__()} at {hex(id(self))}>'

    def port(self, port_id: int) -> Port:
        """
        Get the port with the given ID.

        Args:
            port_id (int): _description_

        Returns:
            Port: _description_
        """
        return self.ports[port_id]

    def add_parallel(self, items: Sequence[_U], *, start: _U, end: _U) -> _U:
        """
        When building the network, this allows for adding several items in parallel.

        Args:
            items (Sequence[_U]): _description_
            start (_U): _description_
            end (_U): _description_

        Returns:
            _U: _description_
        """
        for itm in items:
            self.add_edge(start, itm)
            self.add_edge(itm, end)
        return end

    def add_series(self, items: Sequence[_U]) -> _U:
        """
        Wehn building the network, this allows for adding several items in series.

        Args:
            items (Sequence[_U]): _description_

        Returns:
            _U: _description_
        """
        for itm_A, itm_B in zip(items, items[1:]):
            self.add_edge(itm_A, itm_B)
        return items[-1]

    def _superposition_indices(self) -> list[tuple[int, int]]:
        result = []
        port_ids = self.ports.keys()
        for p1 in port_ids:
            result.extend([(p1, p2) for p2 in port_ids])
        return result

    def _get_dag_solution(self, src: int | Port, target: int | Port) -> SolvableDAG:
        if isinstance(src, int):
            src = self.ports[src]
        if isinstance(target, int):
            target = self.ports[target]
        if (src, target) not in self.solutions:
            self.solutions[(src, target)] = SolvableDAG[Property](
                self,
                +src,
                -target
            )
        return self.solutions[(src, target)]

    def z_parameter(self, src: int | Port, targ: int | Port) -> ImpedanceCallable:
        """Get a function that, given a frequency, will return the impedance between the ports."""
        return self._get_dag_solution(src, targ).impedance

    def z(self, src: int | Port, target: int | Port, frequency: hertz) -> ohm:
        """
        Get the impedance between two ports at a given frequency.

        Args:
            src (int | Port): Either the port ID or the port instance for the source.
            target (int | Port): Either the port ID or the port instance for the source.
            frequency (hertz): Frequency at which we want to determine the impedance.

        Returns:
            ohm: The (potentially comlex) impedance.
        """
        param = self.z_parameter(src, target)
        return param(frequency)

    # def analyze_open_circuit(self):
    #     """

    #     Compute the Z-parameter linear equations with the non-source ports
    #     configured with open-circuit conditions.
    #     """

    # def analyze_short_circuit(self):
    #     """

    #     Compute the Y-parameter linear equations with the non-source ports
    #     configured with closed-circuit conditions.
    #     """

    # @property
    # @cache
    # def Z_matrix(self): pass  # -> dict[tuple, Callable[[hertz], ohm]]:
    # matrix = {}
    # for (p1, p2) in self.superposition_indices():
    #     matrix[p1, p2] = self.Z_parameter(self.port(p1), self.port(p2))
    # return matrix


class OnePortNetwork(PortNetwork):
    """Representation of a single-port network that has one positive and one negative pole."""

    num_ports: ClassVar[int] = 1

    def impedance(self, frequency: hertz) -> ohm:
        """Get the total impedance of the network between port.pos and port.neg."""
        return self.z(1, 1, frequency)


class TwoPortNetwork(PortNetwork):
    """
    Representation of a network that comprises two ports.

    Two-port networks have some 'special' features, such as being able to compute
    the ABCD parameters, the s-parameters, and the h-parameters.
    """

    num_ports: ClassVar[int] = 2

    #def ABCD(self): ...

    #def s(self, port_A, port_B): ...

    #def is_reciprocal(self): ...
