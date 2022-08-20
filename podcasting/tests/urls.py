try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

from django.conf.urls import include


urlpatterns = [
    url(r"^podcasts/", include("podcasting.urls")),
]
