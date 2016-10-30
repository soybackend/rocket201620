# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-30 06:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RateTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='track',
            name='count_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ratetrack',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracks.Track'),
        ),
        migrations.AddField(
            model_name='ratetrack',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
