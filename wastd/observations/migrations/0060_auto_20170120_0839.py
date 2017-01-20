# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-20 00:39
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0059_auto_20170120_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linetransectencounter',
            name='transect',
            field=django.contrib.gis.db.models.fields.LineStringField(help_text='The line transect as LineString in WGS84', srid=4326, verbose_name='Transect line'),
        ),
    ]