# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-30 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='track_images'),
        ),
    ]
