# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 03:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0007_auto_20171106_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cf_id',
            field=models.CharField(blank=True, max_length=50, verbose_name='CF ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='loj_id',
            field=models.CharField(blank=True, max_length=50, verbose_name='LightOJ ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='timus_id',
            field=models.CharField(blank=True, max_length=50, verbose_name='Timus ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='uva_id',
            field=models.CharField(blank=True, max_length=50, verbose_name='UVa ID'),
        ),
        migrations.AddField(
            model_name='requestqueue',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='progress.UserProfile', unique=True),
        ),
    ]
