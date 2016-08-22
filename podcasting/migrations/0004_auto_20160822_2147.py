# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasting', '0003_auto_20160822_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='description_pretty',
            field=models.TextField(help_text='May be longer than 4000 characters and contain HTML tags and styling.', verbose_name='pretty description', blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='description_pretty',
            field=models.TextField(help_text='May be longer than 4000 characters and contain HTML tags and styling.', verbose_name='pretty description', blank=True),
        ),
    ]
