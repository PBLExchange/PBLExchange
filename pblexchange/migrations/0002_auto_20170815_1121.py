# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 11:21
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pblexchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pblexchange.Category'),
        ),
        migrations.AlterField(
            model_name='question',
            name='course',
            field=models.ManyToManyField(blank=True, null=True, to='pblexchange.Course'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(null=True, to='pblexchange.Tag'),
        ),
    ]
