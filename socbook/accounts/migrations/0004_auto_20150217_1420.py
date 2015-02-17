# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150217_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='friends',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='friends_rel_+'),
            preserve_default=True,
        ),
    ]
