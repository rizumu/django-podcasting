from django.conf.urls import include, url


urlpatterns = [
    url(r"^podcasts/", include("podcasting.urls")),
]
