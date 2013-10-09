#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from unittest import TestCase

from .. import Space

class TestSpace(TestCase):

    space_3d_withlabels = {
        'dimensions': 3,
        'labels': ['D1', 'D2', 'D3']
    }
    space_3d = {
        'dimensions': 3,
        'labels': ['0', '1', '2']
    }

    @classmethod
    def setupClass(cls):
        cls._space_3d_withlabels = Space(
                cls.space_3d_withlabels['dimensions'],
                cls.space_3d_withlabels['labels']
        )
        cls._space_3d = Space(cls.space_3d['dimensions'])

    def test_dimensions(self):
        self.assertEqual(
                self._space_3d_withlabels.dimensions,
                self.space_3d_withlabels['dimensions']
        )
        self.assertEqual(
                self._space_3d.dimensions,
                self.space_3d['dimensions']
        )

    def test_labels(self):
        self.assertEqual(
                self._space_3d_withlabels.labels,
                self.space_3d_withlabels['labels']
        )
        self.assertEqual(self._space_3d.labels, self.space_3d['labels'])
        
        self.assertEqual(
                self._space_3d_withlabels[1],
                self.space_3d_withlabels['labels'][1]
        )
        self.assertEqual(self._space_3d_withlabels['D2'], 1)

