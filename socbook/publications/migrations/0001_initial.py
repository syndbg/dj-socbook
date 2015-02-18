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
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('content', models.CharField(max_length=500, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.SmallIntegerField(choices=[(0, 'like'), (1, 'comment'), (2, 'article')], default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('to_publication', models.ForeignKey(to='publications.Publication', related_name='+', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
