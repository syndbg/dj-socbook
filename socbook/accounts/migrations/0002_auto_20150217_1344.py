# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Rejected')])),
                ('from_account', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='friend_requests_sent')),
                ('to_account', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='friend_requests_received')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('url', models.URLField()),
                ('account', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together=set([('from_account', 'to_account')]),
        ),
        migrations.AddField(
            model_name='account',
            name='birthday',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='friends',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True, related_name='friends_rel_+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='location',
            field=models.CharField(max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='site',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='email address', unique=True, blank=True),
            preserve_default=True,
        ),
    ]
