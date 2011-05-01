from django.conf.urls.defaults import patterns, url
from podcasting.feeds import RssShowFeed, AtomShowFeed


urlpatterns = patterns("",
    # Episode list feed by show (RSS 2.0 and iTunes)
    url(r"^(?P<show_slug>[-\w]+)/itunes/(?P<mime_type>[-\w]+)/rss/$",
        RssShowFeed(), name="podcasts_show_feed_rss"),
    # Episode list feed by show (Atom)
    url(r"^(?P<show_slug>[-\w]+)/itunes/(?P<mime_type>[-\w]+)/atom/$",
        AtomShowFeed(), name="podcasts_show_feed_atom"),
    # Episode list feed by show (Media RSS)
    # TODO upon request
)
