# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_birthday'),
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationLike',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('author', models.ForeignKey(null=True, to='profiles.Profile')),
                ('publication', models.ForeignKey(related_name='likes', to='feeds.Publication')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='publication',
            name='visibility',
            field=models.SmallIntegerField(default=0, choices=[(0, 'Public'), (1, 'Private')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='publication',
            unique_together=set([]),
        ),
    ]
