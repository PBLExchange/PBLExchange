# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-22 18:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pble_subscriptions', '0003_remove_subscription_digest_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answernotification',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='commentnotification',
            name='comment',
        ),
        migrations.DeleteModel(
            name='AnswerNotification',
        ),
        migrations.DeleteModel(
            name='CommentNotification',
        ),
    ]
