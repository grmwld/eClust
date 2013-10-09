#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class Space:
    def __init__(self, num_dimensions, dimensions_labels=None):
        self.__dimensions = num_dimensions
        self.__labels = dimensions_labels
        if self.__labels is None:
            self.__labels = [str(i) for i in range(self.__dimensions)]
        self.__labels_dict = dict(zip(self.__labels, range(self.__dimensions)))

    @property
    def dimensions(self):
        return self.__dimensions

    @property
    def labels(self):
        return self.__labels

    def __getitem__(self, key):
        try:
            return self.__labels[key]
        except TypeError:
            return self.__labels_dict[key]

