from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import rfc2822_date, Rss201rev2Feed, Atom1Feed
from django.shortcuts import get_object_or_404

from django.contrib.sites.models import get_current_site
from django.contrib.syndication.views import Feed
from django.views.generic.base import RedirectView

try:
    import imagekit
    easy_thumbnails = False
    sorl = False
except ImportError:
    pass

try:
    import easy_thumbnails
    imagekit = False  # noqa
    sorl = False
except ImportError:
    pass

try:
    import sorl
    imagekit = False
    easy_thumbnails = False  # noqa
except ImportError:
    pass

try:
    import licenses
except ImportError:
    licenses = False

from podcasting.models import Enclosure, Show
from podcasting.conf import settings as settings2


class ITunesElements(object):

    def add_root_elements(self, handler):
        """ Add additional elements to the show object"""
        super(ITunesElements, self).add_root_elements(handler)

        show = self.feed["show"]

        if show.original_image:
            if imagekit:
                itunes_sm_url = show.img_itunes_sm.url
                itunes_lg_url = show.img_itunes_lg.url
            elif easy_thumbnails:
                aliases = settings.THUMBNAIL_ALIASES["podcasting.Show.original_image"]
                thumbnailer = easy_thumbnails.files.get_thumbnailer(show.original_image)
                try:
                    itunes_sm_url = thumbnailer.get_thumbnail(aliases["itunes_sm"]).url
                    itunes_lg_url = thumbnailer.get_thumbnail(aliases["itunes_lg"]).url
                except easy_thumbnails.exceptions.InvalidImageFormatError:
                    easy_thumbnails.signal_handlers.generate_aliases_global(show.original_image)
                    itunes_sm_url = thumbnailer.get_thumbnail(aliases["itunes_sm"]).url
                    itunes_lg_url = thumbnailer.get_thumbnail(aliases["itunes_lg"]).url
                except AttributeError:
                    itunes_sm_url = None
                    itunes_lg_url = None
            elif sorl:
                itunes_sm_url = sorl.thumbnail.get_thumbnail(show.original_image, "144x144").url
                itunes_lg_url = sorl.thumbnail.get_thumbnail(show.original_image, "1400x1400").url
            else:
                itunes_sm_url = show.original_image.url
                itunes_lg_url = show.original_image.url
            if itunes_sm_url and itunes_lg_url:
                handler.addQuickElement("itunes:image", attrs={"href": itunes_lg_url})
                handler.startElement("image", {})
                handler.addQuickElement("url", itunes_sm_url)
                handler.addQuickElement("title", self.feed["title"])
                handler.addQuickElement("link", self.feed["link"])
                handler.endElement("image")

        handler.addQuickElement("guid", str(show.uuid), attrs={"isPermaLink": "false"})
        handler.addQuickElement("itunes:subtitle", self.feed["subtitle"])
        handler.addQuickElement("itunes:author", show.author_text)
        handler.startElement("itunes:owner", {})
        handler.addQuickElement("itunes:name", show.owner.get_full_name())
        handler.addQuickElement("itunes:email", show.owner.email)
        handler.endElement("itunes:owner")
        handler.addQuickElement("itunes:category", attrs={"text": self.feed["categories"][0]})
        handler.addQuickElement("itunes:summary", show.description)
        handler.addQuickElement("itunes:explicit", show.get_explicit_display())
        if show.redirect:
            handler.addQuickElement("itunes:new-feed-url", show.redirect)
        handler.addQuickElement("keywords", show.keywords)
        if show.editor_email:
            handler.addQuickElement("managingEditor", show.editor_email)
        if show.webmaster_email:
            handler.addQuickElement("webMaster", show.webmaster_email)
        try:
            handler.addQuickElement("lastBuildDate",
                                    rfc2822_date(show.episode_set.published()[1].published))
        except IndexError:
            pass
        handler.addQuickElement("generator", "Django Web Framework")
        handler.addQuickElement("docs", "http://blogs.law.harvard.edu/tech/rss")

    def add_item_elements(self, handler, item):
        """ Add additional elements to the episode object"""
        super(ITunesElements, self).add_item_elements(handler, item)

        show = item["show"]
        episode = item["episode"]
        if episode.original_image:
            if imagekit:
                itunes_sm_url = episode.img_itunes_sm.url
                itunes_lg_url = episode.img_itunes_lg.url
            elif easy_thumbnails:
                aliases = settings.THUMBNAIL_ALIASES["podcasting.Episode.original_image"]
                thumbnailer = easy_thumbnails.files.get_thumbnailer(episode.original_image)
                try:
                    itunes_sm_url = thumbnailer.get_thumbnail(aliases["itunes_sm"]).url
                    itunes_lg_url = thumbnailer.get_thumbnail(aliases["itunes_lg"]).url
                except easy_thumbnails.exceptions.InvalidImageFormatError:
                    easy_thumbnails.signal_handlers.generate_aliases_global(episode.original_image)
                    itunes_sm_url = thumbnailer.get_thumbnail(aliases["itunes_sm"]).url
                    itunes_lg_url = thumbnailer.get_thumbnail(aliases["itunes_lg"]).url
                except AttributeError:
                    itunes_sm_url = None
                    itunes_lg_url = None
            elif sorl:
                itunes_sm_url = sorl.thumbnail.get_thumbnail(episode.original_image, "144x144").url
                itunes_lg_url = sorl.thumbnail.get_thumbnail(episode.original_image, "1400x1400").url  # noqa
            else:
                itunes_sm_url = episode.original_image.url
                itunes_lg_url = episode.original_image.url
            if itunes_sm_url and itunes_lg_url:
                handler.addQuickElement("itunes:image", attrs={"href": itunes_lg_url})
                handler.startElement("image", {})
                handler.addQuickElement("url", itunes_sm_url)
                handler.addQuickElement("title", episode.title)
                handler.addQuickElement("link", episode.get_absolute_url())
                handler.endElement("image")

        handler.addQuickElement("guid", str(episode.uuid), attrs={"isPermaLink": "false"})
        if licenses:
            handler.addQuickElement("copyright", "{0} {1} {2}".format(show.license.name,
                                                                      show.license.url,
                                                                      datetime.date.today().year))
        else:
            handler.addQuickElement("copyright", "{0} {1}".format(show.license,
                                                                  datetime.date.today().year))
        handler.addQuickElement("itunes:author", episode.author_text)
        handler.addQuickElement("itunes:subtitle", episode.subtitle)
        handler.addQuickElement("itunes:summary", episode.description)
        handler.addQuickElement("itunes:duration", "%02d:%02d:%02d" % (episode.hours,
                                                                       episode.minutes,
                                                                       episode.seconds))
        handler.addQuickElement("itunes:keywords", episode.keywords)
        handler.addQuickElement("itunes:explicit", episode.get_explicit_display())
        if episode.block:
            handler.addQuickElement("itunes:block", "yes")

    def namespace_attributes(self):
        return {"xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}


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
        if licenses:
            return "{0} {1} {2}".format(
                show.license.name, show.license.url, datetime.date.today().year)
        else:
            return "{0} {1}".format(show.license, datetime.date.today().year)

    def ttl(self, show):
        return show.ttl

    def items(self, show):
        return show.episode_set.published()[:settings2.PODCASTING_FEED_ENTRIES]

    def get_object(self, request, *args, **kwargs):
        self.mime = [mc[0] for mc in Enclosure.MIME_CHOICES if mc[0] == kwargs["mime_type"]][0]
        site = get_current_site(request)
        self.show = get_object_or_404(Show, slug=kwargs["show_slug"], sites=site)
        return self.show

    def item_title(self, episode):
        return episode.title

    def item_description(self, episode):
        "renders summary for atom"
        return episode.description

    def item_link(self, episode):
        return reverse("podcasting_episode_detail",
                       kwargs={"show_slug": self.show.slug, "slug": episode.slug})

    # def item_author_link(self, episode):
    #     return "todo" #this one doesn't add anything in atom or rss
    #
    # def item_author_email(self, episode):
    #     return "todo" #this one doesn't add anything in atom or rss

    def item_pubdate(self, episode):
        return episode.published

    def item_categories(self, episode):
        return self.categories(self.show)

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
        extra["show"] = self.show
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


class AtomRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, show_slug, mime_type):
        return reverse(
            "podcasts_show_feed_atom",
            kwargs={"show_slug": show_slug, "mime_type": mime_type})


class RssRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, show_slug, mime_type):
        return reverse(
            "podcasts_show_feed_rss",
            kwargs={"show_slug": show_slug, "mime_type": mime_type})
