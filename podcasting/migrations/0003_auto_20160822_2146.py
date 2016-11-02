# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('podcasting', '0002_auto_20140914_2220'),
    ]

    operations = [
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
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique='True', verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='show',
            name='webmaster_email',
            field=models.EmailField(help_text='Email address of the person responsible for channel publishing.', max_length=254, verbose_name='webmaster email', blank=True),
        ),
    ]
