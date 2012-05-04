Changelog
=========
v0.9.3
------
- Bump imagekit version to 2.0.1

- Add the missing publish option for shows in admin #9

v0.9.2
------

- Fix upload path for images, slugify was stripping the extension.

- Simply user relationships to episodes and shows. Most importantly
  changing 'authors' to an 'author_text' charfield, and adding a
  Show.owner field. Requires a migration.

- Remove unused show feed templates which were part of old django
  syndication framework.

- Bump imagekit version to 1.1.0

v0.9.1
------

- Many small fixes.

- Upgrade imagekit for better thumbnailing.

- Better forms and internationalized templates.

v0.9.0
------

- First release.
