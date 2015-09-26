from __future__ import unicode_literals

import json
import os

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.sites.models import Site

from autoslug import AutoSlugField
from model_utils.managers import PassThroughManager

from podcasting.managers import EpisodeManager, ShowManager
from podcasting.utils.fields import UUIDField
from podcasting.utils.twitter import can_tweet

# optional external dependencies
try:
    from licenses.models import License
except:
    License = None

try:
    from imagekit.models import ImageSpecField
    from imagekit.processors import ResizeToFill
except ImportError:
    ResizeToFill = ImageSpecField = None

try:
    from easy_thumbnails.fields import ThumbnailerImageField as ImageField
    custom_image_field = True
except ImportError:
    custom_image_field = False

if not custom_image_field:
    try:
        from sorl.thumbnail import ImageField  # noqa
        custom_image_field = True
    except ImportError:
        custom_image_field = False

if not custom_image_field:
    # image-kit uses the standard ImageField as well
    from django.db.models import ImageField  # noqa

if "taggit" in settings.INSTALLED_APPS:
    from taggit.managers import TaggableManager
else:
    def TaggableManager(blank=True):  # noqa
        return None
try:
    import twitter
except ImportError:
    twitter = None  # noqa

try:
    from embed_video.fields import EmbedVideoField
except ImportError:
    EmbedVideoField = None


def get_show_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return "{0}/podcasts/{1}/{2}{3}".format(
        settings.PODCASTING_IMG_PATH, instance.slug, slugify(root), ext
    )


def get_episode_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    if instance.shows.count() == 1:
        return "{0}/podcasts/{1}/episodes/{2}{3}".format(
            settings.PODCASTING_IMG_PATH, instance.shows.all()[0].slug, slugify(root), ext
        )
    else:
        return "{0}/podcasts/episodes/{1}/{2}{3}".format(
            settings.PODCASTING_IMG_PATH, instance.slug, slugify(root), ext
        )


