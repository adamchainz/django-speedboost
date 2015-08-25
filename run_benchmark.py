#!/usr/bin/env python
import timeit
from textwrap import dedent

try:
    # Django 1.8+
    from django.db.backends.mysql.operations import DatabaseOperations
except ImportError:
    from django.db.backends.mysql.base import DatabaseOperations


ops = DatabaseOperations(connection=None)


def main():
    result_orig = timeit.timeit(
        setup="from __main__ import ops",
        stmt=dedent("""\
        ops.quote_name("identifier")
        ops.quote_name("`identifier`")
        """)
    )
    print "original quote_name:", result_orig
    result_speedboost = timeit.timeit(
        setup="import _django_speedboost",
        stmt=dedent("""\
        _django_speedboost.mysql_quote_name("identifier")
        _django_speedboost.mysql_quote_name("`identifier`")
        """)
    )
    print "django_speedboost quote_name:", result_speedboost
    print "relative speed boost", (result_orig / result_speedboost)


if __name__ == '__main__':
    main()
