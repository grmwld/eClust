#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
from functools import lru_cache

import numpy as np
import scipy as sp
from scipy.spatial.distance import cdist, pdist, squareform, euclidean

from . import Point
from . import utils


class Cluster(list):
    def __init__(self, points=[]):
        super().__init__(points)
        self.__id = random.getrandbits(128)

    def __hash__(self):
        return hash(self.__id)

    @property
    def id(self):
        return self.__id

    @property
    @lru_cache()
    def centroid(self):
        coords = np.mean(np.array([p.coords for p in self]), axis=0)
        return coords

    @lru_cache()
    def dispersion(self, method='DB'):
        if method not in ['DB', 'CS']:
            raise AttributeError('Unknown dispersion method')
        if method == 'DB':
            c = self.centroid
            return cdist([c], [p.coords for p in self]).mean()
        if method == 'CS':
            #f = lambda u, v: utils.cached_distance(tuple(u), tuple(v), euclidean)
            #dist_matrix = squareform(pdist([p.coords for p in self], f))
            dist_matrix = squareform(pdist([p.coords for p in self]))
            return dist_matrix.max(axis=1).mean()

    def distance_to(self, other):
        d = euclidean
        return d(self.centroid, other.centroid)

    def split(self):
        pass

    def merge(self, other):
        pass

    def transfer_to(self, other, n, p):
        '''Transfer n points or p*total_points to an other cluster'''
        pass
