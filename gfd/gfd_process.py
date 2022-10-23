from multiprocessing import Process, Queue
from PySide6.QtCore import Signal, QThread
from pygad import pygad
import numpy as np
import time
from multiprocessing import Process

import electrify as e
from gfd.geneticcircuit import GeneticCircuit

from gfd.profile import GFDProfile
from gfd.solution import GFDSolution


def voltage_gain(f, c):
    sln = c.solve(f=f, source=c.source_node, load=c.load_node)
    V_in = e.math.voltage_divider(
        sln[c.source_node]['voltage'],    # V_source
        sln[c.source_node]['res_self'],   # R_source
        sln[c.load_node]['res_self']      # R_load
    )
    V_load = sln[c.load_node]['voltage']  # V_load
    if V_load == 0:
        return 0
    return V_load / V_in


def to_db(value):
    if value == 0:
        return 0
    return (20 * np.log10(value)).real


def numeric_derivative(x, y, delta):
    dv_y_gain = list(np.diff(y[::delta])/np.diff(x))
    dv_y_gain.append(dv_y_gain[-1])
    return dv_y_gain


def full_phase(g):
    return np.arctan(g.imag/g.real) if g.real != 0 else 0


class GeneticProcessor(Process):

    def __init__(self, queue: Queue, profile: GFDProfile):
        super(GeneticProcessor, self).__init__(name="Genetic Designer")
        self.queue = queue
        self.profile = profile
        self._geneticcircuit = GeneticCircuit(freq_domain=self.profile.domain)

        self._best_fitness_level = None
        self._should_stop = False
        self._sln_cache = dict()
        self._best_solutions = set()

    def data_ready(self, solution: GFDSolution):
        self._sln_cache[solution.chromosome] = solution
        self.queue.put(solution)
        if self.queue.qsize() > 10:
            print("Queue has grown too much. Closing the process.", flush=True)
            raise SystemExit()

    def set_up_gfd(self):
        def fitness_fn(sln, sln_idx):
            s = GFDSolution(self.profile)
            s.chromosome = tuple(sln)
            s.generation_id = self.ga_instance.generations_completed
            s.circuit_id = self._geneticcircuit.count
            s.best_fitness = self._best_fitness_level

            start = time.time()
            c = self._geneticcircuit.create_circuit(sln)
            for f in self.profile.domain:
                g = voltage_gain(f, c)
                s.y_gain.append(to_db(g))
                s.y_magnitude.append(e.math.rf.magnitude(g))
                s.y_phase.append(np.rad2deg(full_phase(g)))
                s.y_phase_rad.append(full_phase(g))
            # s.gain_derivative = numeric_derivative(
            #     self.profile.derivative_domain,
            #     s.y_gain,
            #     self.profile.derivative_delta
            # )
            # s.phase_derivative = numeric_derivative(
            #     self.profile.derivative_domain,
            #     s.y_gain,
            #     self.profile.derivative_delta
            # )
            s.num_elements = c.number_of_nodes()
            s.sim_time = time.time() - start

            self.data_ready(s)
            return s.fitness

        def on_generation(ga_instance):
            return self.on_generation(ga_instance)

        def mutation_func(offspring, ga_instance):
            return self._geneticcircuit.mutation_func(offspring, ga_instance)

        def crossover_func(parents, offspring_size, ga_instance):
            return self._geneticcircuit.crossover_func(parents, offspring_size, ga_instance)

        self.ga_instance = pygad.GA(
            gene_type=int,
            num_generations=self.profile.num_generations,
            num_parents_mating=self.profile.num_parents_mating,
            sol_per_pop=self.profile.solutions_per_pop,
            num_genes=len(self._geneticcircuit.get_genespace()),
            fitness_func=fitness_fn,
            on_generation=on_generation,
            gene_space=self._geneticcircuit.get_genespace(),
            mutation_type=mutation_func,
            crossover_type=crossover_func,
            # keep_parents=2,
            stop_criteria=["saturate_500"],
        )

    def on_generation(self, ga_instance):
        chromosome, fitness_level, _ = ga_instance.best_solution()
        new_best = False
        if self._best_fitness_level is None or fitness_level > self._best_fitness_level:
            self._best_fitness_level = fitness_level
            new_best = True

        chromosome_id = tuple(chromosome)
        if chromosome_id in self._best_solutions:
            return

        solution = self._sln_cache[tuple(chromosome)]
        solution.new_best = new_best
        solution.best_fitness = fitness_level
        solution.generation_id = ga_instance.generations_completed
        self._best_solutions.add(chromosome_id)
        self.data_ready(solution)

    def run(self):
        self.set_up_gfd()
        self.ga_instance.run()


class GFDThread(QThread):
    solutionReady = Signal(object)
    fitnessComplete = Signal(object)

    def __init__(self, profile: GFDProfile):
        QThread.__init__(self)
        self.wait_on_queue = True
        self.queue = Queue()
        self.profile = profile
        self.proc = GeneticProcessor(
            self.queue,
            profile
        )

    def run(self):
        self.proc.start()
        while self.wait_on_queue:
            while not self.queue.empty():
                item = self.queue.get()
                self.solutionReady.emit(item)
            time.sleep(0.1)
        self.proc.kill()
        self.wait_on_queue = True

    def stop(self):
        self.wait_on_queue = False
