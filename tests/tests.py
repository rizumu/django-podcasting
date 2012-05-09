from django.test import TestCase
from django.core.urlresolvers import reverse

from milkman.dairy import milkman

from podcasting.models import Show, Episode, Enclosure


class DogTests(TestCase):
    def setUp(self):
        self.show = milkman.deliver(Show, title="snowprayers")
        self.episode = milkman.deliver(Episode, show=self.show, title="Episode 1")
        self.enclosure = milkman.deliver(Enclosure, episode=self.episode)

    def test_podcast(self):
        self.assertEquals(self.show, self.enclosure.episode.show)
        self.assertEquals(self.show.get_absolute_url(),
                          "/podcasts/snowprayers/")
        self.assertEquals(self.episode.get_absolute_url(),
                          "/podcasts/snowprayers/episode-1/")
