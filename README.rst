Django Podcasting
=================

Django Podcasting is a reusable application which provides audio
podcasting functionality for websites running on the Django Web
framework.

|docs|_
|build|_
|coverage|_
|requires|_

More documentation about the usage and installation of Django Podcasting
can be found on `django-podcasting.readthedocs.org`_.

The source code for Django Podcasting can be found and contributed to on
`github.com/rizumu/django-podcasting`_. There you can also `file issues`_.

To find out what's new in this version of django-podcasting, please see
`the changelog`_


Quick Installation Guide
========================

Please visit `django-podcasting.readthedocs.org`_ for the full
installation guide including optional thumbnailing, tagging and
twitter support.


* Tested against Django 1.8 and greater.


* Install Django Podcasting with your favorite Python package manager::

    pip install django-podcasting


* Add ``"podcasting"``, ``"django.contrib.sites"``,
  and the optional apps of your choice to the ``INSTALLED_APPS`` setting
  in your ``settings.py``::

    INSTALLED_APPS = (
        ...
        "django.contrib.admin",
        "django.contrib.sites",
        ...
        "podcasting",
        ...
    )


* Include ``podcasting.urls`` and ``podcasting.urls_feeds`` in your urls definition::

    url(r"^podcasts/", include("podcasting.urls")),
    url(r"^feeds/podcasts/", include("podcasting.urls_feeds")),


* To run the test suite::

    ./runtests.sh


.. _github.com/rizumu/django-podcasting: https://github.com/rizumu/django-podcasting/
.. _django-podcasting.readthedocs.org: http://django-podcasting.readthedocs.org/
.. _file issues: https://github.com/rizumu/django-podcasting/issues/
.. _in-development version: https://github.com/rizumu/django-podcasting/tarball/master#egg=django-podcasting-dev
.. _the changelog: http://django-podcasting.readthedocs.org/en/latest/changelog.html

.. |build| image:: https://secure.travis-ci.org/rizumu/django-podcasting.png?branch=master
.. _build: http://travis-ci.org/#!/rizumu/django-podcasting
.. |coverage| image:: https://coveralls.io/repos/rizumu/django-podcasting/badge.png?branch=master
.. _coverage: https://coveralls.io/r/rizumu/django-podcasting
.. |requires| image:: https://requires.io/github/rizumu/django-podcasting/requirements.png?branch=master
.. _requires: https://requires.io/github/rizumu/django-podcasting/requirements/?branch=master
.. |docs| image:: https://readthedocs.org/projects/django-podcasting/badge/?version=latest
.. _docs: https://readthedocs.org/projects/django-podcasting/?badge=latest
