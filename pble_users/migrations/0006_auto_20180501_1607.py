# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-01 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pble_users', '0005_auto_20180501_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='language',
            field=models.CharField(choices=[('en-gb', 'English'), ('da', 'Danish')], default='en-gb', max_length=4, verbose_name='language'),
        ),
    ]
