# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_auto_20150215_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicationcomment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='publicationcomment',
            name='publication',
        ),
        migrations.DeleteModel(
            name='PublicationComment',
        ),
        migrations.RemoveField(
            model_name='publicationlike',
            name='author',
        ),
        migrations.RemoveField(
            model_name='publicationlike',
            name='publication',
        ),
        migrations.DeleteModel(
            name='PublicationLike',
        ),
    ]
