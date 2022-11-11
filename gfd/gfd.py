from pygad import pygad
import networkx as nx
import numpy as np
import time

import electrify as e

from .stats import sigmoid
from .fitness import circuit_fitness
from .geneticcircuit import GeneticCircuit


def find_frequencies_of_interest(passbands, stopbands):
    if len(passbands) > 0:
        bands = passbands
    elif len(stopbands) > 0:
        bands = stopbands
    else:
        raise ValueError("Cannot find resonant frequencies. Neither passbands nor stopbands were supplied.")
    edge_freqs = set()
    for a, b in bands:
        edge_freqs.add(a)
        edge_freqs.add(b)
    edge_freqs = [1, *sorted(edge_freqs)]

    resonant_freqs = list()
    for a, b in zip(edge_freqs, edge_freqs[1:]):
        if b != 0:
            resonant_freqs.append(e.math.rf.f0_from_bandwidth(a, b))
    return edge_freqs, resonant_freqs[1:]


def apply_fitness_weights(fscore, weights):
    if weights is None:
        return fscore
    fitness = {}
    for k, v in fscore.items():
        if k in weights:
            fitness[k] = sigmoid(v * float(weights[k]))
    return fitness


def get_relevant_gain_values(gfd, candidate, raw_result):
    gains = {
        e.pico(1): candidate.gain(e.pico(1)),
        e.tera(1): candidate.gain(e.tera(1)),
    }

    for f in gfd._resonant_frequencies:
        gains[f] = candidate.gain(f)

    m = max(raw_result)
    m_f = np.flatnonzero(raw_result == m)
    gains[gfd._domain[m_f[0]]] = m
    return gains


def get_circuit_information(gfd, sln, optimize=True):
    info = {}
    info["starttime"] = time.time()
    candidate = gfd._geneticcircuit.create_circuit(sln, optimize)

    try:
        pathlen = nx.shortest_path_length(candidate, source=candidate.source, target=candidate.last)
    except nx.NetworkXNoPath:
        info["starttime"] = 0
        info["endtime"] = 0
        info["simtime"] = 0
        info["nodes"] = candidate.number_of_nodes()
        return info

    raw_result = gfd.get_solution_results(candidate)
    info["endtime"] = time.time()
    info["simtime"] = info["endtime"] - info["starttime"]
    info["nodes"] = candidate.number_of_nodes()

    gains = get_relevant_gain_values(gfd, candidate, raw_result)
    info["baseline"] = max(gains.values())
    info["gains"] = gains

    candidate_result = [v - info['baseline'] for v in raw_result]

    sbavg_list, pbavg_list = [], []
    passband_results = []
    stopband_results = []
    pb_in_range = 0
    sb_in_range = 0

    if gfd.passbands is not None:
        for (pb_start, pb_stop) in gfd.passbands:
            band_pass, band_reject = [], []

            for i, c_val in enumerate(candidate_result):
                if pb_start <= gfd._domain[i] <= pb_stop:
                    band_pass.append(c_val)
                    if c_val >= -3:
                        pb_in_range += 1
                else:
                    band_reject.append(c_val)
                    if c_val < -3:
                        sb_in_range += 1

            if len(band_pass) > 0:
                pbavg_list.append(np.mean(band_pass))
                passband_results.extend(band_pass)

            if len(band_reject) > 0:
                sbavg_list.append(np.mean(band_reject))
                stopband_results.extend(band_reject)

    info["pbrange"] = pb_in_range / float(len(passband_results))
    info["sbrange"] = sb_in_range / float(len(stopband_results))

    info["inv_range_diff"] = 1 - abs(abs(info["sbrange"]) - abs(info["pbrange"]))

    info["pbavg"] = 1 - (abs(np.mean(pbavg_list)) / 100.0)
    if info["pbavg"] > 1:
        info["pbavg"] = 1.0
    elif info["pbavg"] < 0:
        info["pbavg"] = 0.0

    info["sbavg"] = abs(np.mean(sbavg_list)) / 100.0
    if info["sbavg"] > 1:
        info["sbavg"] = 1.0
    elif info["sbavg"] < 0:
        info["sbavg"] = 0.0

    info["circuit"] = circuit_fitness(candidate)
    return info


class GFDException(Exception):
    def __init__(self, circuit=None, sln=None, candidate_result=None, err=None):
        super().__init__()
        self.circuit = circuit
        self.sln = sln
        self.candidate_result = candidate_result
        self.err = err


