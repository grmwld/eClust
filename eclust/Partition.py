#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
from itertools import groupby, permutations

import numpy as np
import scipy as sp

from . import Point
from . import Cluster


class Partition:
    def __init__(self, assignments=None, fitness='DB'):
        self.__assignments = assignments
        self.__clusters = []
        f = lambda x: x[1]
        for k, group in groupby(sorted(assignments, key=f), key=f):
            self.__clusters.append(Cluster([g[0] for g in group]))
        if fitness == 'DB':
            self.__fitness = self.__fitness_DB
        elif fitness == 'SM':
            self.__fitness = self.__fitness_SM
        elif fitness == 'CS':
            self.__fitness = self.__fitness_CS

    def __fitness_DB(self):
        N = len(self.__clusters)
        f = lambda x: x[0]
        #perms2 = list(permutations(self.__clusters, 2))
        #D = zip(
            #(p[0].id for p in perms2),
            #((c1.dispersion() + c2.dispersion()) / c1.distance_to(c2)
                #for c1, c2 in perms2)
        #)
        perms = permutations(self.__clusters, 2)
        D = zip(
            (p[0].id for p in perms),
            ((c1.dispersion() + c2.dispersion()) / c1.distance_to(c2)
                for c1, c2 in perms)
        )
        D = ([i[1] for i in g] for k, g in groupby(D, key=f))
        R = (max(Di, ) for Di in D)
        dbi = np.sum(R) / N
        return dbi

    def __fitness_SM(self):
        return 1

    def __fitness_CS(self):
        return 1

    @property
    def fitness(self):
        return self.__fitness()

    @property
    def assignments(self):
        return self.__assignments

    def crossover_with(self, other, model):
        p1 = []
        p2 = []
        c1 = []
        c2 = []
        start_pos = 0
        junction_positions = model()
        for pos in junction_positions:
            p1.append(self.__assignments[start_pos:pos])
            p2.append(other.assignments[start_pos:pos])
            start_pos = pos
        p1.append(self.__assignments[start_pos:])
        p2.append(other.__assignments[start_pos:])
        for i, s in enumerate(zip(p1, p2)):
            if i % 2 == 0:
                c1.extend(s[0])
                c2.extend(s[1])
            else:
                c1.extend(s[1])
                c2.extend(s[0])
        return (Partition(c1), Partition(c2))

    def fight_with(self, other, p):
        print(self.fitness)
        return self
        #if self.fitness < other.fitness:
            #pass
        #elif self.fitness > other.fitness:
            #pass
        #else:
            #return self
