import sys

from .import_hook import after_imported, before_imported, replaces


@after_imported('django.db.backends.mysql.operations')
def replace_quote_name(mod):
    from django_speedboost.db.backends.mysql.operations import quote_name
    mod.DatabaseOperations.quote_name = quote_name


@replaces('django.utils.regex_helper')
def get_regex_helper():
    from django_speedboost.utils import regex_helper
    return regex_helper


@before_imported('django.template.defaulttags')
def patch_base():
    # N.B. django.template.base imports django.template.defaulttags before it
    # is fully defined. We take advantage of this to patch it before anything
    # else gets a chance to look at it - and take Node and inherit from it.
    from django_speedboost.template import base as fast_base
    base = sys.modules['django.template.base']
    names = [
        'Node', 'NodeList', 'TextNode', 'VariableNode', 'TagHelperNode',
    ]
    for name in names:
        setattr(base, name, getattr(fast_base, name))
