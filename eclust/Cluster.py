#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
from functools import lru_cache

import numpy as np
import scipy as sp
from scipy.spatial import distance

from . import Point


class Cluster(list):
    def __init__(self, points=[]):
        super().__init__(points)
        self.__id = random.getrandbits(128)

    @property
    def id(self):
        return self.__id

    @property
    @lru_cache()
    def centroid(self):
        coords = np.mean(np.array([p.coords for p in self], dtype=float), axis=0)
        return list(coords)

    def __hash__(self):
        return hash(self.__id)

    def dispersion(self):
        d = distance.euclidean
        c = self.centroid
        return np.mean([d(p.coords, c) for p in self])

    def distance_to(self, other):
        d = distance.euclidean
        return d(self.centroid, other.centroid)

    def split(self):
        pass

    def merge(self, other):
        pass

    def transfer_to(self, other, n, p):
        '''Transfer n points or p*total_points to an other cluster'''
        pass
