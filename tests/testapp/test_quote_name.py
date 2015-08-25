# -*- coding:utf-8 -*-
import types

from django.db import connection
from django.test import TestCase


class QuoteNameTests(TestCase):

    def test_is_patched(self):
        assert isinstance(connection.ops.quote_name, types.BuiltinFunctionType)

    def test_basic(self):
        assert connection.ops.quote_name("unquoted") == "`unquoted`"

    def test_already_quoted(self):
        assert connection.ops.quote_name("`quoted`") == "`quoted`"
