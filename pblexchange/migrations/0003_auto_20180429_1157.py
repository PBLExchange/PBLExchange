# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-29 11:57
from __future__ import unicode_literals

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pblexchange', '0002_auto_20180429_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2018, 5, 13, 11, 57, 45, 886914, tzinfo=utc)),
        ),
    ]
