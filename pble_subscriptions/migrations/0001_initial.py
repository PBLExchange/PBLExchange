# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-29 11:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pble_questions', '0001_initial'),
        ('pble_users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pble_questions.Question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_notifications', models.BooleanField(default=True)),
                ('comment_notifications', models.BooleanField(default=False)),
                ('digest', models.CharField(choices=[('NEVER', 'Never'), ('DAILY', 'Daily'), ('WEEKLY', 'Weekly')], default='DAILY', max_length=6)),
                ('categories', models.ManyToManyField(to='pble_questions.Category')),
                ('peers', models.ManyToManyField(to='pble_users.UserProfile')),
                ('tags', models.ManyToManyField(to='pble_questions.Tag')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
