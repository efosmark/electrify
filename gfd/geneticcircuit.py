from itertools import cycle, product
from collections import defaultdict
import numpy as np

from electrify.circuit.circuit import Circuit, Parallel, Series, Shunt
from electrify.component import Capacitor, Inductor, Resistor, Node, Gnd, VoltageSource, Load
from electrify.math import attenuation_factor_db, f0_from_bandwidth
import electrify as e

from .genespace import GeneSpace

NO_ELEMENT = 0
CAPACITOR = 1
CAP_DECOUPLE = 2
CAP_FILTER = 3
INDUCTOR = 4
IND_DECOUPLE = 5
IND_CHOKE = 6
TUNED_SERIES = 7
TUNED_PARALLEL = 8

SERIES = 0
SHUNT = 1


class GeneticCircuit(object):

    def __init__(self, freq_domain):
        self.rng = np.random.default_rng()
        self.count = 0
        self.freq_domain = freq_domain
        space = [
            ('VALUE', range(1, 1000)),
            ('TYPE',  [CAPACITOR, CAP_DECOUPLE, NO_ELEMENT, INDUCTOR, IND_DECOUPLE, IND_CHOKE]),
            #('FREQ',  list(freq_domain)),
            ('TOPO',  [SERIES, SHUNT])
        ]
        self._genespace = GeneSpace(5, space)

    def get_genespace(self):
        return self._genespace.fullspace

    def mutate_gene(self, gene, gene_type):
        value = None
        gene_value_options = self._genespace.space[gene_type]

        current_idx = -1
        if gene in gene_value_options:
            current_idx = gene_value_options.index(gene)

        if current_idx > -1:
            value = gene_value_options[current_idx]
        elif value is None:
            value = np.random.choice(gene_value_options)

        if self.rng.random() < 0.5:
            value = value - 1
        else:
            value = value + 1

        if value <= 0 or value >= len(gene_value_options):
            value = np.random.choice(gene_value_options)
        return value

    def mutate_value(self, value):
        offset = 250.0 * self.rng.random()
        if self.rng.random() < 0.5:
            value = value - offset
        else:
            value = value + offset
        if value < 0:
            value = abs(offset)
        elif value > 1000:
            value = 1000 - abs(offset)
        if value == 0:
            value = offset + 1
        return value

    def mutate_frequency(self, freq):
        offset_hz = ((max(self.freq_domain) * 0.25) * self.rng.random())
        if self.rng.random() < 0.5:
            value = freq - offset_hz
            if value < 0:
                value = min(self.freq_domain) + offset_hz
        else:
            value = freq + offset_hz
            if value >= max(self.freq_domain):
                value = max(self.freq_domain) - offset_hz
        return value

    def mutation_func(self, offspring, ga_instance):
        for chromosome_idx in range(offspring.shape[0]):
            chromosome = offspring[chromosome_idx]
            while self.rng.random() < 0.7:
                gene_idx = np.random.choice(range(len(chromosome)))
                gene_type_idx = gene_idx % len(self._genespace.keys)
                gene_type = self._genespace.keys[gene_type_idx]
                if gene_type == 'VALUE':
                    value = self.mutate_value(chromosome[gene_idx])
                elif gene_type == 'FREQ':
                    value = self.mutate_frequency(chromosome[gene_idx])
                else:
                    value = self.mutate_gene(chromosome[gene_idx], gene_type)
                offspring[chromosome_idx, gene_idx] = value
        return offspring

    def crossover_func(self, parents, offspring_size, ga_instance):
        offspring_size, num_genes = offspring_size
        offspring = []
        idx = 0
        while len(offspring) < offspring_size:
            parent1 = list(parents[idx % parents.shape[0], :].copy())
            parent2 = list(parents[(idx + 1) % parents.shape[0], :].copy())

            genes1 = self._genespace.all_genes(parent1)
            genes2 = self._genespace.all_genes(parent2)

            split_at = np.random.choice(range(len(genes1)))
            child = [
                *genes1[:split_at],
                *genes2[split_at:]
            ]
            offspring.append(self._genespace.chromosome(child))
            idx += 1
        return np.array(offspring)

    def create_element(self, gene):
        v = int(gene['VALUE'])
        t = int(gene['TYPE'])

        if t == NO_ELEMENT:
            return Node()

        elif t == CAPACITOR:
            return Capacitor(pF=v, ESR=1.0)

        elif t == CAP_DECOUPLE:
            return Capacitor(nF=v, name="Decouple", ESR=1.0)

        elif t == CAP_FILTER:
            return Capacitor(uF=v, name="FilterCap", ESR=2.0)

        elif t == INDUCTOR:
            return Inductor(nH=v, ESR=0.5)

        elif t == IND_DECOUPLE:
            return Inductor(uH=v/100.0, ESR=0.5, name="Decouple")

        elif t == IND_CHOKE:
            return Inductor(uH=v, name="RFC", ESR=0.5)

        elif t == TUNED_SERIES:
            f = int(gene['FREQ'])
            ind = Inductor(uH=v, ESR=1.5)
            cap = Capacitor.from_reactance(f, ind.reactance(f), ESR=2.0)
            return Series(ind, cap)

        elif t == TUNED_PARALLEL:
            f = int(gene['FREQ'])
            ind = Inductor(uH=v, ESR=1.5)
            cap = Capacitor.from_reactance(f, ind.reactance(f), ESR=2.0)
            return Parallel(ind, cap)

        return Node()

    def create_circuit(self, chromosome):
        self.count += 1
        c = Circuit()
        c + VoltageSource(voltage=100.0, ESR=50.0)
        for i, gene in enumerate(self._genespace.genes(chromosome)):
            e = self.create_element(gene)

            if gene['TOPO'] == SHUNT:
                c.add(Shunt(e))
            else:
                c.add(e)

        c + Load(50.0)
        c + c.GND
        c.reduce(max_iteration=15)
        return c
