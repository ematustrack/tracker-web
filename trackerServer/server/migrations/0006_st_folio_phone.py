# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20170805_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='st_folio',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]