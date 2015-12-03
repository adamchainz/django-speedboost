# -*- coding:utf-8 -*-
from django.test import TestCase

import django.template.base


class PatchedTests(TestCase):

    def test_is_patched(self):
        assert getattr(django.template.base, '_django_speedboost')