@python_2_unicode_compatible
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

    created = models.DateTimeField(_("created"), auto_now_add=True, editable=False)
    updated = models.DateTimeField(_("updated"), auto_now=True, editable=False)
    published = models.DateTimeField(_("published"), null=True, blank=True, editable=False)

    sites = models.ManyToManyField(Site, verbose_name=_('Sites'))

    ttl = models.PositiveIntegerField(
        _("ttl"), default=1440,
        help_text=_("""``Time to Live,`` the number of minutes a channel can be
        cached before refreshing."""))

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="podcast_shows",
        verbose_name=_("owner"),
        help_text=_("""Make certain the user account has a name and e-mail address."""))

    editor_email = models.EmailField(
        _("editor email"), blank=True,
        help_text=_("Email address of the person responsible for the feed's content."))
    webmaster_email = models.EmailField(
        _("webmaster email"), blank=True,
        help_text=_("Email address of the person responsible for channel publishing."))

    if 'licenses' in settings.INSTALLED_APPS:
        license = models.ForeignKey(License, verbose_name=_("license"))
    else:
        license = models.CharField(
            _("license"), max_length=255,
            help_text=_("To publish a podcast to iTunes it is required to set a license type."))

    organization = models.CharField(
        _("organization"), max_length=255,
        help_text=_("Name of the organization, company or Web site producing the podcast."))
    link = models.URLField(_("link"), help_text=_("""URL of either the main website or the
        podcast section of the main website."""))

    enable_comments = models.BooleanField(default=True)

    author_text = models.CharField(
        _("author text"), max_length=255, help_text=_("""
            This tag contains the name of the person or company that is most
            widely attributed to publishing the Podcast and will be
            displayed immediately underneath the title of the Podcast.
            The suggested format is: 'email@example.com (Full Name)'
            but 'Full Name' only, is acceptable. Multiple authors
            should be comma separated."""))

    title = models.CharField(_("title"), max_length=255)
    slug = AutoSlugField(_("slug"), populate_from="title", unique="True")

    subtitle = models.CharField(
        _("subtitle"), max_length=255,
        help_text=_("Looks best if only a few words, like a tagline."))

    # If the show is not on iTunes, many fields may be ignored in your user forms
    on_itunes = models.BooleanField(
        _("iTunes"), default=True,
        help_text=_("Checked if the podcast is submitted to iTunes"))

    description = models.TextField(
        _("description"), max_length=4000, help_text=_("""
            This is your chance to tell potential subscribers all about your
            podcast. Describe your subject matter, media format,
            episode schedule, and other relevant info so that they
            know what they'll be getting when they subscribe. In
            addition, make a list of the most relevant search terms
            that you want yourp podcast to match, then build them into
            your description. Note that iTunes removes podcasts that
            include lists of irrelevant words in the itunes:summary,
            description, or itunes:keywords tags. This field can be up
            to 4000 characters."""))

    original_image = ImageField(
        _("image"), upload_to=get_show_upload_folder, blank=True, help_text=_("""
            A podcast must have 1400 x 1400 pixel cover art in JPG or PNG
            format using RGB color space. See our technical spec for
            details. To be eligible for featuring on iTunes Stores,
            choose an attractive, original, and square JPEG (.jpg) or
            PNG (.png) image at a size of 1400x1400 pixels. The image
            will be scaled down to 50x50 pixels at smallest in iTunes.
            For reference see the <a
            href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes
            Podcast specs</a>.<br /><br /> For episode artwork to
            display in iTunes, image must be <a
            href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">
            saved to file's <strong>metadata</strong></a> before
            enclosure uploading!"""))

    if ResizeToFill:
        admin_thumb_sm = ImageSpecField(source="original_image",
                                        processors=[ResizeToFill(50, 50)],
                                        options={"quality": 100})
        admin_thumb_lg = ImageSpecField(source="original_image",
                                        processors=[ResizeToFill(450, 450)],
                                        options={"quality": 100})
        img_show_sm = ImageSpecField(source="original_image",
                                     processors=[ResizeToFill(120, 120)],
                                     options={"quality": 100})
        img_show_lg = ImageSpecField(source="original_image",
                                     processors=[ResizeToFill(550, 550)],
                                     options={"quality": 100})
        img_itunes_sm = ImageSpecField(source="original_image",
                                       processors=[ResizeToFill(144, 144)],
                                       options={"quality": 100})
        img_itunes_lg = ImageSpecField(source="original_image",
                                       processors=[ResizeToFill(1400, 1400)],
                                       options={"quality": 100})

    feedburner = models.URLField(
        _("feedburner url"), blank=True,
        help_text=_("""Fill this out after saving this show and at least one
            episode. URL should look like "http://feeds.feedburner.com/TitleOfShow".
            See <a href="http://code.google.com/p/django-podcast/">documentation</a>
            for more. <a href="http://www.feedburner.com/fb/a/ping">Manually ping</a>"""))

    # iTunes specific fields
    explicit = models.PositiveSmallIntegerField(
        _("explicit"), default=1, choices=EXPLICIT_CHOICES,
        help_text=_("``Clean`` will put the clean iTunes graphic by it."))
    redirect = models.URLField(
        _("redirect"), blank=True,
        help_text=_("""The show's new URL feed if changing
            the URL of the current show feed. Must continue old feed for at least
            two weeks and write a 301 redirect for old feed."""))
    keywords = models.CharField(
        _("keywords"), max_length=255, blank=True,
        help_text=_("""A comma-demlimitedlist of up to 12 words for iTunes
            searches. Perhaps include misspellings of the title."""))
    itunes = models.URLField(
        _("itunes store url"), blank=True,
        help_text=_("""Fill this out after saving this show and at least one
            episode. URL should look like:
            "http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewPodcast?id=000000000".
            See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more."""))

    twitter_tweet_prefix = models.CharField(
        _("Twitter tweet prefix"), max_length=80,
        help_text=_("Enter a short ``tweet_text`` prefix for new episodes on this show."),
        blank=True)

    objects = PassThroughManager.for_queryset_class(ShowManager)()
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("Show")
        verbose_name_plural = _("Shows")
        ordering = ("organization", "slug")

    def __str__(self):
        return self.title

    def get_share_url(self):
        return "http://{0}{1}".format(Site.objects.get_current(), self.get_absolute_url())

    def get_absolute_url(self):
        return reverse("podcasting_show_detail", kwargs={"slug": self.slug})

    @property
    def current_episode(self):
        try:
            return self.episode_set.published().order_by("-published")[0]
        except IndexError:
            return None


