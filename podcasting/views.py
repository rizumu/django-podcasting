from django.views.generic import DetailView, ListView

from django.contrib.sites.shortcuts import get_current_site

from podcasting.conf import settings
from podcasting.models import Episode, Show


class ShowListView(ListView):

    paginate_by = settings.PODCASTING_PAGINATE_BY

    def get_queryset(self):
        site = get_current_site(self.request)
        return Show.objects.onsite(site=site)


class ShowDetailView(DetailView):
    def get_queryset(self):
        site = get_current_site(self.request)
        return Show.objects.onsite(site=site)


class EpisodeListView(ListView):

    paginate_by = settings.PODCASTING_PAGINATE_BY

    def get_queryset(self):
        return Episode.objects.published().filter(shows__slug=self.kwargs["show_slug"])


class EpisodeDetailView(DetailView):
    def get_queryset(self):
        return Episode.objects.published().filter(shows__slug=self.kwargs["show_slug"])
