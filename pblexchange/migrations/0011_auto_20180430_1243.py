# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-30 12:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pblexchange', '0010_auto_20180430_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2018, 5, 14, 12, 43, 42, 439210, tzinfo=utc)),
        ),
    ]
