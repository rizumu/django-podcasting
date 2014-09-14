from django.views.generic import DetailView, ListView

from podcasting.conf import settings
from podcasting.models import Episode, Show


class ShowListView(ListView):

    paginate_by = settings.PODCASTING_PAGINATE_BY

    def get_queryset(self):
        return Show.objects.onsite()


class ShowDetailView(DetailView):
    def get_queryset(self):
        return Show.objects.onsite()


class EpisodeListView(ListView):

    paginate_by = settings.PODCASTING_PAGINATE_BY

    def get_queryset(self):
        return Episode.objects.published().filter(shows__slug=self.kwargs["show_slug"])


class EpisodeDetailView(DetailView):
    def get_queryset(self):
        return Episode.objects.published().filter(shows__slug=self.kwargs["show_slug"])
