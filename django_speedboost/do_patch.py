from collections import defaultdict
import importlib
import sys


# Doesn't work - you can't reliably replace sys.modules
# from types import ModuleType
# class FakeModule(ModuleType):
#     _django_speedboost = True

#     def __getattribute__(self, name):
#         if name == '_orig_module':
#             return ModuleType.__getattribute__(self, name)
#         return getattr()

# sys.modules['django.template.base'] = FakeModule('django.template.base')


class SpeedboostImporter(object):
    to_do = defaultdict(lambda: defaultdict(list))
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

        # Here we are definitely *before* it gets imported
        for func in self.to_do[name]['before']:
            func()

        # RECURSION
        # Now we won't respond to the new import statement
        mod = importlib.import_module(name)

        # Here we are definitely *after* it gets imported
        for func in self.to_do[name]['after']:
            func()

        return mod

importer = SpeedboostImporter()

sys.meta_path.append(importer)


def before_imported(name):
    def take_a_func(func):
        importer.to_do[name]['before'].append(func)
        return func
    return take_a_func


@before_imported('django.template.defaulttags')
def patch_base():
    base = sys.modules['django.template.base']
    base._django_speedboost = True
