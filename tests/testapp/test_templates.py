# -*- coding:utf-8 -*-
from django.template.base import Node
from django.test import TestCase


class TemplateTests(TestCase):

    def test_is_patched(self):
        type_ = type(Node.render.im_func)
        assert type_.__name__ == 'cython_function_or_method'
