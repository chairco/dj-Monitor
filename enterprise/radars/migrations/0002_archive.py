# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=50, null=True, verbose_name='url')),
                ('content', models.TextField(max_length=100000, null=True, verbose_name='content')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Archive',
                'verbose_name_plural': 'Archives',
                'ordering': ['-created_at'],
            },
        ),
    ]