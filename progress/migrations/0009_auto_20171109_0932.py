# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 03:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0008_auto_20171109_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestqueue',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='progress.UserProfile'),
        ),
    ]
