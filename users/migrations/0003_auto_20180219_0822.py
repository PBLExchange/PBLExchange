# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-19 08:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='points',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]