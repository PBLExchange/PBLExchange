# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-01 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pble_questions', '0011_category_da_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='da_name',
            field=models.CharField(max_length=160, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='en_name',
            field=models.CharField(max_length=160, unique=True),
        ),
    ]