@python_2_unicode_compatible
class Episode(models.Model):
    """
    An individual podcast episode and it's unique attributes.
    """
    SIXTY_CHOICES = tuple((x, x) for x in range(60))
    uuid = UUIDField("ID", unique=True)

    created = models.DateTimeField(_("created"), auto_now_add=True, editable=False)
    updated = models.DateTimeField(_("updated"), auto_now=True, editable=False)
    published = models.DateTimeField(_("published"), null=True, blank=True, editable=False)

    shows = models.ManyToManyField(Show, verbose_name=_("Podcasts"))

    enable_comments = models.BooleanField(default=True)

    author_text = models.CharField(_("author text"), max_length=255, blank=True, help_text=_("""
        The person or musician name(s) featured on this specific episode.
        The suggested format is: 'email@example.com (Full Name)' but 'Full Name' only,
        is acceptable. Multiple authors should be comma separated."""))

    title = models.CharField(_("title"), max_length=255)
    slug = AutoSlugField(_("slug"), populate_from="title", unique="True")

    subtitle = models.CharField(
        _("subtitle"), max_length=255, blank=True,
        help_text=_("Looks best if only a few words like a tagline."))

    description = models.TextField(
        _("description"), max_length=4000, blank=True, help_text=_("""
            This is your chance to tell potential subscribers all about your podcast.
            Describe your subject matter, media format, episode schedule, and other
            relevant info so that they know what they'll be getting when they
            subscribe. In addition, make a list of the most relevant search terms
            that you want your podcast to match, then build them into your
            description. Note that iTunes removes podcasts that include lists of
            irrelevant words in the itunes:summary, description, or
            itunes:keywords tags. This field can be up to 4000 characters."""))
    tracklist = models.TextField(
        _("tracklist"), blank=True,
        help_text=_("""One track per line, machine will automatically add the numbers."""))

    tweet_text = models.CharField(_("tweet text"), max_length=140, editable=False)

    original_image = ImageField(
        _("image"), upload_to=get_episode_upload_folder, blank=True, help_text=_("""
            A podcast must have 1400 x 1400 pixel cover art in JPG or PNG
            format using RGB color space. See our technical spec for
            details. To be eligible for featuring on iTunes Stores,
            choose an attractive, original, and square JPEG (.jpg) or
            PNG (.png) image at a size of 1400x1400 pixels. The image
            will be scaled down to 50x50 pixels at smallest in iTunes.
            For reference see the <a
            href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes
            Podcast specs</a>.<br /><br /> For episode artwork to
            display in iTunes, image must be <a
            href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">
            saved to file's <strong>metadata</strong></a> before
            enclosure uploading!"""))

    if ImageSpecField:
        admin_thumb_sm = ImageSpecField(source="original_image",
                                        processors=[ResizeToFill(50, 50)],
                                        options={"quality": 100})
        admin_thumb_lg = ImageSpecField(source="original_image",
                                        processors=[ResizeToFill(450, 450)],
                                        options={"quality": 100})
        img_episode_sm = ImageSpecField(source="original_image",
                                        processors=[ResizeToFill(120, 120)],
                                        options={"quality": 100})
        img_episode_lg = ImageSpecField(source="original_image",
                                        processors=[ResizeToFill(550, 550)],
                                        options={"quality": 100})
        img_itunes_sm = ImageSpecField(source="original_image",
                                       processors=[ResizeToFill(144, 144)],
                                       options={"quality": 100})
        img_itunes_lg = ImageSpecField(source="original_image",
                                       processors=[ResizeToFill(1400, 1400)],
                                       options={"quality": 100})

    # iTunes specific fields
    hours = models.SmallIntegerField(_("hours"), default=0)
    minutes = models.SmallIntegerField(_("minutes"), default=0, choices=SIXTY_CHOICES)
    seconds = models.SmallIntegerField(_("seconds"), default=0, choices=SIXTY_CHOICES)
    keywords = models.CharField(
        _("keywords"), max_length=255, blank=True,
        help_text=_("A comma-delimited list of words for searches, up to 12; "
                    "perhaps include misspellings."))
    explicit = models.PositiveSmallIntegerField(
        _("explicit"), choices=Show.EXPLICIT_CHOICES,
        help_text=_("``Clean`` will put the clean iTunes graphic by it."), default=1)
    block = models.BooleanField(
        _("block"), default=False,
        help_text=_("Check to block this episode from iTunes because <br />its "
                    "content might cause the entire show to be <br />removed from iTunes."""))

    objects = PassThroughManager.for_queryset_class(EpisodeManager)()
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("Episode")
        verbose_name_plural = _("Episodes")
        ordering = ("-published", "slug")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("podcasting_episode_detail",
                       kwargs={"show_slug": self.shows.all()[0].slug, "slug": self.slug})

    def as_tweet(self):
        if not self.tweet_text:
            current_site = Site.objects.get_current()
            api_url = "http://api.tr.im/api/trim_url.json"
            u = urlopen("{0}?url=http://{1}{2}".format(
                api_url,
                current_site.domain,
                self.get_absolute_url(),
            ))
            result = json.loads(u.read())
            self.tweet_text = "{0} {1} - {2}".format(
                self.shows.all()[0].episode_twitter_tweet_prefix,
                self.title,
                result["url"],
            )
        return self.tweet_text

    def tweet(self):
        if can_tweet():
            account = twitter.Api(
                username=settings.TWITTER_USERNAME,
                password=settings.TWITTER_PASSWORD)
            account.PostUpdate(self.as_tweet())
        else:
            raise ImproperlyConfigured(
                "Unable to send tweet due to either "
                "missing python-twitter or required settings.")

    def seconds_total(self):
        try:
            return self.minutes * 60 + self.seconds
        except:
            return 0

    def get_share_url(self):
        return "http://{0}{1}".format(Site.objects.get_current(), self.get_absolute_url())

    def get_share_title(self):
        return self.title

    def get_share_description(self):
        return "{0}...".format(self.description[:512])

    def is_show_published(self):
        for show in self.shows.all():
            if show.published:
                return True
        return False


