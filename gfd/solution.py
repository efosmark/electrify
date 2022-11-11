from gfd.profile import GFDProfile
from functools import cache
import numpy as np


def sigmoid(x):
    ''' Apply sigmoid function to x, where 0 < x < 1
        Returns a value between 0 & 1 that falls on the sigmoid curve.
    '''
    return 1 / (1 + np.exp(-(x-0.5)*10))


def phase_linearity(phase):
    dx = []
    for p1, p2 in zip(phase, phase[1:]):
        dist1 = p1 - p2
        if (p1 > 0 and p2 < 0) or (p1 < 0 and p2 > 0):
            dist = min(abs(p1-p2), abs(90-abs(p1))+abs(90-abs(p2)))
        else:
            dist = abs(p1-p2)
        dx.append(dist)
    return dx


class GFDSolution(object):

    def __init__(self, profile: GFDProfile):
        self.profile = profile
        self.chromosome = tuple()
        self.circuit_id = -1
        self.generation_id = -1
        self.best_fitness = 0.0
        self.sim_time = 0.0
        self.num_elements = -1
        self.new_best = False
        self.y_gain = []
        self.y_phase = []
        self.y_magnitude = []
        self.y_phase_rad = []
        self.gain_derivative = []
        self.phase_derivative = []

    @property
    @cache
    def ft_gain(self) -> float:
        fitness = []
        for g, f in zip(self.y_gain, self.profile.domain):
            if f in self.profile.passband_domain:
                fitness.append(63.0 - abs(g))
                if g >= -3:
                    fitness.append((3-abs(g)) * 100.0)
            else:
                if g < -63.0:
                    g = -63.00
                fitness.append(abs(g))
                if g >= -3:
                    fitness.append(0 - ((3 - abs(g)) * 100.0))

        return sum(fitness) * self.profile.weights['gain']

    @property
    @cache
    def ft_phase(self) -> float:
        pb_phase = []
        for ph, f in zip(self.y_phase, self.profile.domain):
            if f in self.profile.passband_domain or True:
                pb_phase.append(abs(ph))

        rotational_dv = phase_linearity(pb_phase)
        return -1e5 * (max(rotational_dv) - min(rotational_dv)) * self.profile.weights['phase']

    @property
    @cache
    def ft_gain_derivative(self) -> float:
        return 0.0

    @property
    @cache
    def ft_phase_derivative(self) -> float:
        return 0.0

    @property
    @cache
    def fitness(self) -> float:
        if self.new_best:
            print("\n\n\n")
            print('Gf={:3.3f} Pf={:3.3f}'.format(self.ft_gain, self.ft_phase))
            print("\n\n\n")
        return self.ft_gain + self.ft_phase  # + self.ft_gain_derivative + self.ft_phase_derivative
