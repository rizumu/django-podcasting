from django.conf.urls import include, patterns, url


urlpatterns = patterns(
    "",

    url(r"^podcasts/", include("podcasting.urls")),
)
