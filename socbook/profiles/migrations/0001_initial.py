# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('location', models.CharField(max_length=75, blank=True)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(to='profiles.Profile', related_name='friends_rel_+', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
