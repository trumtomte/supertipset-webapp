# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-26 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ManyToManyField(to='api.Team'),
        ),
    ]
