from django.utils.encoding import force_str, force_text
from django.utils.safestring import mark_safe


class Node(object):
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


class NodeList(list):
    # Set to True the first time a non-TextNode is inserted by
    # extend_nodelist().
    contains_nontext = False

    def render(self, context):
        bits = []
        for node in self:
            if isinstance(node, Node):
                bit = self.render_node(node, context)
            else:
                bit = node
            bits.append(force_text(bit))
        return mark_safe(''.join(bits))

    def get_nodes_by_type(self, nodetype):
        "Return a list of all nodes of the given type"
        nodes = []
        for node in self:
            nodes.extend(node.get_nodes_by_type(nodetype))
        return nodes

    def render_node(self, node, context):
        return node.render(context)


class TextNode(Node):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return force_str("<Text Node: '%s'>" % self.s[:25], 'ascii',
                errors='replace')

    def render(self, context):
        return self.s


class VariableNode(Node):
    def __init__(self, filter_expression):
        self.filter_expression = filter_expression

    def __repr__(self):
        return "<Variable Node: %s>" % self.filter_expression

    def render(self, context):
        try:
            output = self.filter_expression.resolve(context)
        except UnicodeDecodeError:
            # Unicode conversion can fail sometimes for reasons out of our
            # control (e.g. exception rendering). In that case, we fail
            # quietly.
            return ''
        # django_speedboost: have to inner import render_value_in_context
        # because it is defined in django.template.base
        from django.template.base import render_value_in_context
        return render_value_in_context(output, context)


class TagHelperNode(Node):
    """
    Base class for tag helper nodes such as SimpleNode, InclusionNode and
    AssignmentNode. Manages the positional and keyword arguments to be passed
    to the decorated function.
    """

    def __init__(self, takes_context, args, kwargs):
        self.takes_context = takes_context
        self.args = args
        self.kwargs = kwargs

    def get_resolved_arguments(self, context):
        resolved_args = [var.resolve(context) for var in self.args]
        if self.takes_context:
            resolved_args = [context] + resolved_args
        resolved_kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
        return resolved_args, resolved_kwargs
