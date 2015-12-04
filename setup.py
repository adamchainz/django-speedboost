import os
import re
import sys

from distutils import sysconfig
from setuptools import setup

site_packages_path = sysconfig.get_python_lib(plat_specific=True)
site_packages_rel_path = site_packages_path[len(sysconfig.EXEC_PREFIX) + 1:]

try:
    from Cython.Build import cythonize
except ImportError:
    print("Could not import Cython.Build. Install `cython` and rerun.")
    sys.exit(1)


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


version = get_version('django_speedboost')


setup(
    name='django-speedboost',
    version=version,
    packages=get_packages('django_speedboost'),
    ext_modules=cythonize('**/*.pyx'),
    data_files=[
        (site_packages_rel_path, ['django_speedboost.pth']),
    ],
)
