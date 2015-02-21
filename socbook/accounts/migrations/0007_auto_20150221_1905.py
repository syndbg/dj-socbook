# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150221_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(verbose_name='email address', blank=True, help_text='The email you will use to login and restore your password if forgotten.', unique=True, max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(blank=True, help_text='The <display_name> that will be used in the URL to reach this profile.', max_length=100),
            preserve_default=True,
        ),
    ]
