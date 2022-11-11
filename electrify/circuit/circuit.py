from functools import lru_cache
import collections
import logging

import numpy as np
import networkx as nx

from .reducer import Reducer
from .solver import CircuitSolver

from ..component import Node, Gnd, Source, Terminal, Load


np.set_printoptions(precision=2)
logging.basicConfig(encoding='utf-8', format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class Circuit(nx.Graph):
    logger = logger

    irreducible_types = (Source, Gnd, Load)

    def __init__(self):
        nx.Graph.__init__(self)
        self.name = str(hex(id(self)))
        self.GND = Gnd()
        self.last = None
        self.source_node = None
        self.load_node = None
        self.terminal_map = collections.defaultdict(lambda: {'A': None, 'B': None})
        self.reduction_stats = None
        self.solver = CircuitSolver(self)

    def __str__(self):
        return '<Circuit \'{}\' n={} e={}>'.format(
            self.name,
            len(list(self.nodes())),
            len(list(self.edges()))
        )

    def reduce(self, series=True, parallel=True, nodal=True, max_iteration=10):
        reducer = Reducer(series, parallel, nodal)
        opt_count = 0
        i = 1
        while i <= max_iteration:
            i += 1
            opts = reducer.reduce(self)
            opt_count += opts
            if opts == 0:
                break
        return self

    @lru_cache(2048, typed=True)
    def solve(self, source=None, f=0, load=None):
        if source is None:
            source = self.source_node
        return self.solver.solve(f=f, source=source, load=load)

    def __add__(self, value):
        return self.add(value)

    def add_element(self, e):
        logger.debug('Adding element: %s', e)
        if isinstance(e, Node):
            self.add_node(e)
        elif isinstance(e, nx.Graph):
            self.add_edges_from(e.edges())
        else:
            self.add(e)
        return self

    def _terminalize(self, e):
        print('*'*20, e)
        logger.debug('__TERM   %s', e)
        if e in self.terminal_map.keys():
            return (e, e)

        e_neighbors = list(self.neighbors(e))
        A = Terminal(e, 'A')
        B = Terminal(e, 'B')

        self.add_element(A)
        self.add_element(B)

        self.terminal_map[e]['A'] = A
        self.terminal_map[e]['B'] = B

        for n in e_neighbors:
            self.remove_edge(n, e)
            self.add_edge(n, A)

        self.add_edge(A, e)
        self.add_edge(e, B)

        return A, B

    def _connections(self, u):
        if u not in self.terminal_map:
            return set(self.neighbors(u))
        else:
            conns = set()
            for t in self.terminal_map[u]:
                conns.union(self.neighbors(self.terminal_map[u][t]))
            return conns

    def _connect(self, u, v):
        logger.debug('_CONN    %s    %s', u, v)
        if isinstance(u, nx.Graph):
            u = u.B
        if isinstance(v, nx.Graph):
            v = v.A
        if isinstance(u, Node) or isinstance(v, Node):
            self.add_edge(u, v)
            return self

        v_connections = self._connections(v)
        if u in v_connections:
            return self

        if len(v_connections) == 2:
            _, v = self._terminalize(v)

        u_connections = self._connections(u)
        if len(u_connections) == 2:
            u, _ = self._terminalize(u)

        self.add_edge(u, v)
        return self

    def wire(self, u, v):
        logger.debug('WIRE     %s    %s', u, v)
        nodes = list(self.nodes())
        if u not in nodes:
            self.add_element(u)
        if v not in nodes:
            self.add_element(v)
        self._connect(u, v)

        self.last = v
        return self

    def add(self, element, set_latest=True):
        self.logger.debug('ADDING:  %s of type %s', element, type(element))
        if isinstance(element, Source):
            if self.source_node is None:
                logger.debug('%s: Setting as source', element)
                self.source_node = element
            if element.GND is None:
                logger.debug('%s: Setting element GND:  %s', element, self.GND)
                element.GND = self.GND
            if self.last is not None:
                self.add_edge(self.last, element)
            if set_latest:
                self.last = element
        elif isinstance(element, Load):
            if self.load_node is None:
                logger.debug('%s: Setting as load', element)
                self.load_node = element
            if element.GND is None:
                logger.debug('%s: Setting element GND:  %s', element, self.GND)
                element.GND = self.GND
            if self.last is not None:
                self.add_edge(self.last, element)
            if set_latest:
                self.last = element
        elif isinstance(element, (Parallel, Series, Shunt)):
            if self.last is not None:
                self.add_edge(self.last, element.A)
            self.add_edges_from(element.edges())
            if set_latest:
                self.last = element.B
        elif self.last is not None:
            self.add_edge(self.last, element)
            if set_latest:
                self.last = element
        else:
            self.add_node(element)
            if set_latest:
                self.last = element
        return self

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.name)


class Parallel(Circuit):
    def __init__(self, *elements):
        super().__init__()
        self.A = Node(name='PARALLEL_A')
        self.B = Node(name='PARALLEL_B')
        self.add_node(self.A)
        self.add_node(self.B)
        for e in elements:
            self.wire(self.A, e)
            self.wire(e, self.B)
        self.last = self.B


class Series(Circuit):
    def __init__(self, *elements):
        super().__init__()
        self.A = Node(name="SERIES_A")
        self.B = Node(name="SERIES_B")
        self.add_node(self.A)
        self.add_node(self.B)

        for e in elements:
            self.add_element(e)

        for u, v in zip(elements, elements[1:]):
            self.wire(u, v)

        self.wire(self.A, elements[0])
        self.wire(elements[-1], self.B)
        self.last = self.B


class Shunt(Circuit):
    def __init__(self, *elements, to=None):
        super().__init__()

        self.to = to
        self.A = Node()
        self.B = self.A

        elements = [self.A, *elements]
        if to is not None:
            elements.append(to)
        for u, v in zip(elements, elements[1:]):
            self.wire(u, v)
        self.last = self.B
