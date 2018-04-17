# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-10 12:21
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pblexchange', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('url', models.URLField(validators=[django.core.validators.URLValidator])),
            ],
        ),
    ]