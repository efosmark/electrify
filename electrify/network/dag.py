"""
Network solver that utilizes a directed-acyclic-graph.

This utilizes nodal analysis and the concept of superposition.
Each source should incorporate its own targeted DAG.
"""
from collections import defaultdict
from typing import Any, Generic, Optional, Protocol, TypeVar, Callable
import networkx as nx
import cmath

from electrify.formula.general import current_divider, get_item_impedance
from electrify.value.unit import *
from electrify.formula.sum import sum_parallel_impedance


CurrentResult = dict[Any, ampere]
CurrentFuncType = Callable[[hertz], CurrentResult]
ImpedanceFuncType = Callable[[hertz], ohm]


class Valuable(Protocol):
    """Prototype describing objects that have a value() method."""

    def value(self) -> Any:
        """Get the internal value of the object."""
        ...


_V = TypeVar("_V", bound=Valuable)


# class Stack(Generic[_V]):
#     _stack: list[_V]

#     def __init__(self, initial: Optional[Sequence[_V]] = None):
#         self._stack = []
#         if initial is not None:
#             self._stack.extend(initial)

#     def pop(self) -> Optional[_V]:
#         return self._stack.pop()

#     def push(self, value: _V):
#         self._stack.append(value)

#     def push_all(self, iterable: Sequence[_V]):
#         self._stack.extend(iterable)

#     def __iter__(self) -> Generator[_V, None, None]:
#         while len(self._stack) > 0:
#             item = self.pop()
#             if item is not None:
#                 yield item

#     def __len__(self):
#         return len(self._stack)


class DirectedGraphNode(Generic[_V]):
    """
    DAG nodes hold references to each of its predecessors and its successors.

    This should not need to be instanced directly.
    """

    predecessors: set[_V]
    successors: set[_V]

    def __init__(self, node: Optional[_V] = None):
        """
        Create a new instance of a directed graph node.

        This should not need to be instanced directly.

        Args:
            node (Optional[_V], optional): _description_. Defaults to None.
        """
        self.node = node
        self.successors = set()
        self.predecessors = set()

    @property
    def neighbors(self) -> set[_V]:
        """
        Get the set of all connected nodes, regardless of direction.

        Returns:
            set[_V]: A set containing both sucessors and predecessors.
        """
        return self.successors | self.predecessors

    def __repr__(self):
        return f'p:{len(self.predecessors)} s:{len(self.successors)}'


class TargetedDAG(defaultdict[_V, DirectedGraphNode[_V]]):
    """A directed acyclic graph that connects paths between a given source and target."""

    source: _V
    target: _V

    def __init__(self, graph, source: _V, target: _V):
        """Build a directed acyclic graph from paths that start at `src` and end at `target`."""
        defaultdict.__init__(self, DirectedGraphNode[_V])
        self.source = source
        self.target = target

        seen: set[_V] = set()
        side: bool = True

        top_queue: list[_V] = [source]
        bottom_queue: list[_V] = [target]

        while len(top_queue) > 0 or len(bottom_queue) > 0:
            side = not side
            q = top_queue if side else bottom_queue
            if len(q) > 0:
                item = q.pop(0)
                if item in seen:
                    continue
                seen.add(item)
                for n in set(nx.neighbors(graph, item)) - seen:
                    if n not in q and n not in seen:
                        q.append(n)
                    if side:
                        self._connect_nodes(item, n)
                    else:
                        self._connect_nodes(n, item)

    def _connect_nodes(self, first: _V, second: _V):
        if first not in self[second].neighbors:
            self[first].successors.add(second)
            self[second].predecessors.add(first)


class SolvableDAG(TargetedDAG[_V]):
    """Representation of a targeted acyclic graph that allows for solving electric quantities."""

    Z_funcs: dict[_V, Callable] = {}
    I_funcs: dict[_V, Callable] = {}

    def impedance(self, frequency: hertz, item: Optional[_V] = None) -> ohm:
        """
        Get the complex impedance of the given item at a specific frequency.

        If the item is omitted, it will default to getting the impedance of the
        entire network from source to target.

        Args:
            frequency (hertz): _description_
            item (Optional[_V], optional): _description_. Defaults to None.

        Returns:
            ohm: _description_
        """
        if item is None:
            item = self.source
        if len(self.Z_funcs) == 0:
            self._compute_impedance_funcs()
        return self.Z_funcs[item](frequency)

    def current(self, item: _V, frequency: hertz) -> ampere:
        """
        Get the electric current of a given item.

        Args:
            item (_V): _description_
            frequency (hertz): _description_

        Returns:
            ampere: _description_
        """
        return self.I_funcs[item](frequency)[item]

    def voltage(self, item: _V, frequency: hertz) -> volt:
        """
        Get the voltate drop found across the given item at the given frequency.

        Args:
            item (_V): The item over which the voltage drop occurs.
            frequency (hertz): The frequency of interest.

        Returns:
            volt: The voltage drop across the item.
        """
        Z = self.impedance(frequency, item)
        I = self.current(item, frequency)
        return volt(Z * I)

    def _compute_current_funcs(self):
        self.I_funcs = {}
        stack = [self.target]
        while len(stack) > 0:
            item = stack.pop()
            needed = []
            for p in self[item].predecessors:
                if p not in self.I_funcs:
                    needed.append(p)
            if len(needed) > 0:
                stack.append(item)
                stack.extend(needed)
                continue
            self.I_funcs[item] = self._create_If(item)

    def _compute_impedance_funcs(self):
        self.Z_funcs = {}
        stack = [self.source]
        while len(stack) > 0:
            item = stack.pop()
            needed = []
            for s in self[item].successors:
                if s not in self.Z_funcs:
                    needed.append(s)
            if len(needed) > 0:
                stack.append(item)
                stack.extend(needed)
                continue
            self.Z_funcs[item] = self._create_Zf(item)

    def _create_If(self, item) -> CurrentFuncType:
        incoming_current_funcs = [self.I_funcs[p] for p in self[item].predecessors]

        def __If(f: hertz) -> CurrentResult:
            if len(incoming_current_funcs) == 0:
                I_total = 1.0
            else:
                I_total = sum(i(f)[item] for i in incoming_current_funcs)
            result: dict[Any, ampere] = {
                item: ampere(I_total)
            }
            Z_branch = dict([(s, self.Z_funcs[s](f)) for s in self[item].successors])
            Z_load = sum_parallel_impedance(list(Z_branch.values()))
            for s in self[item].successors:
                result[s] = current_divider(ampere(I_total), Z_branch[s], Z_load)
                result[s] = ampere(
                    result[s].real
                    if cmath.isclose(result[s], result[s].real)
                    else result[s]
                )
                result[s] = ampere(result[s])
            return result
        return __If

    def _create_Zf(self, item):

        def __Zf(frequency: hertz):
            impedance_funcs = [self.Z_funcs[s] for s in self[item].successors]
            Z_self = get_item_impedance(item.value(), frequency)
            Z_load = sum_parallel_impedance([i(frequency) for i in impedance_funcs])
            return ohm(Z_self + Z_load)
        return __Zf
