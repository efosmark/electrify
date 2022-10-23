from itertools import cycle


class GeneSpace(object):

    def __init__(self, size, space):
        self.size = size
        self.space = dict(space)
        self.keys = [s[0] for s in space]
        self.fullspace = [s[1] for s in space] * size

    def all_genes(self, chromosome):
        return list(self.genes(chromosome))

    def genes(self, chromosome):
        n = len(self.keys)
        for i in range(0, len(chromosome), n):
            yield dict((k, v) for k, v in zip(cycle(self.keys), chromosome[i:(i + n)]))

    def chromosome(self, genes):
        c = []
        for g in genes:
            c.extend([g[k] for k in self.keys])
        return c
