# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 18:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_st_folio_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='pro',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
