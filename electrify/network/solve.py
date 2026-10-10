from functools import lru_cache
from collections import defaultdict
import functools
import random
from typing import *
from electrify import ac
from electrify.quantity import power

from electrify.types import ampere, volt, ohm, hertz, watt, SupportsImpedance
from electrify.util import StackLogger
from electrify.dc import current_divider, voltage_divider, harmonic_sum
from electrify.ac import impedance
from .network import PortNetwork
from .net import Net

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stack_logger = StackLogger(logger, log_level=logging.DEBUG, compact=True)

class SolutionException(Exception):...
class UndefinedImpedance(SolutionException):...
class UndefinedElectricCurrent(SolutionException):...

def split_paths(all_paths):
    paths_to_src = defaultdict(set)
    paths_to_end = defaultdict(set)
    for path in all_paths:
        for i, node in enumerate(path):
            if i > 0:
                paths_to_src[node].add(path[i-1::-1])
            if i < len(path)-1:
                paths_to_end[node].add(path[i+1:])
    return paths_to_src, paths_to_end

def noise(level=1.0):
    if level == 0:
        return 0
    noise = random.random()*level
    if random.random() > 0.5:
        noise = 0 - noise
    return noise


def add_noise(input, amount):
    if amount == 0:
        return input
    noise = random.random() * (input * amount)
    if random.random() > 0.5:
        noise = 0 - noise
    return input + noise

def noisy(func):
    @functools.wraps(func)
    def nfunc(*args, **kwargs):
        result = func(*args, **kwargs)
        return add_noise(result, 0.05)
    return nfunc

