# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-06 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_subscription_peers'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='answer_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='comment_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='digest',
            field=models.CharField(choices=[('NEVER', 'Never'), ('DAILY', 'Daily'), ('WEEKLY', 'Weekly')], default='DAILY', max_length=6),
        ),
    ]
