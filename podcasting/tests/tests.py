from django.test import TestCase

from milkman.dairy import milkman

from podcasting.models import Show, Episode, Enclosure


class PodcastTests(TestCase):
    def setUp(self):
        self.show = milkman.deliver(Show, title="snowprayers")
        self.show.save()
        self.episodes = []
        for i in range(0, 10):
            episode = milkman.deliver(Episode, show=self.show,
                                      title="Episode 1")
            episode.save()
            self.episodes.append(episode)
        self.episode = milkman.deliver(Episode, show=self.show, title="Episode")
        self.episode.save()
        long_title = "".join(["x" for i in range(51)])
        self.long_episode1 = milkman.deliver(Episode, show=self.show,
                                             title=long_title)
        self.long_episode1.save()

        self.long_episode2 = milkman.deliver(Episode, show=self.show,
                                             title=long_title)
        self.long_episode2.save()

        self.enclosure = milkman.deliver(Enclosure, episode=self.episodes[0])
        self.enclosure.save()

    def test_podcast(self):
        self.assertEquals(self.show, self.enclosure.episode.show)

    def test_autoslug(self):
        """Test normal slug generation. Slug has to be lower case."""
        self.assertEqual(self.episode.get_absolute_url(),
                         "/podcasts/snowprayers/episode/",
                         "Slug not generated as expected.")
        self.episode.save()
        self.assertEqual(self.episode.get_absolute_url(),
                         "/podcasts/snowprayers/episode/",
                         "Slug changed after additional episode.save()!")

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
                             "/podcasts/snowprayers/episode-1-{0}/".format(i + 1))

    def test_shortend_slug(self):
        """Test if slug get's shortened to max_length"""
        self.assertTrue(len(self.long_episode1.slug) == 50,
                        "Length of slug not <= 50 char!")
        self.assertTrue(len(self.long_episode2.slug) == 50,
                        "Length of slug not <= 50 char!")
        self.assertTrue(self.long_episode2.slug.endswith("-2"),
                        "Slug doesn't end with '-2' since same title does exist"
                        " in other episode already!")
