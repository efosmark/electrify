import logging

from ..element.component import Node, Gnd, Capacitor, Inductor, Resistor, Source, ResistiveLoad, ReactiveComponent
from ..common import parallel_resistance, series_resistance
from ..formula.capacitance import series_capacitance, parallel_capacitance
from ..formula.inductance import series_inductance, parallel_inductance
from ..formula.rf import magnitude

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


def _combine_capacitors(*nodes, is_parallel=False):
    value_list = [i.value for i in nodes]
    if is_parallel:
        new_cap_value = parallel_capacitance(*value_list)
    else:
        new_cap_value = series_capacitance(*value_list)
    return Capacitor(new_cap_value)


def _combine_inductors(*nodes, is_parallel=False):
    value_list = [i.value for i in nodes]
    if is_parallel:
        return Inductor(parallel_inductance(*value_list))
    return Inductor(series_inductance(*value_list))


def _combine_resistors(nodes, is_parallel):
    if is_parallel:
        n = Resistor(parallel_resistance(*[r.value for r in nodes]))
    else:
        n = Resistor(series_resistance(*[r.value for r in nodes]))


def combine_elements(*nodes, is_parallel=False):
    logger.debug("Combining nodes (parallel=%s): %s", is_parallel, nodes)
    if isinstance(nodes[0], Node):
        n = Node()
    elif isinstance(nodes[0], Capacitor):
        n = _combine_capacitors(nodes, is_parallel)
    elif isinstance(nodes[0], Inductor):
        n = _combine_inductors(nodes, is_parallel)
    elif isinstance(nodes[0], Resistor):
        n = _combine_resistors(nodes, is_parallel)
    else:
        raise TypeError("Cannot combine nodes:{}".format(nodes))
    logger.debug('Combined: %s', n)
    return n


class Reducer(object):
    logger = logger
    irreducible_types = (Source, Gnd, ResistiveLoad)

    def __init__(
            self, in_place=False, series=True, parallel=True, nodal=True, frequency=None,
            max_iterations=10):
        """
        fdaf
        """
        self._in_place = in_place
        self._series = series
        self._parallel = parallel
        self._nodal = nodal
        self._frequency = frequency
        self._max_iterations = max_iterations

    def reduce(self, circuit):
        """
        ---
        """
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
                replace_with[node] = Resistor(magnitude(node.impedance(self._frequency) or 0))
                self.logger.debug(
                    ' :: #Replacement candidate found: %s replaced with %s', node,
                    replace_with[node])
                continue

            neighbors = set(circuit.neighbors(node))
            for n in neighbors:
                if should_skip(n):
                    continue

                # Reactive replacement
                if self._frequency is not None and isinstance(n, ReactiveComponent):
                    replace_with[n] = Resistor(magnitude(n.impedance(self._frequency) or 0))
                    self.logger.debug(
                        ' :: Replacement candidate found: %s replaced with %s', n, replace_with
                        [n])
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
                        if type(n2) == type(n) and set(
                                circuit.neighbors(n2)) == set(
                                circuit.neighbors(n)):
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
        """
        Clone all edges from `source` and add them to `target`.

        Parameters
        ----------
        circuit : int or tuple of int
            Shape of the empty matrix.
        source : data-type, optional
            Desired output data-type.
        target : {'C', 'F'}, optional
            Whether to store multi-dimensional data in row-major
            (C-style) or column-major (Fortran-style) order in
            memory.

        See Also
        --------
        empty_like, zeros

        Notes
        -----
        `empty`, unlike `zeros`, does not set the matrix values to zero,
        and may therefore be marginally faster.  On the other hand, it requires
        the user to manually set all the values in the array, and should be
        used with caution.

        Examples
        --------
        >>> import numpy.matlib

        """
        self.logger.debug("Cloning edges from %s to %s", source, target)
        for p in circuit.neighbors(source):
            if p is not target:
                circuit.add_edge(p, target)
