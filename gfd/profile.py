from functools import cache
import electrify as e


class GFDProfile(object):

    def __init__(self):
        self.passbands = []
        self.stopbands = []
        self.domain_type = "geom"
        self.derivative_delta = 1
        self.weights = dict()
        self.sample_count = 100
        self.num_generations = 10000
        self.num_parents_mating = 2
        self.solutions_per_pop = 16
        self.__f_min = None
        self.__f_max = None

    @property
    @cache
    def f_min(self):
        if self.__f_min is not None:
            return self.__f_min
        f_min = None
        for a, b in [*self.passbands, *self.stopbands]:
            if f_min is None or a < f_min:
                f_min = a
            if b < f_min:
                f_min = b
        return f_min

    @f_min.setter
    def f_min(self, value):
        self.__f_min = value

    @property
    @cache
    def f_max(self):
        if self.__f_max is not None:
            return self.__f_max
        f_max = None
        for a, b in [*self.passbands, *self.stopbands]:
            if f_max is None or b > f_max:
                f_max = b
            if a > f_max:
                f_max = a
        return f_max

    @f_max.setter
    def f_max(self, value):
        self.__f_max = value

    @property
    @cache
    def domain(self):
        return e.plot.bode.get_domain(self.domain_type, self.f_min, self.f_max, self.sample_count)

    @property
    @cache
    def derivative_domain(self):
        return self.domain[::self.derivative_delta]

    @property
    @cache
    def passband_domain(self):
        pb_domain = set()
        for f in self.domain:
            added = False
            for pb in self.passbands:
                if pb[0] <= f < pb[1]:
                    pb_domain.add(f)
                    added = True
                    break
            if not added:
                for sb in self.stopbands:
                    if sb[0] <= f < sb[1]:
                        pb_domain.add(f)
                        break
        return pb_domain

    @classmethod
    def from_dict(cls, values: dict):
        x = cls()
        for k, v in values.items():
            setattr(x, k, v)
        return x
