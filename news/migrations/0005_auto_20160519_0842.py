# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20160519_0837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='releasenews',
            name='image_path',
        ),
        migrations.AddField(
            model_name='releasenews',
            name='release_path',
            field=models.ImageField(null=True, upload_to='uploads/pic', verbose_name='新闻图片'),
        ),
        migrations.AddField(
            model_name='releasenews',
            name='release_title',
            field=models.CharField(db_index=True, default='admin', max_length=200, verbose_name='新闻标题'),
            preserve_default=False,
        ),
    ]
