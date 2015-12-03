=================
Django Podcasting
=================

Audio podcasting functionality for django sites.

The source code for Django Podcasting can be found and contributed to on
django-podcasting_. There you can also file tickets.


History
=======

Django Podcasting started off as a heavily stripped down version of
the wonderful django-podcast_. Eventually this app grew enough
differences to be useful to others as a reusable applciation outside
of my sandbox. I hope it inspires you to share your sounds with the
rest of the world, whatever they may be.

This application can seen running on:

    http://snowprayers.net

    http://rizu.mu


Differences
===========

At the time I had no interset in the Video podcasting features of
django-podcast_ and video introduces a lot of extra complexity into
the application, considering I was first studying compliance with
the various specs and the `syndication feed framework
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

An individual podcast is a ``show``.

A ``show`` has many ``episodes`` 001, 002, etc.

An ``episode`` has one or many ``enclosures`` formats for example
.flac, .wav or .mp3.


Requirements
============

``django-podcasting`` requires ``django-autoslug`` which is included
in the setup.py.


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

  To publish a podcast to iTunes it is required to set a
  license. It is suggested to install django-licenses_ which provides a light
  weight mechanism for adding licenses to the shows.

**Serve your media from anywhere**
  Podcasting assumes nothing about where your media file will be
  stored, simply save any valid url to an enclosure object.

**Multiple enclosure types**
  Want to offer versions in .ogg, .flac, and .mp3? It's possible.

**UUID**
  Podcasting uses a UUID field for show and episode uniqueness rather
  than relying on the url.

**Bundled Forms and Templates**
  Podcasting comes with some example forms to get you started with
  for allowing site users ability to manage a show. Generic templates
  are also bundled to get you started.

**Comments**
  To add commenting to you app, you must use a separate Django
  application. One of the simplest options is
  django-disqus_, but you should also look into django-threadedcomments_
  and Django's built in `comments framework
  <http://docs.djangoproject.com/en/dev/ref/contrib/comments/>`_.

  There is an field on both the Show and Episode models to enable
  commenting. The default is to enable commenting. To completely
  disable comments for all of an individual show's episodes, set
  ``enable_comments`` field on the Show model to ``False``. To disable
  comments on an individual episode, set ``enable_comments`` on the
  Show model to ``True`` and ``enable_comments`` on the Episode model
  to ``False``.

**Draft Mode**
  You may work on the new episode in and publish it when ready, simply
  by checking publish in the Admin. While in draft mode the episode's
  ``get_absolute_url`` returns a link comprised of the show_slug and
  the episode's ``uuid`` but once live, it uses
  the show slug, friendlier publish date and episode slug.

    http://snowprayers.net/podcasts/snowprayers/a04deb06-741f-11e0-a714-404096327b80/
    http://snowprayers.net/podcasts/snowprayers/snowprayers-podcast-13/


Optional Features
=================

The following features are expected to work with the most recent
versions of the following libraries, if you find an issue please
report it on github.

**Thumbnailed Album Artwork** Install django-imagekit_,
  easy-thumbnails_ or sorl-thumbnails_ in your project to get sane
  defaults and model support for album artwork thumbnails. Either may
  be is added to your project at point any time and the
  ``django-podcasting`` app will recognize and use it. It is highly
  advised to use a thumbnailing app because thumbnailing podcast
  artwork for iTunes is nontrivial. Support for other thumbnail
  libraries will be considered for inclusion.

**Taggable episodes and shows**
  Install django-taggit_ to provide tagging support for episodes and
  shows. Taggit may be is added to your project at point any time and
  the ``django-podcasting`` app will recognize and support it. Taggit
  may become a requirement in 1.0 if there are no strong objections.

**Share to Twitter**
  Django Pocasting can optionally provide the ability to announce new
  episodes on twitter. Install python-twitter_ to get started.

**Embeddable Media**
  Want to display Youtube, Vimeo or Soundcloud content on Episode
  detail pages? Django Pocasting provides the ability to link to
  external embeddable media via the `podcasting.models.EmbedMedia`
  class. Optionally install django-embed-video_ for easy embedding of
  YouTube and Vimeo videos and music from SoundCloud.


Usage
=====
There has yet to be a need to configure anything via the
``settings.py`` file and the included templates and forms should be
enough to get started. One area that may be somewhat difficult is
connecting with a commenting application. For the simplest option,
take a look at django-disqus_.


Future
======
For the 0.9.x series I'd like to first see if others have interest in
this application and fix any issues discovered with the current
version.

If there is desire, video support after a 1.0 (audio only) version has
been released is possible.


Contents
========

.. toctree::
 :maxdepth: 1

 installation
 changelog

.. _Atom: http://www.atomenabled.org/developers/syndication/
.. _django-autoslug: https://bitbucket.org/neithere/django-autoslug/
.. _django-disqus: https://github.com/arthurk/django-disqus/
.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments/
.. _django-licenses: https://bitbucket.org/jezdez/django-licenses/
.. _django-imagekit: https://github.com/jdriscoll/django-imagekit/
.. _easy-thumbnails: https://github.com/SmileyChris/easy-thumbnails/
.. _sorl: https://github.com/mariocesar/sorl-thumbnail/
.. _django-podcast: https://github.com/jefftriplett/django-podcast/
.. _django-podcasting: https://github.com/rizumu/django-podcasting/
.. _django-taggit: https://github.com/alex/django-taggit/
.. _FeedBurner: http://www.feedburner.com/
.. _iTunes: http://www.apple.com/itunes/podcasts/specs.html
.. _python-twitter: http://code.google.com/p/python-twitter/
.. _django-embed-video: https://github.com/yetty/django-embed-video/
