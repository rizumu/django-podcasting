#!/usr/bin/env python
import os
import sys


def runtests(*test_labels):
    os.environ["DJANGO_SETTINGS_MODULE"] = "podcasting.tests.test_settings"

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    from django_nose import NoseTestSuiteRunner
    runner = NoseTestSuiteRunner(verbosity=1, interactive=True, failfast=False)
    failures = runner.run_tests(test_labels)

    # Nasty hack to fix `setup.py test` with nose.
    sys.exitfunc = lambda: 0

    sys.exit(failures)


if __name__ == "__main__":
    runtests(*sys.argv[1:])
