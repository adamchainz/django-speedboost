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

# print >> sys.stderr, site_packages_path

setup(
    name='django-speedboost',
    packages=['django_speedboost'],
    ext_modules=cythonize("_django_speedboost.pyx"),
    data_files=[
        (site_packages_rel_path, ['django_speedboost.pth']),
    ],
)
