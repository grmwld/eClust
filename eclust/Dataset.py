#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import numpy as np
import scipy as sp

from . import utils
from . import Space
from . import Point
from . import Population
from . import Partition


class Dataset(list):
    def __init__(self, points):
        super().__init__(points)
        self.sort()
        self.__assignments = None
        self.__population = None

    @classmethod
    def from_file(cls, filename, header=True, dtypes=None):
        with open(filename) as f:
            data = utils.read_datafile(f, header, dtypes)
        headers = data['headers']
        rows = data['rows']
        space = Space(len(headers), headers)
        return Dataset((Point(space, row) for row in rows))

    @property
    def assignments(self):
        return self.__assignments

    @property
    def population():
        return self.__population

    def append(self, point):
        super().append(point)
        self.sort()

    def __init_clusters(self, n, k, method):
        if method == 'random':
            np.random.seed(42)
            self.__assignments = np.random.random_integers(0, k, (n, len(self)))
        else:
            raise ValueError('Unknown cluster initialisation method')

    def __assignments_to_partitions(self):
        self.__population = Population()
        for assignment in self.__assignments:
            self.__population.append(Partition(list(zip(self, assignment))))

    def clusterize(self):
        p = {
            'n': 50,
            'ik': 3,
            'ik_method': 'random',
            'co_model': lambda: np.where(np.random.binomial(1, 1.0/len(self), len(self)))[0],
            'p_win': 0.8
        }
        self.__init_clusters(p['n'], p['ik'], p['ik_method'])
        self.__assignments_to_partitions()
        print(len(self.__population))
        self.__population.crossover(p['co_model'])
        print(len(self.__population))
        self.__population.select(p['p_win'])
        print(len(self.__population))
        
