# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-01 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pble_questions', '0010_auto_20180501_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='da_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=160),
            preserve_default=False,
        ),
    ]