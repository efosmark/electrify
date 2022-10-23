import numpy as np

from .stats import bound


def pbavg_fitness(passband_results):
    if len(passband_results) == 0:
        return 0
    pbavg = np.mean(passband_results)
    pbavg = bound(pbavg, -100, 0)
    pbavg = np.abs(pbavg)
    return (60 - pbavg) / 100.0


def sbavg_fitness(sbavg):
    sbavg = bound(sbavg, -100, 0)
    sbavg = np.abs(sbavg)
    return sbavg / 100.0


def circuit_fitness(circuit, target=15):
    nodes = circuit.number_of_nodes()
    return 1 - (np.abs(target - nodes) / float(target))


def pbrange_fitness(passband_results):
    if len(passband_results) == 0:
        return 0
    num_above = len([p for p in passband_results if p >= -3])
    return num_above / float(len(passband_results))


def sbrange_fitness(stopband_results):
    if len(stopband_results) == 0:
        return 0
    num_below = len([s for s in stopband_results if s < -3])
    return num_below / float(len(stopband_results))


def bandrange_fitness(passband_results, stopband_results):
    num_above = len([p for p in passband_results if p >= -3])
    num_below = len([s for s in stopband_results if s < -3])
    return (num_above + num_below) / float(len(passband_results) + len(stopband_results))
