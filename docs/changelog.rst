Changelog
=========
master
------
- Fix autoslug

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
