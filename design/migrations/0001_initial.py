# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-20 14:43
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Convert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('input_data', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='인풋데이터')),
                ('results', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='결과데이터')),
            ],
            options={
                'verbose_name': '3D 모델 변환',
            },
        ),
        migrations.CreateModel(
            name='ModelNet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('thumbnail', models.FileField(upload_to='', verbose_name='썸네일')),
                ('class_info', models.PositiveSmallIntegerField(choices=[(0, '아무거나'), (1, '적어봄')], verbose_name='클래스')),
                ('fc_vector', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='인풋데이터')),
            ],
            options={
                'verbose_name': 'ModelNet 데이터',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP주소')),
            ],
            options={
                'verbose_name': '프로젝트',
            },
        ),
        migrations.AddField(
            model_name='convert',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='design.Project', verbose_name='프로젝트'),
        ),
    ]
