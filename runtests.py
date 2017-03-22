#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings

try:
    import licenses
except ImportError:
    licenses = False
    
try:
    import photologue
except ImportError:
    photologue = False


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "podcasting",
        "podcasting.tests",
    ),
    MIDDLEWARE_CLASSES=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    SITE_ID = 1,
    ROOT_URLCONF="podcasting.tests.urls",
    SECRET_KEY="notasecret",
)

if licenses:
    DEFAULT_SETTINGS["INSTALLED_APPS"] += ("licenses",)

if photologue:
    DEFAULT_SETTINGS["INSTALLED_APPS"] += ("photologue",)

def runtests(*test_args):
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, "setup"):
        django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner
        runner_class = DiscoverRunner
        test_args = ["podcasting.tests"]
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        runner_class = DjangoTestSuiteRunner
        test_args = ["tests"]

    failures = runner_class(verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == "__main__":
    runtests(*sys.argv[1:])
