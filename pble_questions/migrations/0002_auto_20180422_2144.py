# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-22 21:44
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pble_questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='anonymous',
            field=models.BooleanField(verbose_name='anonymous'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='anonymous',
            field=models.BooleanField(verbose_name='anonymous'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='question',
            name='anonymous',
            field=models.BooleanField(verbose_name='anonymous'),
        ),
        migrations.AlterField(
            model_name='question',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pble_questions.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='question',
            name='course',
            field=models.ManyToManyField(blank=True, to='pble_questions.Course', verbose_name='course'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='pble_questions.Tag', verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=160, verbose_name='title'),
        ),
    ]
