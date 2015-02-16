# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20150216_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='content',
            field=models.CharField(max_length=500, blank=True, default=''),
            preserve_default=True,
        ),
    ]
