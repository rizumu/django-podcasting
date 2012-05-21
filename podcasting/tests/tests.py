from django.test import TestCase
from django.core.urlresolvers import reverse

from milkman.dairy import milkman

from podcasting.models import Show, Episode, Enclosure


class PodcastTests(TestCase):
    def setUp(self):
        self.show = milkman.deliver(Show, title="snowprayers")
        self.show.save()
        self.episodes = []
        for i in range(0, 10):
            episode = milkman.deliver(Episode, show=self.show, title="Episode 1")
            episode.save()
            self.episodes.append(episode)

        self.enclosure = milkman.deliver(Enclosure, episode=self.episodes[0])
        self.enclosure.save()

    def test_podcast(self):
        self.assertEquals(self.show, self.enclosure.episode.show)

    def test_slug_append_int_if_already_exists(self):
        """Test that the slug is created properly
        If the slug already exists a '-incremented int' is appended.
        """
        self.assertEquals(self.show.get_absolute_url(),
                          "/podcasts/snowprayers/")
        self.assertEquals(self.episodes[0].get_absolute_url(),
                          "/podcasts/snowprayers/episode-1/")

        for i in range(1, 10):
            self.assertEqual(self.episodes[i].get_absolute_url(),
                             "/podcasts/snowprayers/episode-1-{0}/".format(i+1)
            )

