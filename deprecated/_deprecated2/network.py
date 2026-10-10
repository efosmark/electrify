"""
The base classes for multi-port networks.

Available variants are:

 - `OnePortNetwork`
 - `TwoPortNetwork`

Beyond that, a custom multi-port network can be created by subclassing either of those
variants, or by subclassing `PortNetwork` and specifying the number of ports directly.
"""
from typing import Callable, ClassVar, Literal, Sequence, TypeVar
import networkx as nx

#from electrify.network.solution import Z_Solution

from dag import SolvableDAG
from property import *
from port import Port
from electrify.value.unit1 import *


_T = TypeVar("_T")
_U = TypeVar("_U")


ImpedanceCallable = Callable[[hertz], ohm]
CurrentCallable = Callable[[hertz], ampere]
VoltageCallable = Callable[[hertz], volt]


class PortNetwork(nx.Graph):
    """
    An abstract representation of a port network.

    When subclassing, the `num_ports` class variable must be specified, and equal
    to the number of ports that comprises the network. The ports will be automatically
    created during the initialization of the network, and will be available at ``<instance>.ports``.
    """

    num_ports: ClassVar[int]
    ports: dict[int|str, Port]
    solutions: dict[tuple, SolvableDAG]
    Z_solutions: dict[tuple, Any]

    def __init__(self):
        """Create a new port network with the number of ports equal to cls.num_ports."""
        nx.Graph.__init__(self)
        self.solutions = {}
        self._init_ports()

    def _init_ports(self):
        self.ports = {}
        for i in range(self.num_ports):
            port_id = i + 1
            new_port = Port(self, port_id)
            self.ports[port_id] = new_port

    def __repr__(self):
        return f'{self.__class__.__name__}(num_ports={self.num_ports})'

    def __str__(self):
        return f'<{self.__repr__()} at {hex(id(self))}>'
    
    def __getitem__(self, port_id: int|str):
        return self.ports[port_id]

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
        
    def _superposition_indices(self) -> list[tuple[int|str, int|str]]:
        result = []
        port_ids = self.ports.keys()
        for p1 in port_ids:
            result.extend([(p1, p2) for p2 in port_ids])
        return result

    def get_dag_solution(self, src: int | Port, target: int | Port) -> SolvableDAG:
        if isinstance(src, int):
            src = self.ports[src]
        if isinstance(target, int):
            target = self.ports[target]
        if (src, target) not in self.solutions:
            self.solutions[(src, target)] = SolvableDAG(
                self,
                +src,
                -target
            )
        return self.solutions[(src, target)]

    # def z_parameter(self, src: int | Port, targ: int | Port) -> ImpedanceCallable:
    #     """Get a function that, given a frequency, will return the impedance between the ports."""
    #     return self.get_dag_solution(src, targ).impedance

    # def z(self, src: int | Port, target: int | Port, frequency: hertz) -> ohm:
    #     """
    #     Get the impedance between two ports at a given frequency.

    #     Args:
    #         src (int | Port): Either the port ID or the port instance for the source.
    #         target (int | Port): Either the port ID or the port instance for the source.
    #         frequency (hertz): Frequency at which we want to determine the impedance.

    #     Returns:
    #         ohm: The (potentially comlex) impedance.
    #     """
    #     param = self.z_parameter(src, target)
    #     return param(frequency)
    
    
    #def Z(self, port1: Port, port2: Port, frequency: hertz) -> ohm:
    #    if (port1, port2) not in self.solutions:
    #        self.Z_solutions[(port1,port2)] = self.solve_for(port1, port2)
        
    
    #def solve_for(self, port1: Port, port2: Port) -> Any:
    #    pass
    
    # def _compute_impedances(source, target):
        
        

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

    #def impedance(self, frequency: hertz) -> ohm:
    #    """Get the total impedance of the network between port.pos and port.neg."""
    #    return self.z(1, 1, frequency)


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
