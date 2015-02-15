# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125)),
                ('content', models.TextField(max_length=500)),
                ('author', models.ForeignKey(to='profiles.Profile', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='profiles.Profile', null=True)),
                ('publication', models.ForeignKey(related_name='comments', to='feeds.Publication')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='publication',
            unique_together=set([('author', 'title')]),
        ),
    ]
