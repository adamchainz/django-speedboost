# import imp
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
    done = set()

    def find_module(self, fullname, path=None):
        if fullname == 'django.template.base' and fullname not in self.done:
            self.path = path
            self.done.add('django.template.base')
            return self
        return None

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        # RECURSION
        # Now we won't respond to the new import statement
        mod = importlib.import_module(name)
        import pdb; pdb.set_trace()
        mod._django_speedboost = True
        return mod

if not any(isinstance(imp, SpeedboostImporter) for imp in sys.meta_path):
    sys.meta_path.append(SpeedboostImporter())
