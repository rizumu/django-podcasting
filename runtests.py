#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings

try:
    import licenses
except ImportError:
    licenses = False


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "podcasting",
        "podcasting.tests",
    ),
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    MIDDLEWARE_CLASSES = (
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware"
    ),
    SITE_ID = 1,
    ROOT_URLCONF="podcasting.tests.urls",
    SECRET_KEY="notasecret",
)

if licenses:
    DEFAULT_SETTINGS["INSTALLED_APPS"] += ("licenses",)


def runtests(*test_args):
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, "setup"):
        django.setup()

    if not test_args:
        test_args = ["tests"]

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner
        runner_class = DiscoverRunner
        test_args = ['model_utils.tests']
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        runner_class = DjangoTestSuiteRunner
        test_args = ['tests']

    failures = runner_class(
        verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == "__main__":
    runtests(*sys.argv[1:])
