#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
import multiprocessing
from functools import lru_cache
import types
import copyreg

from scipy.spatial.distance import euclidean



def _pickle_method(method):
    # Author: Steven Bethard
    # http://bytes.com/topic/python/answers/552476-why-cant-you-pickle-instancemethods
    func_name = method.__func__.__name__
    obj = method.__self__
    cls = method.__class__
    cls_name = ''
    if func_name.startswith('__') and not func_name.endswith('__'):
        cls_name = cls.__name__.lstrip('_')
    if cls_name:
        func_name = '_' + cls_name + func_name
    print(func_name, obj, cls)
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    # Author: Steven Bethard
    # http://bytes.com/topic/python/answers/552476-why-cant-you-pickle-instancemethods
    for cls in cls.mro():
        print(cls.__dict__)
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

# This call to copyreg.pickle allows you to pass methods as the first arg to
# mp.Pool methods. If you comment out this line, `pool.map(self.foo, ...)` results in
# PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup
# __builtin__.instancemethod failed
#copyreg.pickle(types.MethodType, _pickle_method, _unpickle_method)
#copyreg.pickle(types.FunctionType, _pickle_method, _unpickle_method)
copyreg.pickle( 
    types.MethodType, 
    lambda method: (getattr, (method.__self__, method.__func__.__name__)), 
    getattr
)



class BijectiveDict(dict):
    def __len__(self):
        return dict.__len__(self) / 2

    def __setitem__(self, key, value):
        if key in self:
            dict.__delitem__(self, dict.__getitem__(self, key))
            dict.__delitem__(self, key)
        if value in self:
            dict.__delitem__(self, dict.__getitem__(self, value))
            dict.__delitem__(self, value)
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)


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


def spawn(f):
    def fun(q_in, q_out):
        while True:
            i, x = q_in.get()
            if i == None:
                break
            q_out.put((i, f(x)))
    return fun


def parmap(f, X, nprocs = multiprocessing.cpu_count()):
    q_in   = multiprocessing.Queue(1)
    q_out  = multiprocessing.Queue()
    proc = [multiprocessing.Process(target=spawn(f), args=(q_in, q_out)) for _ in range(nprocs)]
    for p in proc:
        p.daemon = True
        p.start()
    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]
    [p.join() for p in proc]
    return [x for i, x in sorted(res)]


@lru_cache(maxsize=4096*4096)
def cached_distance(u, v):
    return euclidean(u, v)

#@lru_cache(maxsize=4096)
#def cached_distance(u, v, f=euclidean):
    #return f(u, v)
