from django_speedboost import template

register = template.Library()


@register.simple_tag
def echo2(arg):
    return arg
