# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150217_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='url',
        ),
        migrations.AddField(
            model_name='profile',
            name='display_name',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
    ]
