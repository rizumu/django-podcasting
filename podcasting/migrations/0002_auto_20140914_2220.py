# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from autoslug import AutoSlugField

def move_enclosure_episode(apps, schema_editor):
  Enclosure = apps.get_model('podcasting', 'Enclosure')
  Episode = apps.get_model('podcasting', 'Episode')
  for enclosure_item in Enclosure.objects.all():
      episode = Episode.objects.get(id=enclosure_item.episode)
      enclosure_item.episodes.add(episode)
      enclosure_item.save()

def move_show_site(apps, schema_editor):
  Site = apps.get_model('sites', 'Site')
  Show = apps.get_model('podcasting', 'Show')
  for show_item in Show.objects.all():
      site_item = Site.objects.get(id=show_item.site)
      show_item.sites.add(site_item)
      show_item.save()

def move_episode_show(apps, schema_editor):
  Episode = apps.get_model('podcasting', 'Episode')
  Show = apps.get_model('podcasting', 'Show')
  for episode_item in Episode.objects.all():
      show_item = Show.objects.get(id=episode_item.show)
      episode_item.shows.add(show_item)
      episode_item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('podcasting', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enclosure',
            options={'ordering': ('url', 'mime'), 'verbose_name': 'Enclosure', 'verbose_name_plural': 'Enclosures'},
        ),
        migrations.AddField(
            model_name='enclosure',
            name='episodes',
            field=models.ManyToManyField(to='podcasting.Episode', verbose_name='Episodes'),
            preserve_default=True,
        ),        
        migrations.AddField(
            model_name='episode',
            name='shows',
            field=models.ManyToManyField(to='podcasting.Show', verbose_name='Podcasts'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='show',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', verbose_name='Sites'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='episode',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='episode',
            name='show',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='show',
            name='site',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='enclosure',
            unique_together=None,
        ),
        migrations.AlterField(
            model_name='episode',
            name='slug',
            field=AutoSlugField(verbose_name='slug', unique=b'True', editable=False),
        ),
        migrations.AlterField(
            model_name='show',
            name='slug',
            field=AutoSlugField(verbose_name='slug', unique=b'True', editable=False),
        ),

        migrations.RunPython(move_enclosure_episode),

        migrations.RunPython(move_show_site),

        migrations.RunPython(move_episode_show),

        migrations.RemoveField(
            model_name='enclosure',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='episode',
            name='show',
        ),
        migrations.RemoveField(
            model_name='show',
            name='site',
        ),
    ]
