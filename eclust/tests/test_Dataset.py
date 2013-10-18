#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cProfile
from unittest import TestCase

from .. import Space, Point, Dataset


class TestDataset(TestCase):

    test_file = './tests/test_data.tsv'

    @classmethod
    def setupClass(cls):
        cls._dataset = Dataset.from_file(cls.test_file, dtypes=[float]*4)

    def test_clustering(self):
        #cProfile.run('self._dataset.clusterize()')
        self._dataset.clusterize()
