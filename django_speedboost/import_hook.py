import importlib
import sys
from collections import defaultdict


class HookSpec(object):
    def __init__(self):
        self.before = []
        self.replacer = None
        self.after = []


class HookImporter(object):
    to_do = defaultdict(HookSpec)
    done = set()

    def find_module(self, fullname, path=None):
        if fullname in self.to_do and fullname not in self.done:
            self.path = path
            self.done.add(fullname)
            return self
        return None

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        spec = self.to_do[name]

        for func in spec.before:
            func()

        if spec.replacer is None:
            # Here we re-invoke Python's import machinery to import the module
            # We will now ignore it in find_module so it will be found in the
            # usual manner
            mod = importlib.import_module(name)
        else:
            mod = spec.replacer()
            sys.modules[name] = mod

        for func in spec.after:
            func(mod)

        return mod


importer = HookImporter()
sys.meta_path.append(importer)


def before_imported(name):
    def decorator(func):
        importer.to_do[name].before.append(func)
        return func
    return decorator


def replaces(name):
    def decorator(func):
        importer.to_do[name].replacer = func
        return func
    return decorator


def after_imported(name):
    def decorator(func):
        importer.to_do[name].after.append(func)
        return func
    return decorator

# Now everything has been setup, we can register all the replacements
from .replacements import *  # noqa
