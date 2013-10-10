#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
from functools import lru_cache

from scipy.spatial.distance import euclidean


def read_datafile(f, header=True, dtypes=None):
    headers = []
    rows = []
    columns = {}
    reader = csv.reader(f, delimiter='\t')
    row = next(reader)
    if dtypes is None:
        dtypes = [str.strip] * len(row)
    elif len(dtypes) != len(row):
        raise ValueError('Incorrect number of datatypes provided')
    if header:
        headers = row
    else:
        headers = ['D'+str(i) for i in range(len(row))]
        rows.append(row)
    for h in headers:
        columns[h] = []
    for row in reader:
        typed_row = []
        for h, v, c in zip(headers, row, dtypes):
            columns[h].append(c(v))
            typed_row.append(c(v))
        rows.append(typed_row)
    return {
        'headers': headers,
        'rows': rows,
        'columns': columns
    }


def initialize_points(data):
    headers = data['headers']
    rows = data['rows']
    space = Space(len(headers), headers)
    points = Dataset
    for row in rows:
        points.append(Point(space, row))
    return points


@lru_cache(maxsize=4096)
def cached_distance(u, v, f=euclidean):
    return f(u, v)
