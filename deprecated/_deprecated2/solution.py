"""
Network solver that utilizes a directed-acyclic-graph.

This utilizes nodal analysis and the concept of superposition.
Each source should incorporate its own targeted DAG.
"""
from collections import defaultdict
from functools import lru_cache
from typing import Any, Dict, Generic, Optional, Tuple, TypeVar
from electrify.dc import attenuation_factor, current_divider
from network import PortNetwork, Port
from electrify.quantity import reactance
from electrify.value.sum import harmonic_sum
 
from electrify.value.unit1 import *
from property import Capacitance, Inductance, NegativePole, Pole, PositivePole, Property, Resistance

import networkx as nx

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_V = TypeVar("_V")
_S = Property
Edge = Tuple[_S, _S]

class GraphNode(defaultdict[str, Any], Generic[_V]):
    """
    DAG nodes hold references to each of its predecessors and its successors.

    This should not need to be instanced directly.
    """

    paths: set[tuple]
    predecessors: set[_V]
    successors: set[_V]

    def __init__(self):
        """
        Create a new instance of a directed graph node.

        This should not need to be instanced directly.

        Args:
            node (Optional[_V], optional): _description_. Defaults to None.
        """
        self.paths = set()
        self.successors = set()
        self.predecessors = set()
        self.bidirectional = set()

    @property
    def neighbors(self) -> set[_V]:
        """
        Get the set of all connected nodes, regardless of direction.
 
        Returns:
            set[_V]: A set containing both sucessors and predecessors.
        """
        return self.successors | self.predecessors | self.bidirectional

    def __repr__(self):
        return f'p:{len(self.predecessors)} s:{len(self.successors)}'



# class Solution(defaultdict[_S, GraphNode[_S]]):
#     
#     port: Port
#     graph: PortNetwork
#     _completed_nodes:set[_S]
#     
#     def __init__(self, graph, port):
#         defaultdict.__init__(self, GraphNode[_S])
#         self.graph = graph
#         self.port = port
#     
#         start_node = port.pos
#         end_node = port.neg
#         
#         self._completed_nodes = set()
#         
#         result = defaultdict(lambda _:self, GraphNode[_S])
#         stack = [start_node]
#         while len(stack) > 0:
#             node = stack.pop()
            
        

