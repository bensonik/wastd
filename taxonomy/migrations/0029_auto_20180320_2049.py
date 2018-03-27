# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-20 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0028_auto_20180313_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hbvfamily',
            name='class_name',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='Class'),
        ),
        migrations.AlterField(
            model_name='hbvfamily',
            name='division_name',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='Division'),
        ),
        migrations.AlterField(
            model_name='hbvfamily',
            name='family_name',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='Family Name'),
        ),
        migrations.AlterField(
            model_name='hbvfamily',
            name='kingdom_name',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='Kingdom'),
        ),
        migrations.AlterField(
            model_name='hbvfamily',
            name='order_name',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='Order Name'),
        ),
        migrations.AlterField(
            model_name='hbvfamily',
            name='supra_code',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='HBV Suprafamily Group Code'),
        ),
        migrations.AlterField(
            model_name='hbvgroup',
            name='class_id',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='HBV Suprafamily Group Code'),
        ),
        migrations.AlterField(
            model_name='hbvparent',
            name='class_id',
            field=models.CharField(blank=True, help_text='', max_length=100, null=True, verbose_name='WACensus ClassID'),
        ),
        migrations.AlterField(
            model_name='hbvspecies',
            name='consv_code',
            field=models.CharField(blank=True, help_text='', max_length=100, null=True, verbose_name='Conservation Code'),
        ),
        migrations.AlterField(
            model_name='hbvspecies',
            name='naturalised',
            field=models.CharField(blank=True, help_text='', max_length=100, null=True, verbose_name='Naturalised'),
        ),
        migrations.AlterField(
            model_name='hbvspecies',
            name='ranking',
            field=models.CharField(blank=True, help_text='', max_length=100, null=True, verbose_name='Ranking'),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='rank',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Thing'), (7, 'Community'), (5, 'Domain'), (10, 'Kingdom'), (20, 'Subkingdom'), (30, 'Division'), (40, 'Subdivision'), (50, 'Class'), (60, 'Subclass'), (70, 'Order'), (80, 'Suborder'), (90, 'Family'), (100, 'Subfamily'), (110, 'Tribe'), (120, 'Subtribe'), (130, 'Genus'), (140, 'Subgenus'), (150, 'Section'), (160, 'Subsection'), (170, 'Series'), (180, 'Subseries'), (190, 'Species'), (200, 'Subspecies'), (210, 'Variety'), (220, 'Subvariety'), (230, 'Forma'), (240, 'Subforma')], db_index=True, help_text='The taxonomic rank of the taxon.', null=True, verbose_name='Taxonomic Rank'),
        ),
    ]