@python_2_unicode_compatible
class Enclosure(models.Model):
    """
    An enclosure is one, of possibly many, files/filetypes of an episode.
    """
    try:
        MIME_CHOICES = settings.PODCASTING_MIME_CHOICES
    except AttributeError:
        MIME_CHOICES = (
            ("aiff", "audio/aiff"),
            ("flac", "audio/flac"),
            ("mp3", "audio/mpeg"),
            ("mp4", "audio/mp4"),
            ("ogg", "audio/ogg"),
            ("flac", "audio/flac"),
            ("wav", "audio/wav"),
        )

    episodes = models.ManyToManyField(Episode, verbose_name=_("Episodes"))

    url = models.URLField(
        _("url"),
        help_text=_("""URL of the media file. <br /> It is <strong>very</strong>
            important to remember that for episode artwork to display in iTunes, image must be
            <a href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">
            saved to file's <strong>metadata</strong></a> before enclosure uploading!<br /><br />
            For best results, choose an attractive, original, and square JPEG (.jpg) or PNG (.png)
            image at a size of 1400x1400 pixels. The image will be
            scaled down to 50x50 pixels at smallest in iTunes."""))

    size = models.PositiveIntegerField(
        _("size"), help_text=_("The length attribute is the file size in bytes. "
                               "Find this information in the files properties "
                               "(on a Mac, ``Get Info`` and refer to the size row)"))
    mime = models.CharField(
        _("mime format"), max_length=4, choices=MIME_CHOICES,
        help_text=_("Supports mime types of: {0}".format(
            ", ".join([mime[0] for mime in MIME_CHOICES]))))
    bitrate = models.CharField(
        _("bit rate"), max_length=5, default="192",
        help_text=_("Measured in kilobits per second (kbps), often 128 or 192."))
    sample = models.CharField(
        _("sample rate"), max_length=5, default="44.1",
        help_text=_("Measured in kilohertz (kHz), often 44.1."))
    channel = models.CharField(
        _("channel"), max_length=1, default=2,
        help_text=_("Number of channels; 2 for stereo, 1 for mono."))
    duration = models.IntegerField(
        _("duration"),
        help_text=_("Duration of the audio file, in seconds (always as integer)."))

    class Meta:
        ordering = ("url", "mime",)
        verbose_name = _("Enclosure")
        verbose_name_plural = _("Enclosures")

    def __str__(self):
        return "{0} - {1}".format(self.url, self.mime)


@python_2_unicode_compatible
class EmbedMedia(models.Model):
    """
    Associate a media URL to an Episode.

    This is *not* a replacement for a video podcast, but simply a way
    to embed content via url in an episode description.

    Ideally this will be used with django-embed-video which supports
    easy embeding for YouTube and Vimeo videos and music from SoundCloud.
    """
    episode = models.ForeignKey(Episode, verbose_name=_("episode"))

    if EmbedVideoField:
        url = EmbedVideoField(_("url"), help_text=_("URL of the media file"))
    else:
        url = models.URLField(_("url"), help_text=_("URL of the media file"))

    class Meta:
        ordering = ("episode", "url")
        unique_together = ("episode", "url")
        verbose_name = _("Embed Media URL")
        verbose_name_plural = _("Embed Media URLs")

    def __str__(self):
        return "{0} - {1}".format(self.episode, self.url)