class DirectedSolution(defaultdict[_S, GraphNode[_S]]):
    """A directed graph that connects paths between a given source and target."""

    _terminals: set[_S]
    
    def __init__(self, graph, port):
        """Build a directed graph from paths that start at `src` and end at `target`."""
        defaultdict.__init__(self, GraphNode[_S])
        self.graph = graph
        self.initial_port = port
        self._terminals = set()
        for p in self.graph.ports.values():
            self._terminals.add(p.neg)
        self._build_digraph()

    def __hash__(self):
        return hash(hex(id(self)))

    def _is_transient(self, node:_S) -> bool:
        return not isinstance(node, (Resistance, Capacitance, Inductance))
    
    @lru_cache(2048, typed=True)
    def self_impedance(self, node:_S, frequency:hertz = hertz(0)) -> ohm:
        if node.value is not None:
            if isinstance(node, Resistance):
                return node.value
            if isinstance(node, Capacitance):
                return reactance.get_capacitive_reactance(frequency, node.value)
            if isinstance(node, Inductance):
                return reactance.get_inductive_reactance(frequency, node.value)
        if isinstance(node, Pole):
            return ohm(0)
        raise ValueError("Unknown node '{}'".format(repr(node)))
    
    @lru_cache(2048, typed=True)
    def load_impedance(self, node:_S, frequency:hertz = hertz(0), incl_self=True) -> Optional[ohm]:
        if isinstance(node, NegativePole):
            return ohm(0)
        impedances = [
            z
            for z in [self.load_impedance(n, frequency) for n in self[node].successors]
            if z is not None
        ]
        if len(impedances) == 0:
            return None
        load_impedance = ohm(harmonic_sum([z for z in impedances if z is not None]))
        if incl_self:
            load_impedance = ohm(load_impedance + self.self_impedance(node, frequency))
        return load_impedance

    @lru_cache(2048, typed=True)
    def voltage_drop(self, node: _S, frequency:hertz = hertz(0)) -> volt|None:
        current = self.electric_current(node, frequency)
        self_impedance = self.self_impedance(node, frequency)
        return current * self_impedance
    
    @lru_cache(2048, typed=True)
    def voltage_in(self, node: _S, frequency:hertz = hertz(0)) -> volt|None:
        successors = [
            s for s in self[node].successors
            if s not in self[node].predecessors
            and not isinstance(s, PositivePole)
        ]
        
        if len(successors) == 0:
            if isinstance(node, NegativePole):
                return volt(0.0)
            return self.voltage_out(list(self[node].predecessors)[0], frequency)
         
        V_out = None
        for s in successors:
            v = self.voltage_in(s, frequency)
            if v is None:
                continue
            if V_out is None:
                V_out = v
            if round(v.real, 4) != round(V_out.real, 4):
                logger.warning('The V_in of the successors of %s does not match. (%s, %s)', node, float(V_out.real), float(v.real))
        
        if V_out is None:
            logger.warning('Node %s does not have a V_out. %s', node, self[node].predecessors)
            V_out = volt(0.0)
        
        V_drop = self.voltage_drop(node, frequency)
        if V_drop is None:
            return V_out
        return volt(V_out + V_drop)
    
    @lru_cache(2048, typed=True)
    def voltage_out(self, node: _S, frequency:hertz = hertz(0)) -> volt|None:
        if len(self[node].successors) == 0:
            return None
        V_in = self.voltage_in(node, frequency)
        if V_in is None:
            return None
        V_drop = self.voltage_drop(node, frequency)
        if V_drop is None:
            return V_in
        return volt(V_in - V_drop)
    
    @lru_cache(2048, typed=True) 
    def electric_currents(self, node:_S, frequency:hertz) -> Dict[_S, ampere]:
        if len(self[node].predecessors) == 0:
            incoming_currents = [ampere(1.0)]
        elif isinstance(node, NegativePole):
            incoming_currents = []
        else:
            incoming_currents = [
                self.electric_currents(p, frequency).get(node, ampere(-1000))
                for p in self[node].predecessors
            ]
        
        successors = list(self[node].successors)
        impedances = [self.load_impedance(s, frequency) for s in successors]
        
        I_total = ampere(sum([i for i in incoming_currents if i is not None]))
        Z_total = ohm(harmonic_sum([z for z in impedances if z is not None]))
        
        result:dict[_S, ampere] = {}
        for z,s in zip(impedances, successors):
            if z is None:
                continue
            result[s] = current_divider(I_total, ohm(z), Z_total)
        
        return result
    
    @lru_cache(2048, typed=True)
    def electric_current(self, node:_S, frequency:hertz) -> ampere:
        if len(self[node].predecessors) == 0 and isinstance(node, PositivePole):
            return ampere(1.0)
        elif len(self[node].successors) == 0:
            return ampere(0.0)
        incoming_currents = [
            self.electric_currents(p, frequency).get(node, ampere(-1000))
            for p in self[node].predecessors
        ]
        return ampere(sum([i for i in incoming_currents if i is not None]))
    
    def _build_digraph(self) -> None:
        seen: set[Edge] = set() 
        queue: list[_S] = list([self.initial_port.pos])
        self[self.initial_port.pos].paths.add(tuple([self.initial_port.pos]))
        while len(queue) > 0:
            item = queue.pop(0)
            for n in set(nx.neighbors(self.graph, item)): # type: ignore
                if item in self._terminals and n not in self._terminals:
                    continue
                if (n, item) not in seen and (item, n) not in seen:
                    seen.add((item, n))
                    queue.append(n)
                    self._connect_nodes(item, n)
                    if self._is_transient(item) and self._is_transient(n):
                        self._connect_nodes(n, item)

    def _connect_nodes(self, first: _S, second: _S):
        self[first].successors.add(second)
        self[second].predecessors.add(first)
        for p in self[first].paths:
            self[second].paths.add(tuple([*p, second]))
    
    def to_nx_graph(self, test_f:hertz=hertz(100e3)) -> nx.Graph:
        res = nx.DiGraph()
        for n in self.keys():
            res.add_node(n, **self[n])
            res.nodes[n]["subset"] = 0 - max([len(p) for p in self[n].paths])
            res.nodes[n]["zs"] = ohm(self.self_impedance(n, test_f))
            res.nodes[n]["z"] = self.load_impedance(n, test_f, False)
            res.nodes[n]["v_drop"] = self.voltage_drop(n, test_f)
            res.nodes[n]["v_in"] = self.voltage_in(n, test_f)
            res.nodes[n]["v_out"] = self.voltage_out(n, test_f)
            res.nodes[n]["i"] = self.electric_current(n, test_f)
            
            currents = self.electric_currents(n, test_f)
            for s in self[n].successors:
                res.add_edge(
                    n,
                    s, 
                    v=res.nodes[n]["v_out"],
                    z=self.load_impedance(s, test_f),
                    i=currents.get(s, ampere(0))
                )
        return res


if __name__ == "__main__":
    from typing import Optional
    from property import Resistance
    from electrify.network.filter import LowPassFilter
    from network import  Property
    from electrify.plot.drawcircuit import draw_circuit
    from electrify.value.unit1 import *
    import matplotlib.pyplot as plt
    from electrify.plot import BodePlotManager, get_domain
    
    f_min=1e6
    f_max=30e6
    f_target=15e6 
    f_graph=15e6
    z_load=50
    num_samples = 100
    d = get_domain(f_min, f_max, num_samples)

    lpf = LowPassFilter(hertz(f_target), 5)
    lpf.add_series([lpf[2].pos, Resistance(ohm(50)), lpf[2].neg])
    sln =  DirectedSolution(lpf, lpf._ports[1])
    digraph = sln.to_nx_graph(hertz(f_graph))
    draw_circuit(digraph)

    y_data = []
    for f in d:
        p1 = sln.voltage_in(lpf._ports[1].pos, f)
        if p1 is not None:
            p1 = p1 / 2.0
        else:
            raise 
        p2 = sln.voltage_in(lpf._ports[2].pos, f)
        if p2 is None or p1 is None:
            raise
        y_data.append(p2/p1)

    fig, ax = plt.subplots()
    bpm = BodePlotManager(ax)
    bpm.configure(
        d,
        hlines=[-3],
        vlines=[f_target, f_target*2.0, f_graph],
        f_min=f_min,
        f_max=f_max
    )
    bpm.plot_fq([attenuation_factor(y) for y in y_data])
    bpm.plot_ph([volt(y).phase_angle / 6.28 * 360 for y in y_data])
    plt.show()
