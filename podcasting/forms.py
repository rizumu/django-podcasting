from datetime import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from podcasting.utils.twitter import can_tweet
from podcasting.utils.widgets import ThumbnailImageWidget
from podcasting.models import Enclosure, Episode, Show


class ShowForm(forms.ModelForm):

    original_image = forms.ImageField(widget=ThumbnailImageWidget,
        help_text=Show._meta.get_field("original_image").help_text)

    class Meta:
        model = Show
        fields = [
            "original_image",
            "title", "subtitle", "description",
            "twitter_tweet_prefix",
            "feedburner", "itunes",
            "keywords", "organization", "license",
            "explicit", "link", "authors",
        ]
        if "taggit" in settings.INSTALLED_APPS:
            fields.append("tags")


class EpisodeForm(forms.ModelForm):
    """ A partial episode form, for which the view inserts the show. """

    original_image = forms.ImageField(widget=ThumbnailImageWidget,
        help_text=Show._meta.get_field("original_image").help_text)

    class Meta:
        model = Episode
        fields = [
            "original_image", "authors",
            "title", "subtitle",
            "description", "keywords",
            "tracklist",
            "hours", "minutes", "seconds",
            "explicit", "block",
        ]
        if "taggit" in settings.INSTALLED_APPS:
            fields.append("tags")


class EnclosureForm(forms.ModelForm):

    class Meta:
        model = Enclosure
        fields = [
            "url", "mime", "size", "bitrate", "sample", "channel",
        ]

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove("episode") # allow checking against the missing attribute

        try:
            self.instance.validate_unique(exclude=exclude)
        except forms.ValidationError, e:
            self._update_errors(e.message_dict)


class AdminShowForm(forms.ModelForm):

    publish = forms.BooleanField(
        required = False,
        help_text = _("Checking this will publish this episode on the site, no turning back."),
    )

    class Meta:
        model = Show

    def __init__(self, *args, **kwargs):
        super(AdminShowForm, self).__init__(*args, **kwargs)
        self.fields["publish"].initial = bool(self.instance.published)

    def save(self):
        show = super(AdminShowForm, self).save(commit=False)

        if show.pk is None:
            if self.cleaned_data["publish"]:
                show.published = datetime.now()
        else:
            if Show.objects.filter(pk=show.pk, published=None).count():
                if self.cleaned_data["publish"]:
                    show.published = datetime.now()

        show.updated = datetime.now()
        show.save()

        return show


class AdminEpisodeForm(forms.ModelForm):

    publish = forms.BooleanField(
        required = False,
        help_text = _("Checking this will publish this episode on the site, no turning back."),
    )

    if can_tweet():
        tweet = forms.BooleanField(
            required = False,
            help_text = _("Checking this will send out a tweet announcing the episode."),
        )

    class Meta:
        model = Episode

    def __init__(self, *args, **kwargs):
        super(AdminEpisodeForm, self).__init__(*args, **kwargs)
        self.fields["publish"].initial = bool(self.instance.published)

    def save(self):
        episode = super(AdminEpisodeForm, self).save(commit=False)

        if episode.pk is None:
            if self.cleaned_data["publish"]:
                episode.published = datetime.now()
        else:
            if Episode.objects.filter(pk=episode.pk, published=None).count():
                if self.cleaned_data["publish"]:
                    episode.published = datetime.now()

        episode.updated = datetime.now()
        episode.save()

        if can_tweet() and self.cleaned_data["tweet"]:
            episode.tweet()

        return episode
