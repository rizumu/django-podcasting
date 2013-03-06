Installation
============

* Requires Django 1.3 or greater

* Install Django Podcasting with your favorite Python package manager::

    pip install django-podcasting

* To install the in-development version of Django Podcasting::

    pip install ``django-podcasting==dev``


* Add ``'podcasting'`` and ``'licenses``, and the optional apps of your
  choice to the ``INSTALLED_APPS`` setting in your ``settings.py``::

    INSTALLED_APPS = (
        # other apps
        "podcasting",
        "licenses",
        "imagekit",
        "taggit",
        "python-twitter",
    )

* Add the following to your main ``urls.py``::

    url(r"^podcasts/", include("podcasting.urls")),
    url(r"^feeds/podcasts/", include("podcasting.urls_feeds")),

.. _dependencies:

Optional Dependencies
---------------------

To quickly install all requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    pip install -r requirements.txt

django-imagekit_
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    pip install django-imagekit==2.0.2

django-taggit_
^^^^^^^^^^^^^^^^^^^^^^^^^

    pip install django-taggit==0.9.3

python-twitter_
^^^^^^^^^^^^^^^^^^^^

    pip install python-twitter==0.8.7

.. _django-licenses: https://bitbucket.org/jezdez/django-licenses/
.. _django-imagekit: https://github.com/jdriscoll/django-imagekit/
.. _django-taggit: https://github.com/alex/django-taggit/
.. _python-twitter: http://code.google.com/p/python-twitter/
