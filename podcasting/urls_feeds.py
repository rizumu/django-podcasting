from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from podcasting.feeds import RssShowFeed, AtomShowFeed


urlpatterns = patterns(
    "",

    # Episode list feed by show (RSS 2.0 and iTunes)
    url(r"^(?P<show_slug>[-\w]+)/(?P<mime_type>[-\w]+)/rss/$",
        RssShowFeed(), name="podcasts_show_feed_rss"),

    # Episode list feed by show (Atom)
    url(r"^(?P<show_slug>[-\w]+)/(?P<mime_type>[-\w]+)/atom/$",
        AtomShowFeed(), name="podcasts_show_feed_atom"),

    # Episode list feed by show (Media RSS)
    # TODO upon request

    # Previously we had /itunes/ in the feed url.
    # This is now deprecated and redirects to a more general feed url.
    url(r"^(?P<show_slug>[-\w]+)/itunes/(?P<mime_type>[-\w]+)/rss/$",
        RedirectView.as_view(pattern_name="podcasts_show_feed_rss")),
    url(r"^(?P<show_slug>[-\w]+)/itunes/(?P<mime_type>[-\w]+)/atom/$",
        RedirectView.as_view(pattern_name="podcasts_show_feed_atom")),
)
