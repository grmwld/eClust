#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import numpy as np
import scipy as sp


class Point:
    def __init__(self, space, coords=None):
        self.__space = space
        self.__id = random.getrandbits(64)
        if coords is None:
            self.__coords = [0] * space.dimensions
        elif len(coords) != space.dimensions:
            raise ValueError('Point\'s number of dimensions does not match that of the supplied space')
        else:
            self.__coords = coords

    @property
    def labels(self):
        return self.__space.labels

    @property
    def coords(self):
        return self.__coords

    def __hash__(self):
        return hash((self.__id, tuple(self.__coords)))

    def __getitem__(self, key):
        try:
            return self.__coords[key]
        except TypeError:
            return self.__coords[self.__space[key]]

    def __gt__(self, other):
        return self.__coords > other.coords
    def __lt__(self, other):
        return self.__coords < other.coords
    def __ge__(self, other):
        return self.__coords >= other.coords
    def __le__(self, other):
        return self.__coords <= other.coords

