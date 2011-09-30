from django.conf import settings
from django.db.models import Q

from django.contrib.sites.models import Site


class EpisodeManager(object):
    """Returns public episodes that are currently activated."""

    def itunespublished(self):
        return self.get_query_set().exclude(Q(published=None) | Q(block=True))

    def published(self):
        return self.exclude(published=None)

    def current(self):
        return self.published().order_by("-published")

    def onsite(self):
        return self.filter(site=Site.objects.get_current())


class ShowManager(object):
    """Returns shows that are on the current site."""

    def published(self):
        return self.exclude(published=None)

    def onsite(self):
        return self.filter(site=Site.objects.get_current())
