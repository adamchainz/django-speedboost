from django.test import TestCase

from django_speedboost.bla import foo


class MyTests(TestCase):
    def test_it(self):
        assert foo() == 1
