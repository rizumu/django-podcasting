# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import podcasting.models
from django.conf import settings
import podcasting.utils.fields
from django.utils.translation import ugettext_lazy as _


def get_license_field():
    if 'licenses' in settings.INSTALLED_APPS:
        license = ('license', models.ForeignKey(to='licenses.License', verbose_name=_("license")))
    else:
        license = ('license', models.CharField(
           max_length=255,
           help_text=_("To publish a podcast to iTunes it is required to set a license type."))
        )
    return license

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmbedMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text='URL of the media file', verbose_name='url')),
            ],
            options={
                'ordering': ('episode', 'url'),
                'verbose_name': 'Embed Media URL',
                'verbose_name_plural': 'Embed Media URLs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enclosure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text='URL of the media file. <br /> It is <strong>very</strong>\n            important to remember that for episode artwork to display in iTunes, image must be\n            <a href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">\n            saved to file\'s <strong>metadata</strong></a> before enclosure uploading!<br /><br />\n            For best results, choose an attractive, original, and square JPEG (.jpg) or PNG (.png)\n            image at a size of 1400x1400 pixels. The image will be\n            scaled down to 50x50 pixels at smallest in iTunes.', verbose_name='url')),
                ('size', models.PositiveIntegerField(help_text='The length attribute is the file size in bytes. Find this information in the files properties (on a Mac, ``Get Info`` and refer to the size row)', verbose_name='size')),
                ('mime', models.CharField(help_text='Supports mime types of: aiff, flac, mp3, mp4, ogg, flac, wav', max_length=4, verbose_name='mime format', choices=[(b'aiff', b'audio/aiff'), (b'flac', b'audio/flac'), (b'mp3', b'audio/mpeg'), (b'mp4', b'audio/mp4'), (b'ogg', b'audio/ogg'), (b'flac', b'audio/flac'), (b'wav', b'audio/wav')])),
                ('bitrate', models.CharField(default=b'192', help_text='Measured in kilobits per second (kbps), often 128 or 192.', max_length=5, verbose_name='bit rate')),
                ('sample', models.CharField(default=b'44.1', help_text='Measured in kilohertz (kHz), often 44.1.', max_length=5, verbose_name='sample rate')),
                ('channel', models.CharField(default=2, help_text='Number of channels; 2 for stereo, 1 for mono.', max_length=1, verbose_name='channel')),
                ('duration', models.IntegerField(help_text='Duration of the audio file, in seconds (always as integer).', max_length=1, verbose_name='duration')),
            ],
            options={
                'ordering': ('episode', 'mime'),
                'verbose_name': 'Enclosure',
                'verbose_name_plural': 'Enclosures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', podcasting.utils.fields.UUIDField(verbose_name=b'ID', unique=True, max_length=36, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('published', models.DateTimeField(verbose_name='published', null=True, editable=False, blank=True)),
                ('enable_comments', models.BooleanField(default=True)),
                ('author_text', models.CharField(help_text="\n        The person or musician name(s) featured on this specific episode.\n        The suggested format is: 'email@example.com (Full Name)' but 'Full Name' only,\n        is acceptable. Multiple authors should be comma separated.", max_length=255, verbose_name='author text', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', autoslug.fields.AutoSlugField(verbose_name='slug', editable=False)),
                ('subtitle', models.CharField(help_text='Looks best if only a few words like a tagline.', max_length=255, verbose_name='subtitle', blank=True)),
                ('description', models.TextField(help_text="\n            This is your chance to tell potential subscribers all about your podcast.\n            Describe your subject matter, media format, episode schedule, and other\n            relevant info so that they know what they'll be getting when they\n            subscribe. In addition, make a list of the most relevant search terms\n            that you want your podcast to match, then build them into your\n            description. Note that iTunes removes podcasts that include lists of\n            irrelevant words in the itunes:summary, description, or\n            itunes:keywords tags. This field can be up to 4000 characters.", max_length=4000, verbose_name='description', blank=True)),
                ('tracklist', models.TextField(help_text='One track per line, machine will automatically add the numbers.', verbose_name='tracklist', blank=True)),
                ('tweet_text', models.CharField(verbose_name='tweet text', max_length=140, editable=False)),
                ('original_image', models.ImageField(help_text='\n            A podcast must have 1400 x 1400 pixel cover art in JPG or PNG\n            format using RGB color space. See our technical spec for\n            details. To be eligible for featuring on iTunes Stores,\n            choose an attractive, original, and square JPEG (.jpg) or\n            PNG (.png) image at a size of 1400x1400 pixels. The image\n            will be scaled down to 50x50 pixels at smallest in iTunes.\n            For reference see the <a\n            href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes\n            Podcast specs</a>.<br /><br /> For episode artwork to\n            display in iTunes, image must be <a\n            href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">\n            saved to file\'s <strong>metadata</strong></a> before\n            enclosure uploading!', upload_to=podcasting.models.get_episode_upload_folder, verbose_name='image', blank=True)),
                ('hours', models.SmallIntegerField(default=0, max_length=2, verbose_name='hours')),
                ('minutes', models.SmallIntegerField(default=0, max_length=2, verbose_name='minutes', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59)])),
                ('seconds', models.SmallIntegerField(default=0, max_length=2, verbose_name='seconds', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59)])),
                ('keywords', models.CharField(help_text='A comma-delimited list of words for searches, up to 12; perhaps include misspellings.', max_length=255, verbose_name='keywords', blank=True)),
                ('explicit', models.PositiveSmallIntegerField(default=1, help_text='``Clean`` will put the clean iTunes graphic by it.', verbose_name='explicit', choices=[(1, 'yes'), (2, 'no'), (3, 'clean')])),
                ('block', models.BooleanField(default=False, help_text='Check to block this episode from iTunes because <br />its content might cause the entire show to be <br />removed from iTunes.', verbose_name='block')),
            ],
            options={
                'ordering': ('-published', 'slug'),
                'verbose_name': 'Episode',
                'verbose_name_plural': 'Episodes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', podcasting.utils.fields.UUIDField(verbose_name='id', unique=True, max_length=36, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('published', models.DateTimeField(verbose_name='published', null=True, editable=False, blank=True)),
                ('ttl', models.PositiveIntegerField(default=1440, help_text='``Time to Live,`` the number of minutes a channel can be\n        cached before refreshing.', verbose_name='ttl')),
                ('editor_email', models.EmailField(help_text="Email address of the person responsible for the feed's content.", max_length=75, verbose_name='editor email', blank=True)),
                ('webmaster_email', models.EmailField(help_text='Email address of the person responsible for channel publishing.', max_length=75, verbose_name='webmaster email', blank=True)),
                ('organization', models.CharField(help_text='Name of the organization, company or Web site producing the podcast.', max_length=255, verbose_name='organization')),
                ('link', models.URLField(help_text='URL of either the main website or the\n        podcast section of the main website.', verbose_name='link')),
                ('enable_comments', models.BooleanField(default=True)),
                ('author_text', models.CharField(help_text="\n            This tag contains the name of the person or company that is most\n            widely attributed to publishing the Podcast and will be\n            displayed immediately underneath the title of the Podcast.\n            The suggested format is: 'email@example.com (Full Name)'\n            but 'Full Name' only, is acceptable. Multiple authors\n            should be comma separated.", max_length=255, verbose_name='author text')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', autoslug.fields.AutoSlugField(verbose_name='slug', editable=False)),
                ('subtitle', models.CharField(help_text='Looks best if only a few words, like a tagline.', max_length=255, verbose_name='subtitle')),
                ('on_itunes', models.BooleanField(default=True, help_text='Checked if the podcast is submitted to iTunes', verbose_name='iTunes')),
                ('description', models.TextField(help_text="\n            This is your chance to tell potential subscribers all about your\n            podcast. Describe your subject matter, media format,\n            episode schedule, and other relevant info so that they\n            know what they'll be getting when they subscribe. In\n            addition, make a list of the most relevant search terms\n            that you want yourp podcast to match, then build them into\n            your description. Note that iTunes removes podcasts that\n            include lists of irrelevant words in the itunes:summary,\n            description, or itunes:keywords tags. This field can be up\n            to 4000 characters.", max_length=4000, verbose_name='description')),
                ('original_image', models.ImageField(help_text='\n            A podcast must have 1400 x 1400 pixel cover art in JPG or PNG\n            format using RGB color space. See our technical spec for\n            details. To be eligible for featuring on iTunes Stores,\n            choose an attractive, original, and square JPEG (.jpg) or\n            PNG (.png) image at a size of 1400x1400 pixels. The image\n            will be scaled down to 50x50 pixels at smallest in iTunes.\n            For reference see the <a\n            href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes\n            Podcast specs</a>.<br /><br /> For episode artwork to\n            display in iTunes, image must be <a\n            href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">\n            saved to file\'s <strong>metadata</strong></a> before\n            enclosure uploading!', upload_to=podcasting.models.get_show_upload_folder, verbose_name='image', blank=True)),
                ('feedburner', models.URLField(help_text='Fill this out after saving this show and at least one\n            episode. URL should look like "http://feeds.feedburner.com/TitleOfShow".\n            See <a href="http://code.google.com/p/django-podcast/">documentation</a>\n            for more. <a href="http://www.feedburner.com/fb/a/ping">Manually ping</a>', verbose_name='feedburner url', blank=True)),
                ('explicit', models.PositiveSmallIntegerField(default=1, help_text='``Clean`` will put the clean iTunes graphic by it.', verbose_name='explicit', choices=[(1, 'yes'), (2, 'no'), (3, 'clean')])),
                ('redirect', models.URLField(help_text="The show's new URL feed if changing\n            the URL of the current show feed. Must continue old feed for at least\n            two weeks and write a 301 redirect for old feed.", verbose_name='redirect', blank=True)),
                ('keywords', models.CharField(help_text='A comma-demlimitedlist of up to 12 words for iTunes\n            searches. Perhaps include misspellings of the title.', max_length=255, verbose_name='keywords', blank=True)),
                ('itunes', models.URLField(help_text='Fill this out after saving this show and at least one\n            episode. URL should look like:\n            "http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewPodcast?id=000000000".\n            See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more.', verbose_name='itunes store url', blank=True)),
                ('twitter_tweet_prefix', models.CharField(help_text='Enter a short ``tweet_text`` prefix for new episodes on this show.', max_length=80, verbose_name='Twitter tweet prefix', blank=True)),
                ('owner', models.ForeignKey(related_name=b'podcast_shows', verbose_name='owner', to=settings.AUTH_USER_MODEL, help_text='Make certain the user account has a name and e-mail address.')),
                ('site', models.ForeignKey(verbose_name='Site', to='sites.Site')),
                get_license_field(),
            ],
            options={
                'ordering': ('organization', 'slug'),
                'verbose_name': 'Show',
                'verbose_name_plural': 'Shows',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='episode',
            name='show',
            field=models.ForeignKey(verbose_name='Podcast', to='podcasting.Show'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enclosure',
            name='episode',
            field=models.ForeignKey(verbose_name='episode', to='podcasting.Episode'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='enclosure',
            unique_together=set([('episode', 'mime')]),
        ),
        migrations.AddField(
            model_name='embedmedia',
            name='episode',
            field=models.ForeignKey(verbose_name='episode', to='podcasting.Episode'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='embedmedia',
            unique_together=set([('episode', 'url')]),
        ),
    ]
