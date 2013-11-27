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
        "podcasting",
        "licenses",
    )

* Add the following to your main ``urls.py``::

    url(r"^podcasts/", include("podcasting.urls")),
    url(r"^feeds/podcasts/", include("podcasting.urls_feeds")),

.. _dependencies:

Optional Dependencies
---------------------

You may chose between the following two thumbnail libraries or none,
if imagekit is installed django-podcsating will use that, otherwise it
will check for sorl.:

django-imagekit_
^^^^^^^^^^^^^^^^

    pip install django-imagekit==3.0.4

sorl-thumbnail_
^^^^^^^^^^^^^^^

    pip install sorl-thumbnail==11.12

django-taggit_
^^^^^^^^^^^^^^

    pip install django-taggit==0.11.1

python-twitter_
^^^^^^^^^^^^^^^

    pip install python-twitter==1.1

.. _django-licenses: https://bitbucket.org/jezdez/django-licenses/
.. _django-imagekit: https://github.com/jdriscoll/django-imagekit/
.. _sorl-thumbnail: https://github.com/sorl/sorl-thumbnail
.. _django-taggit: https://github.com/alex/django-taggit/
.. _python-twitter: http://code.google.com/p/python-twitter/
