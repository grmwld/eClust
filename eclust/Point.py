#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Point:
    def __init__(self, space, coords=None):
        self.__space = space
        if coords is None:
            self.__coords = [0] * space.dimensions
        elif len(coords) != space.dimensions:
            raise 'Point\'s number of dimensions does not match that of the supplied space'
        else:
            self.__coords = coords

    @property
    def labels(self):
        return self.__space.labels

    @property
    def coords(self):
        return self.__coords

    def __hash__(self):
        return hash(self.__coords)

    def __getitem__(self, key):
        try:
            return self.__coords[key]
        except TypeError:
            return self.__coords[self.__space[key]]
