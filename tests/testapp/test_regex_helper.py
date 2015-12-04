# -*- coding:utf-8 -*-
import types

from django.test import SimpleTestCase
from django.utils import regex_helper


class NormalizePatchedTests(SimpleTestCase):

    def test_is_patched(self):
        assert isinstance(regex_helper.normalize, types.BuiltinFunctionType)
