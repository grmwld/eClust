from distutils.core import setup

def readme():
    with open('./README.rst') as f:
        return f.read()

setup(
    name='eClust',
    version='0.0.1',
    author='Alexis GRIMALDI',
    author_email='alexis.grimaldi@gmail.com',
    packages=['eclust', 'eclust.tests'],
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
    ]
)
