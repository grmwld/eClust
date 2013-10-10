#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
from itertools import groupby, permutations, filterfalse
from functools import lru_cache

import numpy as np
import scipy as sp
from scipy.spatial.distance import pdist, squareform

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
        elif fitness == 'CS':
            self.__fitness = self.__fitness_CS

    def __gt__(self, other):
        return self.fitness > other.fitness
    def __lt__(self, other):
        return self.fitness < other.fitness
    def __ge__(self, other):
        return self.fitness >= other.fitness
    def __le__(self, other):
        return self.fitness <= other.fitness

    @lru_cache(maxsize=1024)
    def __fitness_DB(self):
        N = len(self.__clusters)
        # Distance matrix of clusters centroids
        centroids = [c.centroid for c in self.__clusters]
        dc = squareform(pdist(centroids))
        f = lambda x: x==0
        Mij = np.array([list(filterfalse(f, i)) for i in dc])
        # Matrix of pairs of cluster dispersions
        dispersions = [[c.dispersion] for c in self.__clusters]
        f = lambda u, v: u+v
        cc = squareform(pdist(dispersions, f))
        f = lambda x: x==0
        Sij = np.array([list(filterfalse(f, i)) for i in cc])
        # Finalise
        Rij = Sij / Mij
        R = [max(Ri, ) for Ri in Rij]
        dbi = np.sum(R) / N
        return dbi

    def __fitness_CS(self):
        N = len(self.__clusters)

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

    def fight_with(self, other, p, reverse=False):
        podium = sorted([self, other], reverse=reverse)
        if random.random() < p:
            return podium[0]
        return podium[1]

