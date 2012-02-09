# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

# Handle optional external dependencies
try:
    from imagekit.models import ImageSpec
    from imagekit.processors import resize
except:
    ImageSpec = None

from licenses.fields import LicenseField

if "taggit" in settings.INSTALLED_APPS:
    from taggit.managers import TaggableManager
else:
    def TaggableManager():
        return None
try:
    import twitter
except ImportError:
    twitter = None

from podcasting.managers import EpisodeManager, ShowManager
from podcasting.utils.db import manager_from
from podcasting.utils.fields import AutoSlugField, UUIDField
from podcasting.utils.twitter import can_tweet


def get_show_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return "img/podcasts/{0}/{1}{2}".format(instance.slug, slugify(root), ext)


def get_episode_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return "img/podcasts/{0}/episodes/{1}{2}".format(instance.show.slug, slugify(root), ext)


class Show(models.Model):
    """
    A podcast show, which has many episodes.
    """
    EXPLICIT_CHOICES = (
        (1, _("yes")),
        (2, _("no")),
        (3, _("clean")),
    )
    uuid = UUIDField(_("id"), unique=True)

    created = models.DateTimeField(_("created"), default=datetime.now, editable=False)
    updated = models.DateTimeField(null=True, blank=True, editable=False)
    published = models.DateTimeField(null=True, blank=True, editable=False)

    site = models.ForeignKey(Site, default=settings.SITE_ID)

    ttl = models.PositiveIntegerField(_("ttl"), default=1440,
        help_text=_("""``Time to Live,`` the number of minutes a channel can be
        cached before refreshing."""))

    owner = models.ForeignKey(User, related_name="podcast_shows",
        help_text=_("""Make certain the user account has a name and e-mail address."""))

    editor_email = models.EmailField(_("editor email"), blank=True,
        help_text="Email address of the person responsible for the feed's content.")
    webmaster_email = models.EmailField(_("webmaster email"), blank=True,
        help_text="Email address of the person responsible for channel publishing.")

    license = LicenseField()

    organization = models.CharField(_("organization"), max_length=255,
        help_text=_("Name of the organization, company or Web site producing the podcast."))
    link = models.URLField(_("link"), help_text=_("""URL of either the main website or the
        podcast section of the main website."""))

    enable_comments = models.BooleanField(default=True)

    author_text = models.CharField("author text", max_length=255, help_text=_("""
        This tag contains the name of the person or company that is most widely attributed to
        publishing the Podcast and will be displayed immediately underneath the title of the Podcast.
        The suggested format is: 'email@example.com (Full Name)' but 'Full Name' only, is acceptable.
        Multiple authors should be comma separated."""))

    title = models.CharField(_("title"), max_length=255)
    slug = AutoSlugField(_("slug"), populate_from="title")

    subtitle = models.CharField(_("subtitle"), max_length=255,
        help_text=_("Looks best if only a few words, like a tagline."))

    description = models.TextField(_("description"), max_length=4000, help_text=_("""
        This is your chance to tell potential subscribers all about your podcast.
        Describe your subject matter, media format, episode schedule, and other
        relevant info so that they know what they'll be getting when they
        subscribe. In addition, make a list of the most relevant search terms
        that you want yourp podcast to match, then build them into your
        description. Note that iTunes removes podcasts that include lists of
        irrelevant words in the itunes:summary, description, or
        itunes:keywords tags. This field can be up to 4000 characters."""))

    original_image = models.ImageField(_("original image"), upload_to=get_show_upload_folder,
        help_text=_("""An attractive, original square JPEG (.jpg) or PNG (.png)
        image of exactly 1000x1000 pixels at 72 pixels per inch. Image will be
        scaled down to 50x50 pixels at smallest in iTunes.<br /><br />
        For episode artwork to display in iTunes, image must be
        <a href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">
        saved to file's <strong>metadata</strong></a> before enclosure uploading!"""))

    if ImageSpec:
        admin_thumb_sm = ImageSpec([resize.Crop(50, 50)], image_field="original_image",
                                   pre_cache=True, options={"quality": 100})
        admin_thumb_lg = ImageSpec([resize.Crop(450, 450)], image_field="original_image",
                                   pre_cache=True, options={"quality": 100})
        img_show_sm = ImageSpec([resize.Crop(120, 120)], image_field="original_image",
                                pre_cache=True, options={"quality": 100})
        img_show_lg = ImageSpec([resize.Crop(550, 550)], image_field="original_image",
                                pre_cache=True, options={"quality": 100})
        img_itunes_sm = ImageSpec([resize.Crop(144, 144)], image_field="original_image",
                                  pre_cache=True, options={"quality": 100})
        img_itunes_lg = ImageSpec([resize.Crop(1000, 1000)], image_field="original_image",
                                  pre_cache=True, options={"quality": 100})

    feedburner = models.URLField(_("feedburner url"), blank=True,
        help_text=_("""Fill this out after saving this show and at least one
        episode. URL should look like "http://feeds.feedburner.com/TitleOfShow".
        See <a href="http://code.google.com/p/django-podcast/">documentation</a>
        for more. <a href="http://www.feedburner.com/fb/a/ping">Manually ping</a>"""))

    # iTunes specific fields
    explicit = models.PositiveSmallIntegerField(_("explicit"), default=1, choices=EXPLICIT_CHOICES,
        help_text=_("``Clean`` will put the clean iTunes graphic by it."))
    redirect = models.URLField(_("redirect"), blank=True,
        help_text=_("""The show's new URL feed if changing
        the URL of the current show feed. Must continue old feed for at least
        two weeks and write a 301 redirect for old feed."""))
    keywords = models.CharField(_("keywords"), max_length=255,
        help_text=_("""A comma-demlimitedlist of up to 12 words for iTunes
        searches. Perhaps include misspellings of the title."""))
    itunes = models.URLField(_("itunes store url"), blank=True,
        help_text=_("""Fill this out after saving this show and at least one
        episode. URL should look like:
        "http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewPodcast?id=000000000".
        See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more."""))

    twitter_tweet_prefix = models.CharField(_("Twitter tweet prefix"), max_length=80, help_text=_("""
        Enter a short ``tweet_text`` prefix for new episodes on this show."""), blank=True)

    objects = manager_from(ShowManager)
    tags = TaggableManager()

    class Meta:
        verbose_name = _("Show")
        verbose_name_plural = _("Shows")
        ordering = ("organization", "slug")

    def __unicode__(self):
        return u"%s" % (self.title)

    def save(self, **kwargs):
        self.updated = datetime.now()
        super(Show, self).save(**kwargs)

    def get_share_url(self):
        return "http://%s%s" % (Site.objects.get_current(), self.get_absolute_url())

    def get_absolute_url(self):
        return reverse("podcasting_show_detail", kwargs={"slug": self.slug})


