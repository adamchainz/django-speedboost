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
    base.Node = Node


class Node(object):
    speedboosted = True
    # Set this to True for nodes that must be first in the template (although
    # they can be preceded by text nodes.
    must_be_first = False
    child_nodelists = ('nodelist',)

    def render(self, context):
        """
        Return the node rendered as a string.
        """
        pass

    def __iter__(self):
        yield self

    def get_nodes_by_type(self, nodetype):
        """
        Return a list of all nodes (within this node and its nodelist)
        of the given type
        """
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        for attr in self.child_nodelists:
            nodelist = getattr(self, attr, None)
            if nodelist:
                nodes.extend(nodelist.get_nodes_by_type(nodetype))
        return nodes
