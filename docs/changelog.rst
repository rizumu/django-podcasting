Changelog
=========

master
------

1.3.1
----
- Bugfix for imports

1.3.0
----
- Django 1.10 compatibility - thanks @urtzai
- Add support for Photologue - thanks @urtzai

1.2.0
------
- Basque Translation - thanks @urtzai
- Add next/prev methods to episode.

1.1.0
------
- Multiple bugfixes
- Improvments to queryset managers
- Add a pretty description field for WYSIWYG editors

1.0.1
------
- Improve onsite manager by supporting mutliple environments, and getting site from request

1.0.0
------
- When no django-licensing is installed, show the Show's CharField
  license. @nachopro
- Setting to choose the path where podcast's images will be saved.
  Thanks @nachopro

0.10.2
------
- Fix for runserver warning, 'max_length' is ignored when used with IntegerField.

0.10.1
------
- Add missing `django-autoslug` requirement to setup.py. Thanks @Rolando.

0.10.0
------
- Fix unicode literals in models.py. Thanks @hakanw
- Convert relationships for Enclosure, Episode, Sites into M2M to
  allow mix and match show creation. Thanks to Jeff Lindsey
  @djangolackey

0.9.10
------
- Setting FEED_ENTRIES hides older episodes, use None (aka all) as default.
- More forgiving error handling on images in feeds.

0.9.9
------
- Add django-appconf to required packages
- RedirectView fixes - kike721
- Spanish translations - kike721
- Use AppConf for pagination settings - kike721
- Enforce that feed urls can only request supported mime types.
- Make feed_urs more generic by removing /itunes/. Redirect old style.
- Make django-licenses optional
- Drop bundled AutoSlug and use django-autoslug
- Rename the newly added Video class to EmbedMedia, and build in
  support for django-embed-video for easy embedding of SoundCloud, Vimeo
  and YouTube files on Episode detail pages.
- Add a show.on_itunes boolean and relax required fields to allow
  simpler user forms when not publishing to iTunes.
- Testing on Python3
- Move runtests.py to homedir, drop django-nose and add test support
  for Django 1.7, add coverage and version badges.
- Extend full support to easy-thumbnails and sorl
- Extend the Admin widget to support sorl, imagekit, easy-thumbnails and css for thumbnailing.
- Add a simple Video model for attaching extrnal video-urls to an
  episode.
- Add more mime type choices for enclosures.
- Upgrade imagekit to 3.0.4
- Bump python-twitter to 1.0 and django-taggit to 0.10a1
- Remove settings.SITE_ID default from Site field.
- Setup Travis CI.
- Flake8.
- Support Django 1.5's customizable user model. This change makes
  django-podacasting usuable only on Django versions 1.4 LTS and greater.
- Fix autoslug
- Fix for non ImageKit installs
- Support Django 1.4's timezone-aware datetimes

0.9.4
-------
- Bump django-licenses version to 0.2.5
- Increase imagekit maxsize for fields because iTunes spec now allows
  artwork up to 1400x1400px
- Fix for autoslug: https://github.com/rizumu/django-podcasting/pull/11
- Update authors
- Use django-nose for tests

0.9.3
------
- Bump imagekit version to 2.0.1

- Add the missing publish option for shows in admin #9

0.9.2
------

- Fix upload path for images, slugify was stripping the extension.

- Simply user relationships to episodes and shows. Most importantly
  changing 'authors' to an 'author_text' charfield, and adding a
  Show.owner field. Requires a migration.

- Remove unused show feed templates which were part of old django
  syndication framework.

- Bump imagekit version to 1.1.0

0.9.1
------

- Many small fixes.

- Upgrade imagekit for better thumbnailing.

- Better forms and internationalized templates.

0.9.0
------

- First release.
