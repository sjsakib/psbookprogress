# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 04:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0005_auto_20171105_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dtype', models.CharField(max_length=10)),
                ('value', models.CharField(max_length=200)),
            ],
        ),
    ]
