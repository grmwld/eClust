#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
from itertools import zip_longest


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

