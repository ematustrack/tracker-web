# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-12 22:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_auto_20170807_1021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folio',
            options={'verbose_name_plural': 'Creaci\xf3n de Folio'},
        ),
        migrations.AlterModelOptions(
            name='pro',
            options={'verbose_name_plural': 'Creaci\xf3n de Profesional'},
        ),
        migrations.AlterModelOptions(
            name='st',
            options={'verbose_name_plural': 'Creaci\xf3n de ST'},
        ),
        migrations.AlterModelOptions(
            name='st_folio',
            options={'verbose_name_plural': 'ST y Folios asociados'},
        ),
        migrations.AlterModelOptions(
            name='st_work',
            options={'verbose_name_plural': 'Obras asociadas'},
        ),
        migrations.AlterModelOptions(
            name='work',
            options={'verbose_name_plural': 'Creaci\xf3n de Obra'},
        ),
    ]
