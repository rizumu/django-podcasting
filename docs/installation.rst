Installation
============

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

.. _dependencies:

Optional Dependencies
=====================

The following features are expected to work with the most recent
versions of the following libraries, if you find an issue please
report it on github.

Thumbnails
----------

You may chose between the following three thumbnail libraries or none,
if imagekit is installed django-podcsating will use that, else it will
check for easy-thumbnails, followed by sorl.

* django-imagekit_: ``pip install django-imagekit``

* easy-thumbnails_: ``pip install easy-thumbnails``

Here is an example ``settings.THUMBNAIL_ALIASES`` for
`easy-thumbnails`. iTunes sizes are to spec.::

    THUMBNAIL_ALIASES = {
        "podcasting.Show.original_image": {
            "sm": {"size": (120, 120)},
            "lg": {"size": (550, 550)},
            "itunes_sm": {"size": (144, 144)},
            "itunes_lg": {"size": (1400, 1400)},
        },
        "podcasting.Episode.original_image": {
            "sm": {"size": (120, 120)},
            "lg": {"size": (550, 550)},
            "itunes_sm": {"size": (144, 144)},
            "itunes_lg": {"size": (1400, 1400)},
        },
    }

* Sorl-thumbnail_

    pip install sorl-thumbnail

Tagging
-------

If django-taggit is installed, tagging will be enabled for Episodes
and Shows:

* django-taggit_: ``pip install django-taggit``

Licencing
---------

If django-licenses is installed, the show will contain the license
field which which is helpful for publishing podcasts on iTunes:

* django-licenses_: ``pip install django-licenses``

Tweeting
--------

Want to send a tweet every time a new Episode is created?

If python-twiiter is installed, automatic posts for new tweets is possible:

* python-twitter_: ``pip install python-twitter``


Media Embedding
---------------

Want to display Youtube, Vimeo or Soundcloud content on Episode detail
pages?

* django-embed-video_: ``pip install django-embed-video``

.. _django-licenses: https://bitbucket.org/jezdez/django-licenses/
.. _django-imagekit: https://github.com/jdriscoll/django-imagekit/
.. _easy-thumbnails: https://github.com/SmileyChris/easy-thumbnails/
.. _sorl-thumbnail: https://github.com/sorl/sorl-thumbnail/
.. _django-taggit: https://github.com/alex/django-taggit/
.. _python-twitter: http://code.google.com/p/python-twitter/
.. _django-embed-video: https://github.com/yetty/django-embed-video/
