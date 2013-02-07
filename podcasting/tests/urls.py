from django.conf.urls import *

urlpatterns = patterns("",
    url(r"^podcasts/", include("podcasting.urls")),
    )
