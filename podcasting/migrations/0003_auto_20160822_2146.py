# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields
import autoslug.fields
import podcasting.models
import taggit.managers
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('podcasting', '0002_auto_20140914_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='show',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='embedmedia',
            name='url',
            field=embed_video.fields.EmbedVideoField(help_text='URL of the media file', verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='duration',
            field=models.IntegerField(help_text='Duration of the audio file, in seconds (always as integer).', verbose_name='duration'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='hours',
            field=models.SmallIntegerField(default=0, verbose_name='hours'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='minutes',
            field=models.SmallIntegerField(default=0, verbose_name='minutes', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59)]),
        ),
        migrations.AlterField(
            model_name='episode',
            name='original_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(help_text='\n            A podcast must have 1400 x 1400 pixel cover art in JPG or PNG\n            format using RGB color space. See our technical spec for\n            details. To be eligible for featuring on iTunes Stores,\n            choose an attractive, original, and square JPEG (.jpg) or\n            PNG (.png) image at a size of 1400x1400 pixels. The image\n            will be scaled down to 50x50 pixels at smallest in iTunes.\n            For reference see the <a\n            href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes\n            Podcast specs</a>.<br /><br /> For episode artwork to\n            display in iTunes, image must be <a\n            href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">\n            saved to file\'s <strong>metadata</strong></a> before\n            enclosure uploading!', upload_to=podcasting.models.get_episode_upload_folder, verbose_name='image', blank=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='seconds',
            field=models.SmallIntegerField(default=0, verbose_name='seconds', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59)]),
        ),
        migrations.AlterField(
            model_name='episode',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique='True', verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='show',
            name='editor_email',
            field=models.EmailField(help_text="Email address of the person responsible for the feed's content.", max_length=254, verbose_name='editor email', blank=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='original_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(help_text='\n            A podcast must have 1400 x 1400 pixel cover art in JPG or PNG\n            format using RGB color space. See our technical spec for\n            details. To be eligible for featuring on iTunes Stores,\n            choose an attractive, original, and square JPEG (.jpg) or\n            PNG (.png) image at a size of 1400x1400 pixels. The image\n            will be scaled down to 50x50 pixels at smallest in iTunes.\n            For reference see the <a\n            href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes\n            Podcast specs</a>.<br /><br /> For episode artwork to\n            display in iTunes, image must be <a\n            href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">\n            saved to file\'s <strong>metadata</strong></a> before\n            enclosure uploading!', upload_to=podcasting.models.get_show_upload_folder, verbose_name='image', blank=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique='True', verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='show',
            name='webmaster_email',
            field=models.EmailField(help_text='Email address of the person responsible for channel publishing.', max_length=254, verbose_name='webmaster email', blank=True),
        ),
    ]
