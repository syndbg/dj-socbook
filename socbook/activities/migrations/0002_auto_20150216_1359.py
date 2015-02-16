# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_birthday'),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('type', models.SmallIntegerField(choices=[(0, 'like'), (1, 'comment'), (2, 'befriendment'), (3, 'publication'), (4, 'profile post'), (5, 'deletetion')], default=0)),
                ('activity', models.ForeignKey(to='activities.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='other_activity',
            new_name='to_activity',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='publication',
            new_name='to_publication',
        ),
        migrations.AddField(
            model_name='activity',
            name='to_profile',
            field=models.ForeignKey(to='profiles.Profile', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='profile',
            field=models.ForeignKey(to='profiles.Profile', related_name='activities'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'like'), (1, 'comment'), (2, 'befriendment'), (3, 'publication'), (4, 'profile post'), (5, 'deletetion')], default=0),
            preserve_default=True,
        ),
    ]
