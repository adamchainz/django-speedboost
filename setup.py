import sys

from distutils import sysconfig
from setuptools import find_packages, setup

site_packages_path = sysconfig.get_python_lib(plat_specific=True)
site_packages_rel_path = site_packages_path[len(sysconfig.EXEC_PREFIX) + 1:]

try:
    from Cython.Build import cythonize
except ImportError:
    print("Could not import Cython.Build. Install `cython` and rerun.")
    sys.exit(1)


setup(
    name='django-speedboost',
    version='1.8.7.0',  # Django version + our version for that
    packages=find_packages(exclude=['tests']),
    ext_modules=cythonize('**/*.pyx'),
    data_files=[
        (site_packages_rel_path, ['django_speedboost.pth']),
    ],
)
