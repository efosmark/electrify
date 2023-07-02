from collections import defaultdict
from functools import lru_cache
import logging

import networkx as nx
import numpy as np

from ..common import parallel_resistance, voltage_divider, phase_angle
from ..element.component import Gnd, Node, Source
from ..formula.rf import magnitude
from ..value.value import format_value

logging.basicConfig(encoding='utf-8', format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

VOLTAGE = 'voltage'
VOLTAGE_DROP = 'volt_drop'
CURRENT = 'current'
CURRENT_SELF = 'current_self'
RES_SELF = 'res_self'
RES_TOTAL = 'res_total'
RES_UNLOADED_TOTAL = 'res_unloaded'
POWER_DISSIPATED = 'pwr_dis'
POWER_TOTAL = 'pwr_tot'

class CircuitSolver:
    logger = logger

    def __init__(self, circuit):
        self.c = circuit
        self.is_solved = False
        self.sln = defaultdict(dict)

    def annotate(self):
        """
        """
        for el, data in self.sln.items():
            for key, val in data.items():
                self.c.nodes[el][key] = val

    def solve(self, f=0, source=None, load=None):
        """
        """
        if source is None:
            if self.c.source_node is None:
                raise Exception('No source specified.')
            source = self.c.source_node

        self.sln = defaultdict(dict)
        for edge in self.c.edges():
            try:
                del self.c.edges[edge][VOLTAGE]
            except KeyError:
                pass

        depths = self._get_depths(source)
        self._compute_resistances(depths, f, load)
        self._compute_voltages(depths)
        self.is_solved = True
        return self.sln

    def _compute_element_voltage(self, el):
        """
        """
        if isinstance(el, Source):
            return el.voltage
        voltage = 0
        for n in self.c[el]:
            voltage += self.c.edges[el, n].get(VOLTAGE, 0)
        return voltage

    @lru_cache(1000, typed=True)
    def _get_depths(self, source):
        """
        """
        self.logger.debug('_get_depths(%s)', source)
        bfs = dict(enumerate(nx.bfs_layers(self.c, [source])))
        element_depths = defaultdict(list)
        for depth in sorted(bfs.keys()):
            element_depths[0 - depth] = bfs[depth]
            for el in bfs[depth]:
                self.c.nodes[el]['layer'] = 0 - depth
        return element_depths

    def _compute_resistances(self, depths, f, load=None):
        """
        """
        self.logger.debug('load: %s', load)
        for depth in sorted(depths.keys()):
            for el in depths[depth]:
                fwd_res = []
                fwd_res_unloaded = []
                for n in self.c[el]:
                    if self.c.nodes[n]['layer'] < depth:
                        self.c.edges[el,
                                     n][RES_TOTAL] = self.sln[n][RES_TOTAL] - self.sln[el].get(RES_SELF, 0.0)
                        fwd_res.append(self.sln[n][RES_TOTAL])
                        if n is not load:
                            fwd_res_unloaded.append(self.sln[n][RES_UNLOADED_TOTAL])
                res_self = el.impedance(f)
                self.sln[el][RES_SELF] = res_self
                self.sln[el][RES_TOTAL] = self.sln[el][RES_SELF] + parallel_resistance(*fwd_res)
                self.sln[el][RES_UNLOADED_TOTAL] = np.inf
                if el != load:
                    self.sln[el][RES_UNLOADED_TOTAL] = self.sln[el][RES_SELF] + \
                        parallel_resistance(*fwd_res_unloaded)
                self.sln[el]['equation'] = '({})'.format(
                    '||'.join(format_value(r, places=0) for r in fwd_res))

    def _compute_voltages(self, depths):
        """
        """
        for depth in sorted(depths.keys(), reverse=True):
            for el in depths[depth]:
                voltage = self._compute_element_voltage(el)   # Real voltage presented to element
                # Complex impedance of all forward elements
                res_total = self.sln[el][RES_TOTAL]
                res_self = self.sln[el][RES_SELF]             # Complex impedance of this element
                if np.isinf(res_self) or res_total == 0:
                    continue

                current = voltage / res_total                 # Complex current
                current_self = voltage / res_self if res_self != 0 else 0                # Complex current

                v_drop = current * res_self                   # Complex voltage drop
                v_out = voltage - v_drop                      # Real voltage presented from this element

                self.sln[el]['volt_out'] = v_out
                self.sln[el][CURRENT] = current
                self.sln[el][CURRENT_SELF] = current_self
                self.sln[el][VOLTAGE] = voltage
                self.sln[el][VOLTAGE_DROP] = v_drop

                for n in self.c[el]:
                    nlayer = self.c.nodes[n].get('layer', 0)
                    if nlayer >= self.c.nodes[el]['layer']:
                        continue

                element_layer = self.c.nodes[el]['layer']
                for n in self.c[el]:
                    if self.c.nodes[n]['layer'] < element_layer:
                        self.c.edges[(el, n)][VOLTAGE] = v_out
                        if self.c.edges[(el, n)][RES_TOTAL]:
                            self.c.edges[(el, n)][CURRENT] = v_out / self.c.edges[(el, n)][RES_TOTAL]
                        else:
                            self.c.edges[(el, n)][CURRENT] = 0


# def voltage_gain_db(f, c):
#     sln = c.solve(f=f, source=c.source_node, load=c.load_node)
#     V_in = voltage_divider(
#         sln[c.source_node]['voltage'],    # V_source
#         sln[c.source_node]['res_self'],   # R_source
#         sln[c.load_node]['res_self']      # R_load
#     )
#     V_load = sln[c.load_node]['voltage']  # V_load
#     if V_load == 0:
#         return 0, 0
#     gain = V_load / V_in
#     return ((20 * np.log10(gain)).real), e.math.phase_angle(gain, deg=True)


# def current_gain_db(f, c):
#     sln = c.solve(f=f, source=c.source_node, load=c.load_node)

#     C_source = magnitude(sln[c.source_node]['current']
#                          ) - magnitude(sln[c.source_node]['current_self'])
#     C_load = magnitude(sln[c.load_node]['current_self'])

#     return (20 * np.log10(C_load / C_source)) if C_source != 0 else 0


# def power_gain_db(f, c):
#     sln = c.solve(f=f, source=c.source_node, load=c.load_node)

#     src_v = sln[c.source_node]['voltage']
#     src_z = sln[c.load_node]['res_self'] * 4.0
#     S = src_v**2 / src_z

#     load_v = sln[c.load_node]['voltage']
#     load_z = sln[c.load_node]['res_self']
#     L = load_v**2 / load_z

#     return 10 * np.log10(L / S)


# def power_gain2_db(f, c):
#     sln = c.solve(f=f, source=c.source_node, load=c.load_node)
#     Gt = transducer_gain(
#         VL=sln[c.load_node]['voltage'],
#         RL=sln[c.load_node]['res_self'],
#         VIN=sln[c.source_node]['voltage'],
#         RS=sln[c.source_node]['res_self']
#     )
#     return 10 * np.log10(Gt)