class Solution:
    paths_to_src:dict[Any, set[tuple]]
    paths_to_end:dict[Any, set[tuple]]
    logger:ClassVar[logging.Logger] = logger
    
    def __init__(self, network:PortNetwork, src_ref:Any, zero_ref:Any):
        self.set_network(network, src_ref, zero_ref)
    
    def set_network(self, network:PortNetwork, src_ref:Any, zero_ref:Any):
        self.network = network
        self.src_ref = src_ref
        self.zero_ref = zero_ref
        self.paths_to_src, self.paths_to_end = split_paths(self.network.paths_between(src_ref, zero_ref))
        
        # for n in {**self.paths_to_src, **self.paths_to_end}:
        #     print()
        #     print(self.network.id(n), n)
        #     print('  to-src:')
        #     for p in self.paths_to_src[n]:
        #         print(f'    - {p}')
        #     print('  to-end:')
        #     for p in self.paths_to_end[n]:
        #         print(f'    - {p}')
        
        self.clear_cache()

    @stack_logger.func
    def clear_cache(self):
        self._i_cache = dict()
        self._z_cache = dict()
        self._v_cache = dict()
    
    @stack_logger.func
    def load_impedance(self, item:Net|SupportsImpedance,  frequency:hertz=hertz(0), include_self:bool=True, raise_on_undefined=False) -> ohm:
        cache_key = (item, frequency, include_self)
        if cache_key in self._z_cache:
            return self._z_cache[(item, frequency)]
        
        seen_impedances = self.divided_impedances(item, frequency).values()
        if len(seen_impedances) == 0 and item is not self.zero_ref:
            if raise_on_undefined:
                raise UndefinedImpedance()
            else:
                return ohm(0)
        
        # perform a parallel sum
        z_load = ohm(harmonic_sum([
            v for v in seen_impedances
            if v is not None
        ]))
        
        if include_self and isinstance(item, SupportsImpedance):
            z_self = ac.magnitude(impedance(item, frequency))
            if z_self is not None:
                z_load = ohm(z_load + z_self)
        
        #self._z_cache[(item, frequency)] = z_load
        return add_noise(z_load, 0)
    
    @stack_logger.func
    def source_impedance(self, item:Net|SupportsImpedance,  frequency:hertz=hertz(0), include_self:bool=True, raise_on_undefined=False) -> ohm:
        
        seen_impedances = self.divided_impedances(item, frequency, reverse=True).values()
        if len(seen_impedances) == 0 and item is not self.src_ref:
            if raise_on_undefined:
                raise UndefinedImpedance()
            else:
                return ohm(0)
        
        # perform a parallel sum
        z_load = ohm(harmonic_sum([
            v for v in seen_impedances
            if v is not None
        ]))
        
        if include_self and isinstance(item, SupportsImpedance):
            z_self = ac.magnitude(impedance(item, frequency))
            if z_self is not None:
                z_load = ohm(z_load + z_self)
        
        return z_load
    
    @stack_logger.func
    def divided_impedances(self, item:Net|SupportsImpedance, frequency:hertz, *, reverse=False) -> dict[SupportsImpedance|Net, ohm]:
        impedances:dict[SupportsImpedance|Net, ohm] = dict()
        paths = self.paths_to_end[item]
        z_func = self.load_impedance
        if reverse:
            paths = self.paths_to_src[item]
            z_func = self.source_impedance
        for node in set( p[0] for p in paths ):
            try:
                impedances[node] = ohm(z_func(node, frequency, raise_on_undefined=True))
            except UndefinedImpedance:
                continue
        return impedances

    # def divided_currents(self, item:SupportsImpedance|Net, frequency:hertz) -> dict:
    #     impedances = self.divided_impedances(item, frequency)
    #     i_total = self.electric_current(item, frequency, raise_on_undefined=True)
    #     z_total = ohm(harmonic_sum([z for z in impedances.values() if z is not None]))
    #     return dict([
    #         (c, current_divider(i_total, z_branch, z_total))
    #         for c, z_branch in impedances.items()
    #         if z_branch is not None
    #     ])

    # def electric_current(self, item:Net|SupportsImpedance, frequency:hertz, raise_on_undefined=False) -> ampere:
    #     if cache_key in self._i_cache:
    #         return self._i_cache[(item, frequency)]
        
    #     if item is self.src_ref:
    #         return ampere(1)
        
    #     # get a list of all items adjacent to this item and is between it and the src
    #     prev_nets = set( p[0] for p in self.paths_to_src[item] )
    #     if len(prev_nets) == 0:
    #         if not raise_on_undefined:
    #             return ampere(0)
    #         raise UndefinedElectricCurrent()
        
    #     # Sum all of the currents from those adjacent items
    #     i_src = 0
    #     for n in prev_nets:
    #         try:
    #             currents = self.divided_currents(n, frequency)
    #         except UndefinedElectricCurrent:
    #             continue
    #         if item in currents:
    #             i_src += currents[item]
        
    #     self._i_cache[(item, frequency)] = ampere(i_src)
    #     return ampere(i_src)

    @stack_logger.func
    def volts_in(self, item:Net|SupportsImpedance, frequency:hertz) -> volt:
        if item is self.src_ref:
            return volt(1)
        predecessors = set([p[0] for p in self.paths_to_src[item]])
        return volt(sum(
            self.volts_out(p, frequency)
            for p in predecessors
        ))
    
    @stack_logger.func
    def volts_out(self, item:Net|SupportsImpedance, frequency:hertz) -> volt:
        if item is self.src_ref:
            return volt(1)
        
        volts_in = self.volts_in(item, frequency)
        if isinstance(item, Net):
            return volts_in
        
        z_self = impedance(item, frequency)
        z_load = self.load_impedance(item, frequency, include_self=False, raise_on_undefined=False) or ohm(0)
        return volt(voltage_divider(volts_in, z_self, ohm(z_load)))

    @stack_logger.func
    def volts_drop(self, item:Net|SupportsImpedance, frequency:hertz) -> volt:
        v_in = self.volts_in(item, frequency)
        v_out = self.volts_out(item, frequency)
        return volt(v_in - v_out)

    @stack_logger.func
    def power(self, item:Net|SupportsImpedance, frequency:hertz) -> watt:
        v = self.volts_in(item, frequency)
        z = self.load_impedance(item, frequency)
        if z == 0 or v == 0:
            return watt(1.0)
        return power.from_RV(z, v) 
        v = self.volts_in(item, frequency) 
        i = self. electric_currentcache_key    
        return watt(v * i)
