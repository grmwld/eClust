#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Point:
    def __init__(self, space, values=None):
        self.__space = space
        if values is None:
            self.__values = [0] * space.dimensions
        elif len(values) != space.dimensions:
            raise 'Point\'s number of dimensions does not match that of the supplied space'

    def __hash__(self):
        return hash(self.__values)

    def __getitem__(self, key):
        try:
            return self.__values[key]
        except TypeError:
            index = self.__space.label_to_index(key)
            try:
                return self.__values[index]
            except Exception as e:
                raise e
