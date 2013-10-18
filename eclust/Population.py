#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
from itertools import zip_longest
from operator import methodcaller
from multiprocessing import Pool
from functools import partial

from . import utils



def set_fitness_method(p, m):
    p.set_fitness_method(m)
    return p

def _getattr_proxy_partialable(instance, name, arg): 
    return getattr(instance, name)(arg) 

def getattr_proxy(instance, name): 
    return partial(_getattr_proxy_partialable, instance, name)


class Population(list):
    def __init__(self, partitions=[]):
        super().__init__(partitions)

    def __update(self, l):
        del self[:]
        self.extend(l)

    def __shuffle(self):
        random.seed(42)
        random.shuffle(self)
        
    def __make_pairs(self):
        args = [iter(self)] * 2
        for p1, p2 in zip_longest(*[iter(self)]*2):
            yield (p1, p2)

    def set_fitness_method(self, method):
        f = methodcaller('set_fitness_method', method=method)

        #Parallel(n_jobs=2)(delayed(f)(p) for p in self)
        #Parallel(n_jobs=2)(delayed(set_fitness_method)(p, method) for p in self)
        #Parallel(n_jobs=2)(delayed(lambda x, m: x.set_fitness_method(m))(p, method) for p in self)
        pool = Pool(1)
        a = list(pool.map(f, (p for p in self)))
        #for i, p in enumerate(self):
            #pool.apply(getattr_proxy(p, 'set_fitness_method'), (method,))
            #pool.apply(p.set_fitness_method, (method,))
            #pool.apply(f, (p,))
            #f(p)
            #p.set_fitness_method(method)
        pool.close()
        pool.join()
        print(self[0].fitness)

    def crossover(self, model):
        self.__shuffle()
        offsprings = []
        for p1, p2 in self.__make_pairs():
            offsprings.extend(p1.crossover_with(p2, model))
        self.extend(offsprings)

    def select(self, p):
        self.__shuffle()
        winners = []
        for p1, p2 in self.__make_pairs():
            winners.append(p1.fight_with(p2, p))
        self.__update(winners)

    def mutate(self, model):
        for partition in self:
            partition.mutate(model)

