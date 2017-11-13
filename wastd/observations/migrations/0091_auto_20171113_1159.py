# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 03:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0090_auto_20170419_1626'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animalencounter',
            options={'base_manager_name': 'base_objects', 'get_latest_by': 'when', 'ordering': ['when', 'where'], 'verbose_name': 'Animal Encounter', 'verbose_name_plural': 'Animal Encounters'},
        ),
        migrations.AlterModelOptions(
            name='encounter',
            options={'base_manager_name': 'base_objects', 'get_latest_by': 'when', 'ordering': ['when', 'where'], 'verbose_name': 'Encounter', 'verbose_name_plural': 'Encounters'},
        ),
        migrations.AlterModelOptions(
            name='linetransectencounter',
            options={'base_manager_name': 'base_objects', 'get_latest_by': 'when', 'ordering': ['when', 'where'], 'verbose_name': 'Line Transect Encounter', 'verbose_name_plural': 'Line Transect Encounters'},
        ),
        migrations.AlterModelOptions(
            name='loggerencounter',
            options={'base_manager_name': 'base_objects', 'get_latest_by': 'when', 'ordering': ['when', 'where'], 'verbose_name': 'Logger Encounter', 'verbose_name_plural': 'Logger Encounters'},
        ),
        migrations.AlterModelOptions(
            name='mediaattachment',
            options={'base_manager_name': 'base_objects'},
        ),
        migrations.AlterModelOptions(
            name='observation',
            options={'base_manager_name': 'base_objects'},
        ),
        migrations.AlterModelOptions(
            name='turtlenestencounter',
            options={'base_manager_name': 'base_objects', 'get_latest_by': 'when', 'ordering': ['when', 'where'], 'verbose_name': 'Turtle Nest Encounter', 'verbose_name_plural': 'Turtle Nest Encounters'},
        ),
        migrations.AlterModelManagers(
            name='animalencounter',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='dispatchrecord',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='dugongmorphometricobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='encounter',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='hatchlingmorphometricobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='linetransectencounter',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='loggerencounter',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='managementaction',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='mediaattachment',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='nesttagobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='observation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='tagobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='temperatureloggerdeployment',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='temperatureloggersettings',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='tracktallyobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='turtledamageobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='turtlemorphometricobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='turtlenestdisturbanceobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='turtlenestdisturbancetallyobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='turtlenestencounter',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='turtlenestobservation',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='tagobservation',
            name='tag_type',
            field=models.CharField(choices=[('flipper-tag', 'Flipper Tag'), ('pit-tag', 'PIT Tag'), ('sat-tag', 'Satellite Relay Data Logger'), ('blood-sample', 'Blood Sample'), ('biopsy-sample', 'Biopsy Sample'), ('stomach-content-sample', 'Stomach Content Sample'), ('physical-sample', 'Physical Sample'), ('egg-sample', 'Egg Sample'), ('qld-monel-a-flipper-tag', 'QLD Monel Series A flipper tag'), ('qld-titanium-k-flipper-tag', 'QLD Titanium Series K flipper tag'), ('qld-titanium-t-flipper-tag', 'QLD Titanium Series T flipper tag'), ('acoustic-tag', 'Acoustic tag'), ('commonwealth-titanium-flipper-tag', 'Commonwealth titanium flipper tag (old db value)'), ('cmlth-titanium-flipper-tag', 'Commonwealth titanium flipper tag'), ('cayman-juvenile-tag', 'Cayman juvenile tag'), ('hawaii-inconel-flipper-tag', 'Hawaii Inst Mar Biol Inconel tag'), ('ptt', 'Platform Transmitter Terminal (PTT)'), ('rototag', 'RotoTag'), ('narangebub-nickname', 'Narangebup rehab informal name'), ('aqwa-nickname', 'AQWA informal name'), ('atlantis-nickname', 'Atlantis informal name'), ('wa-museum-reptile-registration-number', 'WA Museum Natural History Reptiles Catalogue Registration Number (old db value)'), ('wam-reptile-registration-number', 'WA Museum Natural History Reptiles Catalogue Registration Number'), ('genetic-tag', 'Genetic ID sequence'), ('other', 'Other')], default='flipper-tag', help_text='What kind of tag is it?', max_length=300, verbose_name='Tag type'),
        ),
    ]