class GeneticFilterDesigner(object):

    def __init__(
            self, n=100, max_num_stages=10, max_elements_per_stage=5, num_parents_mating=10, solutions_per_pop=5,
            passbands=None, stopbands=None, weights=None, sample_count=None, min_f=None, max_f=None, domain_type=None):
        self.stopbands = stopbands
        self.passbands = passbands
        self.weights = weights
        self.min_f = min_f
        self.max_f = max_f
        self.sample_count = sample_count

        edge_freqs, resonant_freqs = find_frequencies_of_interest(passbands, stopbands)
        self._resonant_frequencies = sorted([*resonant_freqs, *edge_freqs])[1:]

        rmin_f = min(self._resonant_frequencies[1:])
        rmax_f = max(self._resonant_frequencies)
        buffer = (rmax_f - rmin_f) * 0.1

        if self.min_f is None:
            if buffer > rmin_f:
                self.min_f = rmin_f / 2
            else:
                self.min_f = int(max(rmin_f - buffer, 1))
        if self.max_f is None:
            self.max_f = int(rmax_f + buffer)
        if self.sample_count is None:
            self.sample_count = int((self.max_f - self.min_f) / 5e5)

        if domain_type == "geom":
            self._domain = list(np.geomspace(self.min_f, self.max_f, self.sample_count))

        elif domain_type == "linear":
            self._domain = list(np.linspace(self.min_f, self.max_f, self.sample_count))

        else:
            raise ValueError("Unknown domain_type. Must be 'geom' or 'linear'.")

        self._geneticcircuit = GeneticCircuit(
            max_num_stages,
            max_elements_per_stage,
            num_parents_mating,
            resonant_frequencies=self._resonant_frequencies,
            freq_domain=self._domain
        )

        self._num_generations = n
        self._num_parents_mating = num_parents_mating
        self._solutions_per_pop = solutions_per_pop
        self._best_fitness_level = None

        def fitness_fn(sln, sln_idx):
            try:
                sln_info = get_circuit_information(self, sln)
            except (ZeroDivisionError, RecursionError) as err:
                raise GFDException(
                    sln=sln,
                    circuit=self._geneticcircuit.create_circuit(sln),
                    err=err
                )
            fitness = apply_fitness_weights(sln_info, self.weights)
            return sum(fitness.values())

        def on_generation(ga_instance):
            return self.on_generation(ga_instance)

        def mutation_func(offspring, ga_instance):
            return self._geneticcircuit.mutation_func(offspring, ga_instance)

        def crossover_func(parents, offspring_size, ga_instance):
            return self._geneticcircuit.crossover_func(parents, offspring_size, ga_instance)

        self.ga_instance = pygad.GA(
            gene_type=float,
            num_generations=self._num_generations,
            num_parents_mating=self._num_parents_mating,
            sol_per_pop=self._solutions_per_pop,
            num_genes=len(self._geneticcircuit.get_genespace()),
            # mutation_type=mutation_func,
            # crossover_type=crossover_func,
            fitness_func=fitness_fn,
            on_generation=on_generation,
            gene_space=self._geneticcircuit.get_genespace(),
            stop_criteria=["saturate_200"],
            # keep_parents=2,
        )

    def get_solution_results(self, candidate):
        candidate_result = []
        for f in self._domain:
            att_factor = e.math.rf.attenuation_factor_db(candidate.gain(f))
            candidate_result.append(att_factor)
        return candidate_result

    def on_generation(self, ga_instance):
        sln, fitness_level, sln_idx = ga_instance.best_solution()
        new_best = False
        if self._best_fitness_level is None or fitness_level > self._best_fitness_level:
            self._best_fitness_level = fitness_level
            new_best = True
        if not new_best:
            print(".", end="")
        else:
            sln_info = get_circuit_information(self, sln)

            stats = [
                "G# {: <3}".format(ga_instance.generations_completed),
                "best {:5.4f}".format(fitness_level),
                "pb {:6.2f}".format(sln_info['pbavg']),
                "pbr^ {:6.2f}%".format(sln_info.get('pbrange', 0) * 100),
                "sb {:6.2f}".format(sln_info['sbavg']),
                "sbr^ {:6.2f}%".format(sln_info['sbrange'] * 100),
                "RD {:6.2f}%".format(sln_info['inv_range_diff'] * 100),
                "{: >8}s".format(e.format_value(sln_info['simtime'])),
                "{:2.0f} nodes".format(sln_info['nodes']),
                "{:5.2f} dB".format(sln_info['baseline']),
            ]

            print("\n{} |".format(" | ".join(stats)), end="")

    def run(self):
        self.ga_instance.run()
