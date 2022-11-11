import logging

import numpy as np


from ..component import Node, Gnd, Capacitor, Inductor, Resistor, Source, Terminal, Load, ReactiveComponent
from ..math import magnitude, parallel_resistance, series_resistance, series_capacitance, parallel_capacitance, series_inductance, parallel_inductance, solve_for_V, solve_for_I


np.set_printoptions(precision=2)
logging.basicConfig(encoding='utf-8', format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class parallelset(set):
    pass


def _add_to_meld_group(meld_groups, u, v, is_parallel=False):
    if u in meld_groups:
        meld_groups[v] = meld_groups[u]
        meld_groups[v].add(v)
    elif v in meld_groups:
        meld_groups[u] = meld_groups[v]
        meld_groups[u].add(u)
    else:
        if is_parallel:
            g = parallelset()
        else:
            g = set()
        g.add(u)
        g.add(v)
        meld_groups[u] = g
        meld_groups[v] = g
    return meld_groups


def combine_elements(*nodes, is_parallel=False):
    logger.debug("Combining nodes (parallel=%s): %s", is_parallel, nodes)
    if isinstance(nodes[0], Node):
        n = Node()
    elif isinstance(nodes[0], Capacitor):
        if is_parallel:
            n = Capacitor(parallel_capacitance(*[c.value for c in nodes]))
        else:
            n = Capacitor(series_capacitance(*[c.value for c in nodes]))
    elif isinstance(nodes[0], Inductor):
        if is_parallel:
            n = Inductor(parallel_inductance(*[i.value for i in nodes]))
        else:
            n = Inductor(series_inductance(*[i.value for i in nodes]))
    elif isinstance(nodes[0], Resistor):
        if is_parallel:
            n = Resistor(parallel_resistance(*[r.value for r in nodes]))
        else:
            n = Resistor(series_resistance(*[r.value for r in nodes]))
    else:
        raise TypeError("Cannot combine nodes:{}".format(nodes))
    logger.debug('Combined: %s', n)
    return n


class Reducer(object):
    logger = logger
    irreducible_types = (Source, Gnd, Load)

    def __init__(self, in_place=False, series=True, parallel=True, nodal=True, frequency=None, max_iterations=10):
        self._in_place = in_place
        self._series = series
        self._parallel = parallel
        self._nodal = nodal
        self._frequency = frequency
        self._max_iterations = max_iterations

    def reduce(self, circuit):
        self.logger.debug('Beginning reduce operation on %s.', circuit)
        meld_groups = dict()
        replace_with = dict()
        redundant = set()
        remove_node = set()
        opt_count = 0

        def should_skip(n):
            return isinstance(n, self.irreducible_types) \
                or n in remove_node \
                or n in meld_groups \
                or n in replace_with \
                or n in redundant

        for node in circuit.nodes():
            if should_skip(node):
                continue

            if self._frequency is not None and isinstance(node, ReactiveComponent):
                replace_with[node] = Resistor(magnitude(node.impedance(self._frequency)))
                self.logger.debug(' :: #Replacement candidate found: %s replaced with %s', node, replace_with[node])
                continue

            neighbors = set(circuit.neighbors(node))
            for n in neighbors:
                if should_skip(n):
                    continue

                # Reactive replacement
                if self._frequency is not None and isinstance(n, ReactiveComponent):
                    replace_with[n] = Resistor(magnitude(n.impedance(self._frequency)))
                    self.logger.debug(' :: Replacement candidate found: %s replaced with %s', n, replace_with[n])
                    continue

                # Touching nodes
                elif self._nodal and isinstance(n, Node) and isinstance(node, Node):
                    _add_to_meld_group(meld_groups, n, node)
                    self.logger.debug(' :: Nodal group found: %s %s', node, n)
                    continue

                # Series optimization
                elif self._series and circuit.degree(n) == 2 and isinstance(n, type(node)):
                    _add_to_meld_group(meld_groups, n, node)
                    self.logger.debug(' :: Series candidate found: %s and %s', node, n)
                    continue

                # Redundant node
                elif self._nodal and isinstance(n, Node) and circuit.degree(n) == 2:
                    redundant.add(n)
                    self.logger.debug(' :: Redundant node found: %s', n)
                    continue

                elif self._parallel:
                    for n2 in neighbors:
                        if should_skip(n2) or n2 is n:
                            continue

                        # Parallel optimization
                        if type(n2) == type(n) and set(circuit.neighbors(n2)) == set(circuit.neighbors(n)):
                            self.logger.debug(' :: Parallel candidate found: %s and %s', n2, n)
                            _add_to_meld_group(meld_groups, n, n2, is_parallel=True)
                            break
                    continue

        if len(replace_with) > 0:
            opt_count += self._process_replacement_nodes(circuit, replace_with, remove_node)

        if len(meld_groups):
            opt_count += self._process_combining_nodes(circuit, meld_groups, remove_node)

        if len(redundant):
            opt_count += self._process_redundant_nodes(circuit, redundant, remove_node)

        if len(remove_node):
            opt_count += self._process_node_removal(circuit, remove_node)

        self.logger.debug('Reduce complete with %s optimizations applied.', opt_count)
        return opt_count

    def _process_combining_nodes(self, circuit, meld_groups, remove_node):
        self.logger.debug('Combining up to %s groups of nodes.', len(meld_groups.values()))
        opt_count = 0
        melded_groups = set()
        for group in meld_groups.values():
            is_parallel = isinstance(group, parallelset)
            group = frozenset(group)

            if group in melded_groups or len(group) <= 1:
                continue

            elif len([g for g in group if g in remove_node]) > 0:
                continue

            n = combine_elements(*group, is_parallel=is_parallel)
            for node in group:
                self.clone_edges(circuit, node, n)
                remove_node.add(node)

            opt_count += 1
            melded_groups.add(group)
        self.logger.debug('Combined %s nodes.', opt_count)
        return opt_count

    def _process_redundant_nodes(self, circuit, redundant, remove_node):
        self.logger.debug('Removing redundant nodes: %s', redundant)
        opt_count = 0

        for rn in redundant:
            if rn not in circuit.nodes() or rn in remove_node:
                continue
            can_be_removed = False
            neighbors = list(circuit.neighbors(rn))
            for n in neighbors:
                if n not in circuit.nodes() or n in remove_node:
                    continue
                for n2 in neighbors:
                    if n2 is n or n2 in remove_node:
                        continue
                    can_be_removed = True
                    circuit.add_edge(n, n2)
            if can_be_removed:
                opt_count += 1
                remove_node.add(rn)
        self.logger.debug('Redundant nodes removed: %s', opt_count)
        return opt_count

    def _process_replacement_nodes(self, circuit, replace_with, remove_node):
        opt_count = 0
        for orig_node, new_node in replace_with.items():
            self.clone_edges(circuit, orig_node, new_node)
            remove_node.add(orig_node)
            opt_count += 1
        return opt_count

    def _process_node_removal(self, circuit, remove_node):
        for n in remove_node:
            if n in circuit.nodes():
                circuit.remove_node(n)
        return 0

    def clone_edges(self, circuit, source, target):
        self.logger.debug("Cloning edges from %s to %s", source, target)
        for p in circuit.neighbors(source):
            if p is not target:
                circuit.add_edge(p, target)
