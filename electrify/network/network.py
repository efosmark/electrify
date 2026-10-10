import math
from typing import *
from electrify.dc import SupportsImpedance
from electrify.util import StackLogger
from electrify.types import *
from .net import Edge, Net, NetList, Side, VirtualItem

stack_logger = StackLogger(compact=True)

class Port(VirtualItem):
    """External connection point for a port network."""

    network:'PortNetwork'
    id:int|str

    def __init__(self, network:'PortNetwork', id:int|str):
        self.network = network
        self.id = id

    @property
    def pos(self) -> Edge[Self]:
        return Edge(self, Side.A)
    
    @property
    def neg(self) -> Edge[Self]:
        return Edge(self, Side.B)
    
    def impedance(self, frequency:hertz) -> ohm:
        return ohm(math.inf)
    
    def __repr__(self):
        return f'Port({self.network}, {self.id})'


class PortNetwork(NetList[SupportsImpedance]):
    """Base class for one-port and two-port component networks."""

    allow_compose: ClassVar[bool] = True
    num_ports: ClassVar[int]
    ports: Dict[int|str, Port]

    def __init__(self):
        super().__init__()
        self.ports = {}
        for i in range(1, self.num_ports + 1):
            p = Port(self, i)
            self.ports[i] = p
            self.add(p, Side.A)
            self.add(p, Side.B)

    def __str__(self):
        return f'<{self.__class__.__name__}>'

    def _resolve_net(self, p1:SupportsImpedance|Edge, side:Side, compose:bool) -> Net:
        if isinstance(p1, OnePortNetwork) and compose:
            self.import_netlist(p1)
            p1 = p1.get_pole(side)
        if not isinstance(p1, Edge):
            p1 = Edge(p1, side)
        return self.net_from_edge(p1)

    def connect(self, p1:SupportsImpedance|Edge, p2:SupportsImpedance|Edge, compose:bool=True):
        """Connect terminal ``p1`` to terminal ``p2``."""
        net1 = self._resolve_net(p1, Side.B, compose)
        net2 = self._resolve_net(p2, Side.A, compose)
        self.combine_nets(net1, net2)
    
    def series(self, *items):
        """Connect all ``items`` in series and return the last item."""
        last = None
        for c1, c2 in zip(items, items[1:]):
            self.connect(c1, c2)
            last = c2
        return last
    
    def paths_between(self, start_ref:Net, end_ref:Net) -> set[tuple]:
        """Get all acyclic paths between the two refs."""
        result = set()
        paths:list[list[SupportsImpedance|Net]] = [[start_ref]]
        while len(paths) > 0:
            path = paths.pop(0)
            node = path[-1]
            if isinstance(node, Port):
                continue
            elif node is end_ref:
                result.add(tuple(path))
                continue
            elif isinstance(node, Net):
                for prop, side in node.edges:
                    if isinstance(prop, Port) or (prop, side) in path:
                        continue
                    paths.append([*path, prop])
            elif isinstance(node, SupportsImpedance):
                net_A = self.get_net(node, Side.A)
                if net_A not in path:
                    paths.append([*path, net_A])
                net_B = self.get_net(node, Side.B)
                if net_B not in path:
                    paths.append([*path, net_B])
            else:
                raise Exception(f'unknown type for {node}')
        return result


class OnePortNetwork(PortNetwork):
    """Network with one positive/negative external port pair."""

    num_ports: ClassVar[int] = 1
    
    def get_pole(self, side:Side) -> Edge:
        return Edge(self.ports[1], side)
    
    def impedance(self, frequency: hertz) -> ohm:
        # TODO: impedance between +p1 and -p1
        return ohm(math.inf)


class Series(OnePortNetwork):
    """
    One-port network that connects items in series.

    Examples:
        >>> from electrify.component import R
        >>> network = Series(R(ohm(100)), R(ohm(220)))
        >>> len(network.export()["items"])
        2
    """
    
    def __init__(self, *args, **kwargs):
        OnePortNetwork.__init__(self)
        compose = kwargs.get("compose", True)
        items = [
            self.get_pole(Side.A),
            *args,
            self.get_pole(Side.B)
        ]
        for a,b in zip(items, items[1:]):
            self.connect(a, b, compose)


# class Parallel(OnePortNetwork):
    
#     def __init__(self, *args:Connectable, **kwargs):
#         OnePortNetwork.__init__(self)
#         compose = kwargs.get("compose", True)
#         A_pole = self.get_pole(Side.A)
#         B_pole = self.get_pole(Side.B)
#         for a in args:
#             self.connect(A_pole, a, compose)
#             self.connect(a, B_pole, compose)


class TwoPortNetwork(PortNetwork):
    """Network with input and output port pairs."""

    num_ports: ClassVar[int] = 2

    def cascade(self):...
