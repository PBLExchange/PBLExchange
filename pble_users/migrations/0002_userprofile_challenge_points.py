# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-30 03:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pble_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='challenge_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
