# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-13 10:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181113_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_approved',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(blank=True, choices=[(1, 'HR'), (2, 'MANAGER'), (3, 'REGULAR')], null=True),
        ),
    ]
