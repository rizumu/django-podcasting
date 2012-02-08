import datetime

from django.core.urlresolvers import reverse
from django.db.models import permalink
from django.utils.feedgenerator import rfc2822_date, Rss201rev2Feed, Atom1Feed
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed

from podcasting.models import Enclosure, Show


class ITunesElements(object):

    def add_root_elements(self, handler):
        """ Add additional elements to the show object"""
        super(ITunesElements, self).add_root_elements(handler)
        show = self.feed["show"]
        handler.addQuickElement(u"guid", str(show.uuid), attrs={"isPermaLink": "false"})
        handler.addQuickElement(u"itunes:subtitle", self.feed["subtitle"])
        handler.addQuickElement(u"itunes:author", show.author_text)
        handler.startElement(u"itunes:owner", {})
        handler.addQuickElement(u"itunes:name", show.owner.get_full_name())
        handler.addQuickElement(u"itunes:email", show.owner.email)
        handler.endElement(u"itunes:owner")
        handler.addQuickElement(u"itunes:image", attrs={"href": show.img_itunes_lg.url})
        handler.startElement(u"image", {})
        handler.addQuickElement(u"url", show.img_itunes_sm.url)
        handler.addQuickElement(u"title", self.feed["title"])
        handler.addQuickElement(u"link", self.feed["link"])
        handler.endElement(u"image")
        handler.addQuickElement(u"itunes:category", attrs={"text": self.feed["categories"][0]})
        handler.addQuickElement(u"itunes:summary", show.description)
        handler.addQuickElement(u"itunes:explicit", show.get_explicit_display())
        if show.redirect:
            handler.addQuickElement(u"itunes:new-feed-url", show.redirect)
        handler.addQuickElement(u"keywords", show.keywords)
        if show.editor_email:
            handler.addQuickElement(u"managingEditor", show.editor_email)
        if show.webmaster_email:
            handler.addQuickElement(u"webMaster", show.webmaster_email)
        try:
            handler.addQuickElement(u"lastBuildDate", rfc2822_date(show.episode_set.published()[1].published))
        except IndexError:
            pass
        handler.addQuickElement(u"generator", "Django Web Framework")
        handler.addQuickElement(u"docs", "http://blogs.law.harvard.edu/tech/rss")

    def add_item_elements(self, handler, item):
        """ Add additional elements to the episode object"""
        super(ITunesElements, self).add_item_elements(handler, item)
        episode = item["episode"]
        handler.addQuickElement(u"guid", str(episode.uuid), attrs={"isPermaLink": "false"})
        handler.addQuickElement(u"copyright", "{0} {1} {2}".format(episode.show.license.name, episode.show.license.url, datetime.date.today().year))
        handler.addQuickElement(u"itunes:author", episode.author_text)
        handler.addQuickElement(u"itunes:subtitle", episode.subtitle)
        handler.addQuickElement(u"itunes:summary", episode.description)
        handler.addQuickElement(u"itunes:duration", "%02d:%02d:%02d" % (episode.hours, episode.minutes, episode.seconds))
        handler.addQuickElement(u"itunes:keywords", episode.keywords)
        handler.addQuickElement(u"itunes:explicit", episode.get_explicit_display())
        if episode.block:
            handler.addQuickElement(u"itunes:block", "yes")
        handler.addQuickElement(u"itunes:image", attrs={"href": episode.img_itunes_lg.url})
        handler.startElement(u"image", {})
        handler.addQuickElement(u"url", episode.img_itunes_sm.url)
        handler.addQuickElement(u"title", episode.title)
        handler.addQuickElement(u"link", episode.get_absolute_url())
        handler.endElement(u"image")

    def namespace_attributes(self):
        return {u"xmlns:itunes": u"http://www.itunes.com/dtds/podcast-1.0.dtd"}


class AtomITunesFeedGenerator(ITunesElements, Atom1Feed):
    def root_attributes(self):
        atom_attrs = super(AtomITunesFeedGenerator, self).root_attributes()
        atom_attrs.update(self.namespace_attributes())
        return atom_attrs


class RssITunesFeedGenerator(ITunesElements, Rss201rev2Feed):
    def rss_attributes(self):
        rss_attrs = super(RssITunesFeedGenerator, self).rss_attributes()
        rss_attrs.update(self.namespace_attributes())
        return rss_attrs


class ShowFeed(Feed):
    """
    A feed of podcasts for iTunes and other compatible podcatchers.
    """
    def title(self, show):
        return show.title

    def link(self, show):
        return show.link

    def categories(self, show):
        return ("Music",)

    def feed_copyright(self, show):
        return "{0} {1} {2}".format(show.license.name, show.license.url, datetime.date.today().year)

    def ttl(self, show):
        return show.ttl

    def items(self, show):
        return show.episode_set.published()

    def get_object(self, request, *args, **kwargs):
        self.mime = [mc[0] for mc in Enclosure.MIME_CHOICES if mc[0] == kwargs["mime_type"]][0]
        self.show = get_object_or_404(Show, slug=kwargs["show_slug"])
        return self.show

    def item_title(self, episode):
        return episode.title

    def item_description(self, episode):
        "renders summary for atom"
        return episode.description

    def item_link(self, episode):
        return reverse("podcasting_episode_detail",
                       kwargs={"show_slug": episode.show.slug, "slug": episode.slug})

    # def item_author_link(self, episode):
    #     return "todo" #this one doesn't add anything in atom or rss
    #
    # def item_author_email(self, episode):
    #     return "todo" #this one doesn't add anything in atom or rss

    def item_pubdate(self, episode):
        return episode.published

    def item_categories(self, episode):
        return self.categories(episode.show)

    def item_enclosure_url(self, episode):
        try:
            e = episode.enclosure_set.get(mime=self.mime)
            return e.url
        except Enclosure.DoesNotExist:
            pass

    def item_enclosure_length(self, episode):
        try:
            e = episode.enclosure_set.get(mime=self.mime)
            return e.size
        except Enclosure.DoesNotExist:
            pass

    def item_enclosure_mime_type(self, episode):
        try:
            e = episode.enclosure_set.get(mime=self.mime)
            return e.get_mime_display()
        except Enclosure.DoesNotExist:
            pass

    def item_keywords(self, episode):
        return episode.keywords

    def feed_extra_kwargs(self, obj):
        extra = {}
        extra["show"] = self.show
        return extra

    def item_extra_kwargs(self, item):
        extra = {}
        extra["episode"] = item
        return extra


class AtomShowFeed(ShowFeed):
    feed_type = AtomITunesFeedGenerator

    def subtitle(self, show):
        return show.subtitle

    def author_name(self, show):
        return show.owner.get_full_name()

    def author_email(self, show):
        return show.owner.email

    def author_link(self, show):
        return show.link


class RssShowFeed(ShowFeed):
    feed_type = RssITunesFeedGenerator

    def item_guid(self, episode):
        "ITunesElements can't add isPermaLink attr unless None is returned here."
        return None

    def description(self, show):
        return show.description
