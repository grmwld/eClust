#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from unittest import TestCase
import numpy as np

from .. import Space, Point, Cluster

class TestCluster(TestCase):

    space = {
        'dimensions': 2,
        'labels': ['D1', 'D2']
    }
    p1 = {
        'num_points': 50,
        'center': 3,
        'disp': 1
    }
    p2 = {
        'num_points': 50,
        'center': 4,
        'disp': 1
    }
    p3 = {
        'num_points': 75,
        'center': 10,
        'disp': 2
    }
    p4 = {
        'num_points': 75,
        'center': 13,
        'disp': 3
    }

    @classmethod
    def setupClass(cls):
        cls._space = Space(cls.space['dimensions'], cls.space['labels'])
        #cls._points = np.random.normal(
                #(p1['center'], p2['center'], p3['center'], p4['center']),
                #(p1['disp'], p2['disp'], p3['disp'], p4['disp']),
                #(p1['num_points'], p2['num_points'], p3['num_points'], p4['num_points'])
        #)
        cls._points_1 = np.random.normal(p1['center'], p1['disp'], p1['num_points'])
        cls._points_2 = np.random.normal(p2['center'], p2['disp'], p2['num_points'])
        cls._points_3 = np.random.normal(p3['center'], p3['disp'], p3['num_points'])
        cls._points_4 = np.random.normal(p4['center'], p4['disp'], p4['num_points'])

        cls._cluster_1 = Cluster(cls._points_1)
        cls._cluster_2 = Cluster(cls._points_2)
        cls._cluster_3 = Cluster(cls._points_3)
        cls._cluster_4 = Cluster(cls._points_4)

