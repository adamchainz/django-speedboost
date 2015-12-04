# -*- coding:utf-8 -*-
from django.test import TestCase

import django.template.defaulttags


class PatchedTests(TestCase):

    def test_is_patched(self):
        assert getattr(django.template.defaulttags.IfNode, '_speedboosted')
