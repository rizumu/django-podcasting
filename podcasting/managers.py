from django.db.models import Q
from django.db.models.query import QuerySet

from django.contrib.sites.models import Site


class EpisodeManager(QuerySet):
    """Returns public episodes that are currently activated."""

    def itunespublished(self):
        return self.get_queryset().exclude(Q(published=None) | Q(block=True))

    def published(self):
        return self.exclude(published=None)

    def onsite(self):
        return self.filter(shows__sites=Site.objects.get_current())

    def current(self):
        try:
            return self.published().order_by("-published")[0]
        except IndexError:
            return None


class ShowManager(QuerySet):
    """Returns shows that are on the current site."""

    def published(self):
        return self.exclude(published=None)

    def onsite(self):
        return self.filter(sites=Site.objects.get_current())
