import enum
import math
from collections import defaultdict
from typing import *

from electrify.util import StackLogger
from electrify.types import *

stack_logger = StackLogger(compact=True)
_T = TypeVar("_T")


class VirtualItem:
    def impedance(self, frequency:hertz) -> ohm:
        return ohm(math.inf)


class Side(enum.Enum):
    A = 0
    B = 1
    
    def __repr__(self):
        return f'Side.{self.name}'


class Edge(NamedTuple, Generic[_T]):
    item: _T
    pin: Side


class Net(NamedTuple):
    netlist: 'NetList'
    id: int
    
    @property
    def edges(self) -> frozenset[Edge]:
        return frozenset(self.netlist._nets[self])
    
    def impedance(self, frequency:hertz) -> ohm:
        return ohm(0)
    
    def __repr__(self):
        return f'Net(<{self.netlist.__class__.__name__}>, {self.id})'


class NetList(Generic[_T]):
    _nets: Dict[Net, Set[Edge[_T]]]
    _edges: Dict[Edge[_T], Net]
    
    _id_to_item: Dict[str, _T]
    _item_to_id: Dict[_T, str]
    
    _net_count: int
    _symbol_count: dict[str, int]
    
    def __init__(self):
        self._nets = dict()
        self._edges = dict()
        
        self._id_to_item = dict()
        self._item_to_id = dict()
        
        self._net_count = 0
        self._symbol_count = defaultdict(lambda:1)
    
    def _symbol(self, prop:_T) -> str:
        if len(prop.__class__.__name__) <= 2:
            return prop.__class__.__name__
        elif isinstance(prop, Net):
            return 'N'
        return 'U'
    
    def _new_item_id(self, prop:_T) -> str:
        symbol = self._symbol(prop)
        item_id = str(f'{symbol}{self._symbol_count[symbol]}')
        self._symbol_count[symbol] += 1
        return item_id
    
    def id(self, prop:_T) -> str:
        if prop in self._item_to_id:
            return self._item_to_id[prop]
        item_id = self._new_item_id(prop)
        self._item_to_id[prop] = item_id
        self._id_to_item[item_id] = prop
        return item_id
    
    def new_net(self) -> Net:
        net_id = self._net_count
        self._net_count += 1
        net = Net(self, net_id)
        self._nets[net] = set()
        return net
    
    def add(self, item:_T, pin:Side, net:Optional[Net]=None) -> Net:        
        if net is None:
            net = self.new_net()
        if item not in self._item_to_id:
            self.id(item)
        edge = Edge(item, pin)
        if edge not in self._edges:
            self._edges[edge] = net
            self._nets[net].add(edge)
        return self._edges[edge]
    
    def get_net(self, item:_T, side:Side) -> Net:
        edge = Edge(item, side)
        if edge not in self._edges:
            return self.add(item, side)
        return self._edges[edge]
    
    def delete_net(self, net:Net):
        edges = self._nets[net]
        del self._nets[net]
        for edge in edges:
            if self._edges[edge] is net:
                del self._edges[edge]
    
    def net_from_edge(self, edge:Edge[_T]) -> Net:
        if edge not in self._edges:
            return self.add(edge.item, edge.pin)
        return self._edges[edge]
    
    def combine_nets(self, primary:Net, secondary:Net) -> Net:
        if primary == secondary:
            return primary
        edges = secondary.edges
        self.delete_net(secondary)
        self._nets[primary].update(edges)
        for edge in self._nets[primary]:
            self._edges[edge] = primary
        return primary

    def import_netlist(self, netlist:'NetList'):
        for net in netlist._nets:
            n = self.new_net()
            for edge in net.edges:
                self._nets[n].add(edge)
                self._edges[edge] = n
                
    def nets(self) -> Sequence[Net]:
        return tuple(self._nets.keys())

    def export(self, exclude_virtual=True):
        nets = {}
        items = {}
        for net in self.nets():
            entries = set()
            for edge in net.edges:
                if exclude_virtual and isinstance(edge.item, VirtualItem):
                    continue
                item_id = self.id(edge.item)
                if item_id not in items:
                    items[item_id] = edge.item
                entries.add((item_id, edge.pin))
            nets[net.id] = entries
        return {
            "nets": nets,
            "items": items
        }
