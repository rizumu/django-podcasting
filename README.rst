Django Podcasting
=================

Django Podcasting is a reusable application which provides audio
podcasting functionality for websites running on the Django Web
framework.

|buildstatus|_ (only failing on Django 1.7 dev branch)

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

* Requires Django 1.4 or greater

* Install Django Podcasting with your favorite Python package manager::

    pip install django-podcasting

* To install the `in-development version`_ of Django Podcasting::

    pip install django-podcasting==dev


* Add ``"podcasting"`` and ``"licenses"``, and the optional apps of your
  choice to the ``INSTALLED_APPS`` setting in your ``settings.py``::

    INSTALLED_APPS = (
        "podcasting",
        "licenses",
    )

* Add the following to your main ``urls.py``::

    url(r"^podcasts/", include("podcasting.urls")),
    url(r"^feeds/podcasts/", include("podcasting.urls_feeds")),

.. _github.com/rizumu/django-podcasting: https://github.com/rizumu/django-podcasting/
.. _django-podcasting.readthedocs.org: http://django-podcasting.readthedocs.org/
.. _file issues: https://github.com/rizumu/django-podcasting/issues/
.. _in-development version: https://github.com/rizumu/django-podcasting/tarball/master#egg=django-podcasting-dev
.. _the changelog: http://django-podcasting.readthedocs.org/en/latest/changelog.html
.. |buildstatus| image:: https://secure.travis-ci.org/rizumu/django-podcasting.png?branch=master
.. _buildstatus: http://travis-ci.org/#!/rizumu/django-podcasting
