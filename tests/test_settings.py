INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "licenses",
    "podcasting",
    "tests",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        }
    }


SITE_ID = 1

ROOT_URLCONF = "tests.urls"
