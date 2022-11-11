import numpy as np


class StatTracker(object):
    def __init__(self):
        self._values = []
        self.reset()

    def average(self):
        if len(self._values) == 0:
            return 0
        return np.mean(self._values)

    def maximum(self):
        if len(self._values) == 0:
            return 0
        return np.max(self._values)

    def minimum(self):
        if len(self._values) == 0:
            return 0
        return np.min(self._values)

    def values(self):
        return self._values

    def add(self, x):
        return self._values.append(x)

    def reset(self):
        del self._values
        self._values = []

    def __add__(self, x):
        return self.add(x)

    def __iadd__(self, x):
        return self.add(x)

    def __str__(self):
        return "<avg:{} count:{}>".format(fmt(self.avg()), fmt(len(self._values)))

    def __repr__(self):
        return self.__str__()


def convert_scale(x, initial=(0, 100), target=(0, 100)):
    ''' Given value `x` that falls within the range specified in `initial=(min, max)`,
        convert the value to instead fall within the target range `target=(min, max)`.

        Examples:

        > convert_scale(89, (10, 90), (100, 200))
        198.75
        > convert_scale(-56, (-100, 0), (0, 100))
        56.0
        > convert_scale(-2, (-3, 0), (0, 100))
        66.66
    '''
    if not initial[0] <= x <= initial[1]:
        raise ValueError('Value x={:.2f} is not within the initial scale={}'.format(x, initial))
    init_range = initial[1] - initial[0]
    init_ratio = (x - initial[0]) / init_range
    target_range = target[1] - target[0]
    return target[0] + (target_range * init_ratio)


def bound(x, lower, upper, inclusive=True):
    if x < lower:
        x = lower
    if x >= upper and inclusive:
        x = upper
    elif x > upper:
        x = upper
    return x


def sigmoid(x):
    ''' Apply sigmoid function to x, where 0 < x < 1
        Returns a value between 0 & 1 that falls on the sigmoid curve.
    '''
    return 1 / (1 + np.exp(-(x-0.5)*10))


def exp_scale(x, scale, limit=None):
    x = apply_scale(x, scale, limit)
    max_y = 100
    max_x = scale[1]
    return max_y**(x/max_x)


def exp_converge(x, target):
    r = 4
    if x == target:
        # Prevent asymptote issues
        x += 0.1
    return abs(((10**r) - x)/(x - target)) - target