class Episode(models.Model):
    """
    An individual podcast episode and it's unique attributes.
    """
    SIXTY_CHOICES = tuple((x, x) for x in range(60))
    uuid = UUIDField("ID", unique=True)

    created = models.DateTimeField(_("created"), default=datetime.now, editable=False)
    updated = models.DateTimeField(null=True, blank=True, editable=False)
    published = models.DateTimeField(null=True, blank=True, editable=False)

    show = models.ForeignKey(Show)

    enable_comments = models.BooleanField(default=True)

    author_text = models.CharField("author text", max_length=255, help_text=_("""
        The person or musician name(s) featured on this specific episode.
        The suggested format is: 'email@example.com (Full Name)' but 'Full Name' only, is acceptable.
        Multiple authors should be comma separated."""))

    title = models.CharField(_("title"), max_length=255)
    slug = AutoSlugField(_("slug"), populate_from="title")

    subtitle = models.CharField(_("subtitle"), max_length=255,
        help_text=_("Looks best if only a few words like a tagline."))

    description = models.TextField(_("description"), max_length=4000, help_text=_("""
        This is your chance to tell potential subscribers all about your podcast.
        Describe your subject matter, media format, episode schedule, and other
        relevant info so that they know what they'll be getting when they
        subscribe. In addition, make a list of the most relevant search terms
        that you want your podcast to match, then build them into your
        description. Note that iTunes removes podcasts that include lists of
        irrelevant words in the itunes:summary, description, or
        itunes:keywords tags. This field can be up to 4000 characters."""))
    tracklist = models.TextField(_("tracklist"), null=True, blank=True,
        help_text=_("""One track per line, machine will automatically add the numbers."""))

    tweet_text = models.CharField(_("tweet text"), max_length=140, editable=False)

    # iTunes specific fields
    original_image = models.ImageField(_("original image"), upload_to=get_episode_upload_folder,
        help_text=_("""An attractive, original square JPEG (.jpg) or PNG (.png)
        image of 300x300 pixles to 1000x1000 pixels at 72 pixels per inch. Image will be
        scaled down to 50x50 pixels at smallest in iTunes.<br /><br />
        For episode artwork to display in iTunes, image must be
        <a href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">
        saved to file's <strong>metadata</strong></a> before enclosure uploading!"""))

    if ImageSpec:
        admin_thumb_sm = ImageSpec([resize.Crop(50, 50)], image_field="original_image",
                                   pre_cache=True, options={"quality": 100})
        admin_thumb_lg = ImageSpec([resize.Crop(450, 450)], image_field="original_image",
                                   pre_cache=True, options={"quality": 100})
        img_episode_sm = ImageSpec([resize.Crop(120, 120)], image_field="original_image",
                                   pre_cache=True, options={"quality": 100})
        img_episode_lg = ImageSpec([resize.Crop(550, 550)], image_field="original_image",
                                   pre_cache=True, options={"quality": 100})
        img_itunes_sm = ImageSpec([resize.Crop(144, 144)], image_field="original_image",
                                  pre_cache=True, options={"quality": 100})
        img_itunes_lg = ImageSpec([resize.Crop(1000, 1000)], image_field="original_image",
                                  pre_cache=True, options={"quality": 100})

    hours = models.SmallIntegerField(_("hours"), max_length=2, default=0)
    minutes = models.SmallIntegerField(_("minutes"), max_length=2, default=0, choices=SIXTY_CHOICES)
    seconds = models.SmallIntegerField(_("seconds"), max_length=2, default=0, choices=SIXTY_CHOICES)
    keywords = models.CharField(_("keywords"), max_length=255,
        help_text=_("""A comma-delimited list of words for searches, up to 12;
        perhaps include misspellings."""))
    explicit = models.PositiveSmallIntegerField(_("explicit"), choices=Show.EXPLICIT_CHOICES,
        help_text=_("``Clean`` will put the clean iTunes graphic by it."), default=1)
    block = models.BooleanField(_("block"), default=False,
        help_text=_("""Check to block this episode from iTunes because <br />its
        content might cause the entire show to be <br />removed from iTunes."""))

    objects = manager_from(EpisodeManager)
    tags = TaggableManager()

    class Meta:
        verbose_name = _("Episode")
        verbose_name_plural = _("Episodes")
        ordering = ("-published", "slug")

    def __unicode__(self):
        return u"%s" % (self.title)

    def save(self, **kwargs):
        self.updated = datetime.now()
        super(Episode, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("podcasting_episode_detail", kwargs={"show_slug": self.show.slug, "slug": self.slug})

    def as_tweet(self):
        if not self.tweet_text:
            current_site = Site.objects.get_current()
            api_url = "http://api.tr.im/api/trim_url.json"
            u = urllib2.urlopen("%s?url=http://%s%s" % (
                api_url,
                current_site.domain,
                self.get_absolute_url(),
            ))
            result = json.loads(u.read())
            self.tweet_text = u"%s %s — %s" % (
                self.show.episode_twitter_tweet_prefix,
                self.title,
                result["url"],
            )
        return self.tweet_text

    def tweet(self):
        if can_tweet():
            account = twitter.Api(
                username=settings.TWITTER_USERNAME,
                password=settings.TWITTER_PASSWORD,
            )
            account.PostUpdate(self.as_tweet())
        else:
            raise ImproperlyConfigured("Unable to send tweet due to either "
                "missing python-twitter or required settings.")

    def seconds_total(self):
        try:
            return self.minutes * 60 + self.seconds
        except:
            return 0

    def get_share_url(self):
        return "http://%s%s" % (Site.objects.get_current(), self.get_absolute_url())

    def get_share_title(self):
        return self.title

    def get_share_description(self):
        return "%s..." % self.description[:512]


class Enclosure(models.Model):
    """
    An enclosure is one, of possibly many, files/filetypes of an episode.
    """
    MIME_CHOICES = (
        ("mp3", "audio/mpeg"),
    )

    episode = models.ForeignKey(Episode)

    url = models.URLField(_("url"),
        help_text=_("""URL of the media file. <br /> It is <strong>very</strong>
        important to remember that for episode artwork to display in iTunes, image must be
        <a href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">
        saved to file's <strong>metadata</strong></a> before enclosure uploading!<br /><br />
        For best results, choose an attractive, original square JPEG (.jpg) or PNG (.png)
        image of 300x300 pixels to 1000x1000 pixels at 72 pixels per inch. Image will be
        scaled down to 50x50 pixels at smallest in iTunes."""))

    size = models.PositiveIntegerField(_("size"), help_text=_("""The length attribute is the
        file size in bytes. Find this information in the files properties
        (on a Mac, ``Get Info`` and refer to the size row)"""))
    mime = models.CharField(_("mime format"), max_length=4, choices=MIME_CHOICES,
        default="mp3", help_text=_("Please contact support for a non mp3 filetype!"))
    bitrate = models.CharField(_("bit rate"), max_length=5, default="192",
        help_text=_("Measured in kilobits per second (kbps), often 128 or 192."))
    sample = models.CharField(_("sample rate"), max_length=5, default="44.1",
        help_text=_("Measured in kilohertz (kHz), often 44.1."))
    channel = models.CharField(_("channel"), max_length=1, default=2,
        help_text=_("Number of channels; 2 for stereo, 1 for mono."))

    class Meta:
        ordering = ("episode", "mime")
        unique_together = ("episode", "mime")
        verbose_name = _("Enclosure")
        verbose_name_plural = _("Enclosures")

    def __unicode__(self):
        return u"%s - %s" % (self.episode, self.mime)
