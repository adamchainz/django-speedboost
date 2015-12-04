__django_version__ = '1.8.7'
__version__ = '1.8.7.0'
# Can't concat __django_version__ in __version__ because it breaks setup.py
assert __version__.startswith(__django_version__)
