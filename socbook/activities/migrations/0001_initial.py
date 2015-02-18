# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.SmallIntegerField(choices=[(0, 'like'), (1, 'comment'), (2, 'befriendment'), (3, 'publication'), (4, 'shared'), (5, 'register')], default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.SmallIntegerField(choices=[(0, 'public'), (1, 'friends'), (2, 'private')], default=1)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='activities')),
                ('to_account', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='foreign_activities', null=True)),
                ('to_publication', models.ForeignKey(to='publications.Publication', related_name='activities', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('type', models.SmallIntegerField(choices=[(0, 'like'), (1, 'comment'), (2, 'publication'), (3, 'shared'), (4, 'register'), (5, 'friend request acceptence'), (6, 'friend request transmission'), (7, 'friend request rejectection')], default=0)),
                ('activity', models.ForeignKey(null=True, to='activities.Activity')),
                ('from_account', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('publication', models.ForeignKey(null=True, to='publications.Publication')),
                ('to_account', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notifications')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
