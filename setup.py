import sys

from setuptools import setup

try:
    from Cython.Build import cythonize
except ImportError:
    print("Could not import Cython.Build. Install `cython` and rerun.")
    sys.exit(1)


setup(
    name='django-speedboost',
    packages=['django_speedboost'],
    ext_modules=cythonize('django_speedboost/**/*.pyx')
)
