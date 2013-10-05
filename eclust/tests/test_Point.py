#!/usr/bin/env python
# -*- coding:utf-8 -*-

from unittest import TestCase

from .. import Space, Point

class TestPoint(TestCase):

    space_3d = {
        'dimensions': 3,
        'labels': ['D1', 'D2', 'D3']
    }

    point_3d = {
        'coords': (3, 5, -4)
    }

    point_2d = {
        'coords': (0, 1)
    }

    @classmethod
    def setupClass(cls):
        cls._space_3d = Space(cls.space_3d['dimensions'], cls.space_3d['labels'])
        cls._point_3d = Point(cls._space_3d, cls.point_3d['coords'])

    def test_coords(self):
        self.assertEqual(
                self._point_3d.coords,
                self.point_3d['coords']
        )

    def test_getprojection(self):
        self.assertEqual(self._point_3d[1], self.point_3d['coords'][1])
        self.assertEqual(self._point_3d['D2'], self.point_3d['coords'][1])

