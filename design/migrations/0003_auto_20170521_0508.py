# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 05:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0002_auto_20170521_0229'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['code'], name='code_idx'),
        ),
    ]
