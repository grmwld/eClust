#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import numpy

from setuptools import setup, Extension
from Cython.Distutils import build_ext


def readme():
    with open('./README.rst') as f:
        return f.read()

setup(
    name='eClust',
    version='0.0.1',
    author='Alexis GRIMALDI',
    author_email='alexis.grimaldi@gmail.com',
    packages=['eclust', 'eclust.tests'],
    test_suite='nose.collector',
    scripts=[],
    url='http://pypi.python.org/pypi/eClust/',
    license='LICENSE.txt',
    description='Clustering based on a genetic algorithm',
    long_description=readme(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    install_requires=['cython', 'numpy', 'scipy'],
    tests_require=['nose'],
    #cmdclass={'build_ext': build_ext},
    #ext_modules=[
        #Extension(
            #name='cdist',
            #sources=['eclust/cdist.pyx'],
            #extra_link_args=['-fopenmp'],
            #extra_compile_args=['-fopenmp'],
            #include_dirs=[numpy.get_include()]
        #)
    #]
)
