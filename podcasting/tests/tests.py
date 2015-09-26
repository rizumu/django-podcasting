import factory

from django.test import TestCase

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings

from podcasting.models import Show, Episode, Enclosure

if 'licenses' in settings.INSTALLED_APPS:
    try:
        from licenses .models import License
    except ImportError:
        License = False
else:
    License = False


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site


if License:
    class LicenseFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = License


class ShowFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    if License:
        license = factory.SubFactory(LicenseFactory)

    class Meta:
        model = Show

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        else:
            site = SiteFactory.create()
            self.sites.add(site)


class EpisodeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Episode

    @factory.post_generation
    def shows(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for show in extracted:
                self.shows.add(show)


class EnclosureFactory(factory.django.DjangoModelFactory):
    size = 303
    duration = 909

    class Meta:
        model = Enclosure

    @factory.post_generation
    def episodes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for episode in extracted:
                self.episodes.add(episode)


class PodcastTests(TestCase):
    def setUp(self):
        self.show = ShowFactory.create(title="snowprayers")
        self.show.save()
        self.episodes = []
        for i in range(0, 10):
            episode = EpisodeFactory.create(shows=(self.show,), title="Episode 1")
            self.episodes.append(episode)
        self.episode = EpisodeFactory.create(shows=(self.show,), title="Episode")
        long_title = "".join(["x" for i in range(51)])
        self.long_episode1 = EpisodeFactory.create(shows=(self.show,), title=long_title)

        self.long_episode2 = EpisodeFactory.create(shows=(self.show,), title=long_title)

        self.enclosure = EnclosureFactory.create(episodes=(self.episodes[0],),)

    def test_podcast(self):
        self.assertEquals(self.show, self.enclosure.episodes.all()[0].shows.all()[0])

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
