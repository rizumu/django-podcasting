=================
Django Podcasting
=================

Audio podcasting functionality for django sites.

History
=======
Django Podcasting started off as a heavily stripped down version of
the wonderful django-podcast_. Eventually this app grew enough
differences to be useful to others as a reusable applciation outside
of my sandbox. I hope it inspires you to share your sounds with the
rest of the world, whatever they may be.

This application is currently in use on:

    http://snowprayers.net/

    http://rizumu.us/

Differences
===========
At the time I had no interset in the Video podcasting features of
django-podcast_ and video introduces a lot of extra complexity into
the project. Considering I was first studying compliance with the
various specs and the `syndication feed framework
<http://docs.djangoproject.com/en/dev/ref/contrib/syndication/>`_.

This application also differs from django-podcast_ in that it uses
UUID identifiers, support multiple authors,makes use of Django's 
`sites framework
<http://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ and
`syndication feed framework
<http://docs.djangoproject.com/en/dev/ref/contrib/syndication/>`_. Podcasting
only supports Django 1.3 or greater due to its choice in class-based views,
though writing additional views and urls to work with 1.2 would be a trivial
task. There are also other less significant diffences which may or may not
be of relavance to your project.

Nomenclature
============
An individual podcast is a ``show``. A ``show`` has many ``episodes``:
001, 002, etc. An ``episode`` may link to multiple ``enclosures`` of
varying types.

Requirements
============
``django-podcasting`` requires ``django-licenses`` which is included
in the setup.py and Django 1.3 or greater due to its choice in
class-based views.

Features
========

**Feeds**
  Supports Atom_, `RSS 2.0 <http://cyber.law.harvard.edu/rss/rss.html>`_,
  iTunes_, and FeedBurner_ by attempting to match as best as possible
  their detailed specifications and additionally utilizing Django's 
  `syndication feed framework
  <http://docs.djangoproject.com/en/dev/ref/contrib/syndication/>`_.

**Multi-site**
  Supports Django's `sites framework
  <http://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ allowing
  for great flexibility in the relationships between shows and sites
  in a multi-site application.

**Licensing** 
  Requires django-licenses_ which provides a light weight mechanism
  for adding licenses to the shows.   

**Serve your media from anywhere**
  Podcasting assumes nothing about where your media file will be
  stored, simply save any valid url to an enclosure object.

**Multiple enclosure types**
  Want to serve .ogg, .flac, .mp3 or more? It's possible.

**UUID**
  Podcasting uses a UUID field for show and episode uniqueness rather
  than relying on the url.

**Bundled Forms and Templates**
  Podcasting comes with some example forms to get you started with
  allowing non Admin users to manage a show. Generic templates are
  also bundled to get you started.

**Comments**
  To add commenting to you app, you must use a separate Django
  application. One of the simplest options is
  django-Disqus_, but you should also into django-threadedcomments_
  and Django's built in `comments framework
  <http://docs.djangoproject.com/en/dev/ref/contrib/comments/>`_.

  There is an field on both the Show and Episode models to enable
  commenting. The default is to enable commenting. To completely
  disable comments for all of an individual show's episodes, set
  ``enable_comments`` field on the Show model to ``False``. To disable
  comments on an individual episode, set ``enable_comments`` on the
  Show model to ``True`` and ``enable_comments`` on the Episode model
  to ``False``.

**Share to Twitter**
  Django Pocasting can optionally provide the ability to announce new
  episodes on twitter.

**Draft Mode**
  You may work on the new episode in a draft mode, and publish it when
  ready.

Options
=======

**Thumbnailed Album Artwork**
  Install django-imagekit_ in your project provides to get sane
  defaults and model support for album artwork thumbnails. ImageKit
  may be is added to your project at point any time and the
  ``django-podcasting`` app will recognize and use it. Support for
  other thumbnail libraries will be considered for inclusion.

**Taggable episodes and shows**
  Install django-taggit_ to provide tagging support for episodes and
  shows. Taggit may be is added to your project at point any time and
  the ``django-podcasting`` app will recognize and support it.

sage
=====
At the moment there are not settings and the included templates are
enough to get started. One area that may be confusing is connecting
with a commenting application. For the simplest option, take a look at
django-disqus_.

Future
======
For the 0.9.x series I'd like to first see if others have interest in
this application and fix any issues discovered with the current
version. At the moment, multiple authors are supported in the
application, but onlye one shows on the feed pages. This is a bug that
I'd like to fix soon. Also I'd like to do one last double check of the
specs to verify I've best matched all the options. Adding tests and
more documentation is also of high importance at this time.

If there is desire I'd like to eventually add in video support
after a 1.0 (audio only) version has been released.

Contents
========

.. toctree::
 :maxdepth: 1

 installation

.. _django-podcast: https://github.com/jefftriplett/django-podcast/
.. _Atom: http://www.atomenabled.org/developers/syndication/
.. _iTunes: http://www.apple.com/itunes/podcasts/specs.html
.. _FeedBurner: http://www.feedburner.com/
.. _django-disqus: https://github.com/arthurk/django-disqus
.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments
.. _django-licenses: https://bitbucket.org/jezdez/django-licenses/
.. _django-imagekit: https://github.com/jdriscoll/django-imagekit/
.. _django-taggit: https://github.com/alex/django-taggit/
.. _python-twitter: http://code.google.com/p/python-twitter/
