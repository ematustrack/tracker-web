# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 17:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20170802_1035'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='st_folio',
            unique_together=set([('idST', 'idFolio', 'path_img')]),
        ),
    ]