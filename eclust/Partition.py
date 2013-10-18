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
from . import utils



class Partition:
    def __init__(self, assignments=None, fitness_method=None):
        self.__assignments = assignments
        if fitness_method:
            self.set_fitness_method(fitness_method)

    def __init_clusters(self, disp_method=None):
        self.__kcluster = utils.BijectiveDict()
        self.__clusters = {}
        self.__points = {}
        f = lambda x: x[1]
        for k, group in groupby(sorted(self.__assignments, key=f), key=f):
            self.__init_cluster(k, group, disp_method)

    def __init_cluster(self, k, group, disp_method):
        points = [g[0] for g in group]
        c = Cluster(points)
        c.update_centroid()
        if disp_method:
            c.update_dispersion(disp_method)
        self.__kcluster[k] = c.id
        self.__clusters[c.id] = c
        for p in points:
            self.__points[p] = c.id

    def __set_disp_method(self, method):
        if method == 'DC':
            self.__disp_method = 'DC'
        if method == 'MD':
            self.__disp_method = 'MD'
        self.__init_clusters(method)

    @property
    def assignments(self):
        return self.__assignments

    @property
    def fitness(self):
        return self.__fitness()

    def set_fitness_method(self, method):
        print(self)
        if method == 'DSP':
            self.__set_disp_method('DC')
            self.__fitness_method = 'DSP'
            self.__fitness = self.__fitness_DSP
        if method == 'COID':
            self.__init_clusters()
            self.__fitness_method = 'COID'
            self.__fitness = self.__fitness_COID
        if method == 'DB':
            self.__set_disp_method('DC')
            self.__fitness_method = 'DB'
            self.__fitness = self.__fitness_DB
        if method == 'CS':
            self.__set_disp_method('MD')
            self.__fitness_method = 'CS'
            self.__fitness = self.__fitness_CS
        return self

    @lru_cache(maxsize=1024)
    def __fitness_DSP(self):
        return np.mean([[c.dispersion] for c in self.__clusters.values()])

    @lru_cache(maxsize=1024)
    def __fitness_COID(self):
        centroids = [c.centroid for c in self.__clusters.values()]
        dc = squareform(pdist(centroids))
        f = lambda x: x==0
        Mij = np.array([list(filterfalse(f, i)) for i in dc])
        return Mij.min(axis=1).mean()

    @lru_cache(maxsize=1024)
    def __fitness_DB(self):
        N = len(self.__clusters)
        # Distance matrix of clusters centroids
        centroids = [c.centroid for c in self.__clusters.values()]
        dc = squareform(pdist(centroids))
        f = lambda x: x==0
        Mij = np.array([list(filterfalse(f, i)) for i in dc])
        # Matrix of pairs of cluster dispersions
        dispersions = [[c.dispersion] for c in self.__clusters.values()]
        f = lambda u, v: u+v
        cc = squareform(pdist(dispersions, f))
        f = lambda x: x==0
        Sij = np.array([list(filterfalse(f, i)) for i in cc])
        # Finalise
        Rij = Sij / Mij
        R = [max(Ri, ) for Ri in Rij]
        dbi = np.sum(R) / N
        return dbi

    @lru_cache(maxsize=1024)
    def __fitness_CS(self):
        N = len(self.__clusters)
        # Distance matrix of clusters centroids
        centroids = [c.centroid for c in self.__clusters.values()]
        dc = squareform(pdist(centroids))
        f = lambda x: x==0
        Mij = np.array([list(filterfalse(f, i)) for i in dc])
        # Dispersion
        dispersions = [c.dispersion for c in self.__clusters.values()]
        S = np.mean(dispersions)
        csi = S / np.min(Mij, axis=1).mean()
        return csi

    def fight_with(self, other, p, reverse=False):
        podium = sorted([self, other], reverse=reverse)
        if random.random() < p:
            return podium[0]
        return podium[1]

    def mutate(self, model):
        positions = model()
        for pos in positions:
            point, old_k = self.__assignments[pos]
            old_id = self.__kcluster[old_k]
            new_k = random.randint(0, len(self.__clusters)-1)
            new_id = self.__kcluster[new_k]
            self.__assignments[pos][1] = new_k
            self.__clusters[old_id].remove(point)
            self.__clusters[new_id].append(point)
            
            #print('c', self.__clusters[new_id].centroid.cache_info())
            #print('d', self.__clusters[new_id].dispersion.cache_info())
            #print('fDB', self.__fitness_DB.cache_info())
            #print('fCS', self.__fitness_CS.cache_info())

            self.__clusters[new_id].update_centroid()
            self.__clusters[new_id].update_dispersion(self.__fitness_dispersion)
            #self.__clusters[new_id].centroid.cache_clear()
            #self.__clusters[new_id].dispersion.cache_clear()
            self.__fitness.cache_clear()

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
        return (Partition(c1, self.__fitness_method),
                Partition(c2, self.__fitness_method))

    def __gt__(self, other):
        return self.fitness > other.fitness
    def __lt__(self, other):
        return self.fitness < other.fitness
    def __ge__(self, other):
        return self.fitness >= other.fitness
    def __le__(self, other):
        return self.fitness <= other.fitness

