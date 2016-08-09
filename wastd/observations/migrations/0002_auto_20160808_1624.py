# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-08 08:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TurtleEncounter',
            fields=[
                ('animalencounter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.AnimalEncounter')),
            ],
            options={
                'ordering': ['when', 'where'],
                'get_latest_by': 'when',
                'verbose_name': 'Turtle Encounter',
                'verbose_name_plural': 'Turtle Encounters',
            },
            bases=('observations.animalencounter',),
        ),
        migrations.CreateModel(
            name='TurtleNestingObservation',
            fields=[
                ('observation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.Observation')),
                ('nest_position', models.CharField(choices=[('below-hwm', 'below high water mark'), ('above-hw', 'above high water mark, below dune'), ('dune-edge', 'edge of dune, beginning of spinifex'), ('in-dune', 'inside dune, spinifex')], default='unknown', help_text='The position of the nest on the beach.', max_length=300, verbose_name='Beach position')),
                ('eggs_laid', models.BooleanField(default=False, help_text="Did round, white objects leave the turtle's butt?", verbose_name='Did the turtle lay eggs?')),
                ('egg_count', models.PositiveIntegerField(blank=True, help_text='The number of eggs laid.', null=True, verbose_name='Number of eggs laid')),
            ],
            options={
                'abstract': False,
            },
            bases=('observations.observation',),
        ),
        migrations.AddField(
            model_name='animalencounter',
            name='activity',
            field=models.CharField(choices=[('arriving', 'arriving'), ('digging-body-pit', 'digging body pit'), ('excavating-egg-chamber', 'excavating egg chamber'), ('laying-eggs', 'laying eggs'), ('filling-in-egg-chamber', 'filling in egg chamber'), ('returning-to-water', 'returning to water'), ('other', 'other activity'), ('unknown', 'unknown activity')], default='unknown', help_text="The animal's activity at the time of observation.", max_length=300, verbose_name='Activity'),
        ),
        migrations.AddField(
            model_name='distinguishingfeatureobservation',
            name='scanned_for_pit_tags',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Scanned for PIT tags'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='maturity',
            field=models.CharField(choices=[('juvenile', 'juvenile'), ('adult', 'adult'), ('unknown', 'unknown maturity')], default='unknown', help_text="The animal's maturity.", max_length=300, verbose_name='Maturity'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='species',
            field=models.CharField(choices=[('Natator depressus', 'Flatback turtle (Natator depressus)'), ('Chelonia mydas', 'Green turtle (Chelonia mydas)'), ('Eretmochelys imbricata', 'Hawksbill turtle (Eretmochelys imbricata)'), ('Caretta caretta', 'Loggerhead turtle (Caretta caretta)'), ('Lepidochelys olivacea', 'Olive Ridley turtle (Lepidochelys olivacea)'), ('Dermochelys coriacea', 'Leatherback turtle (Dermochelys coriacea)'), ('Corolla corolla', 'Hatchback turtle (Corolla corolla)'), ('unidentified', 'Unidentified species')], default='unidentified', help_text='The species of the animal.', max_length=300, verbose_name='Species'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='algal_growth',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Algal growth on carapace'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='barnacles',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Barnacles'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='damage_injury',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Obvious damage or injuries'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='missing_limbs',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Missing limbs'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='propeller_damage',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Propeller strike damage'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='tagging_scars',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Tagging scars'),
        ),
    ]