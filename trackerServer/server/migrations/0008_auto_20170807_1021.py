# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 10:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_pro_phone'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='st_folio',
            unique_together=set([('idST', 'idFolio', 'path_img')]),
        ),
    ]