# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0003_auto_20150216_0139'),
        ('profiles', '0003_profile_birthday'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('type', models.SmallIntegerField(choices=[(0, 'Like'), (1, 'Comment')], default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('content', models.TextField(blank=True, max_length=500, default='')),
                ('other_activity', models.ForeignKey(to='activities.Activity', null=True)),
                ('profile', models.ForeignKey(to='profiles.Profile')),
                ('publication', models.ForeignKey(to='feeds.Publication', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
