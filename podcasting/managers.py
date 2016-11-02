from django.db.models import Q
from django.db.models.query import QuerySet

from django.contrib.sites.models import Site


class EpisodeQuerySet(QuerySet):
    """Returns public episodes that are currently activated."""

    def itunespublished(self):
        return self.get_queryset().exclude(Q(published=None) | Q(block=True))

    def published(self):
        return self.exclude(published=None)

    def onsite(self, site=None):
        if not site:
            site = Site.objects.get_current()
        return self.filter(shows__sites__name=site.name).distinct()

    def current(self):
        try:
            return self.published().order_by("-published")[0]
        except IndexError:
            return None


class ShowQuerySet(QuerySet):
    """Returns shows that are on the current site."""

    def published(self):
        return self.exclude(published=None)

    def onsite(self, site=None):
        if not site:
            site = Site.objects.get_current()
        return self.filter(sites__name=site.name).distinct()
