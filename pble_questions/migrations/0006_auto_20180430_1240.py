# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-30 12:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pble_questions', '0005_auto_20180430_1220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='featuredcategory',
            old_name='text',
            new_name='text_dk',
        ),
        migrations.AddField(
            model_name='featuredcategory',
            name='text_en',
            field=models.CharField(default=django.utils.timezone.now, max_length=128),
            preserve_default=False,
        ),
    ]