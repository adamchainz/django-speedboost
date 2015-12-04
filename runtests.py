#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import subprocess

import pytest

try:
    from flake8.main import main as flake8_main
except ImportError:
    pass


def main():
    try:
        sys.argv.remove('--nolint')
    except ValueError:
        run_lint = True
    else:
        run_lint = False

    try:
        sys.argv.remove('--lintonly')
    except ValueError:
        run_tests = True
    else:
        run_tests = False

    try:
        sys.argv.remove('--nodjangotests')
    except ValueError:
        run_django_tests = True
    else:
        run_django_tests = False

    if run_tests:
        exit_on_failure(tests_main())
        if run_django_tests:
            exit_on_failure(tests_django())

    if run_lint:
        exit_on_failure(run_flake8())
        exit_on_failure(run_isort())
        exit_on_failure(run_setup_py_check())


def tests_main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    sys.path.insert(0, "tests")
    return pytest.main()


def tests_django():
    # Downloads the relevant version of Django
    env_path = os.environ['VIRTUAL_ENV']
    exitcode = subprocess.call([
        'ansible-playbook', 'runtests-django.yml',
        '-i', '127.0.0.1,',
        '-e', 'env_path=' + env_path,
        '-e', 'python_version=' + str(sys.version_info[0]),
        '-e', 'django_version=1.8.7',
    ])
    if exitcode:
        return exitcode
    # Run Django's test suite
    django_path = env_path + '/djangotests/django-1.8.7/'
    return subprocess.call([
        sys.executable,
        django_path + 'tests/runtests.py',
        '--settings', 'test_sqlite',
        'template_tests',
    ])


def run_flake8():
    print('Running flake8 code linting')
    try:
        original_argv = sys.argv
        sys.argv = ['flake8', 'django_speedboost', 'tests']
        did_fail = False
        flake8_main()
    except SystemExit:
        did_fail = True
    finally:
        sys.argv = original_argv

    print('flake8 failed' if did_fail else 'flake8 passed')
    return did_fail


def run_isort():
    print('Running isort check')
    return subprocess.call([
        'isort', '--recursive', '--check-only', '--diff',
        'django_speedboost', 'tests'
    ])


def run_setup_py_check():
    print('Running setup.py check')
    return subprocess.call([
        'python', 'setup.py', 'check',
        '-s', '--restructuredtext', '--metadata'
    ])


def exit_on_failure(ret, message=None):
    if ret:
        sys.exit(ret)


if __name__ == '__main__':
    main()
