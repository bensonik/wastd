# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-19 05:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagobservation',
            name='position',
        ),
        migrations.RemoveField(
            model_name='tagobservation',
            name='side',
        ),
        migrations.AddField(
            model_name='tagobservation',
            name='tag_location',
            field=models.CharField(choices=[('head', 'head'), ('plastron', 'plastron'), ('carapace', 'carapace'), ('tail', 'tail'), ('flipper-front-left-1', 'front left flipper, 1st scale from body'), ('flipper-front-left-2', 'front left flipper, 2nd scale from body'), ('flipper-front-left-3', 'front left flipper, 3rd scale from body'), ('flipper-front-left', 'front left flipper'), ('flipper-front-right-1', 'front right flipper, 1st scale from body'), ('flipper-front-right-2', 'front right flipper, 2nd scale from body'), ('flipper-front-right-3', 'front right flipper, 3rd scale from body'), ('flipper-front-right', 'front right flipper'), ('flipper-rear-left', 'rear left flipper'), ('flipper-rear-right', 'rear right flipper'), ('whole', 'whole turtle')], default='whole', help_text='Where is the tag attached, or the sample taken from?', max_length=300, verbose_name='Tag position'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='activity',
            field=models.CharField(choices=[('na', 'not observed'), ('arriving', 'arriving on beach'), ('digging-body-pit', 'digging body pit'), ('excavating-egg-chamber', 'excavating egg chamber'), ('laying-eggs', 'laying eggs'), ('filling-in-egg-chamber', 'filling in egg chamber'), ('returning-to-water', 'returning to water'), ('floating', 'floating (dead, sick, unable to dive, drifting in water)'), ('beach-washed', 'beach washed (dead, sick or stranded on beach/coast)'), ('beach-jumped', 'beach jumped'), ('carcass-tagged-released', 'carcass tagged and released'), ('carcass-inland', 'carcass or butchered remains found removed from coast'), ('captivity', 'in captivity'), ('non-breeding', 'general non-breeding activity (swimming, sleeping, feeding, etc.)'), ('other', 'other activity')], default='na', help_text="The animal's activity at the time of observation.", max_length=300, verbose_name='Activity'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='habitat',
            field=models.CharField(choices=[('na', 'not observed'), ('beach', 'beach (below vegetation line)'), ('bays-estuaries', 'bays, estuaries and other enclosed shallow soft sediments'), ('dune', 'dune'), ('dune-constructed-hard-substrate', 'dune, constructed hard substrate (concrete slabs, timber floors, helipad)'), ('dune-grass-area', 'dune, grass area'), ('dune-compacted-path', 'dune, hard compacted areas (road ways, paths)'), ('dune-rubble', 'dune, rubble, usually coral'), ('dune-bare-sand', 'dune, bare sand area'), ('dune-beneath-vegetation', 'dune, beneath tree or shrub'), ('slope-front-dune', 'dune, front slope'), ('sand-flats', 'sand flats'), ('slope-grass', 'slope, grass area'), ('slope-bare-sand', 'slope, bare sand area'), ('slope-beneath-vegetation', 'slope, beneath tree or shrub'), ('below-mean-spring-high-water-mark', 'below the mean spring high water line or current level of inundation'), ('lagoon-patch-reef', 'lagoon, patch reef'), ('lagoon-open-sand', 'lagoon, open sand areas'), ('mangroves', 'mangroves'), ('reef-coral', 'coral reef'), ('reef-crest-front-slope', 'reef crest (dries at low water) and front reef slope areas'), ('reef-flat', 'reef flat, dries at low tide'), ('reef-seagrass-flats', 'coral reef with seagrass flats'), ('reef-rocky', 'rocky reef'), ('open-water', 'open water')], default='na', help_text='The habitat in which the animal was encountered.', max_length=500, verbose_name='Habitat'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='health',
            field=models.CharField(choices=[('na', 'not observed'), ('alive', 'alive (healthy)'), ('alive-injured', 'alive (injured)'), ('alive-then-died', 'initally alive (but died)'), ('dead-edible', 'dead (carcass edible)'), ('dead-organs-intact', 'dead (decomposed but organs intact)'), ('dead-advanced', 'dead (organs decomposed)'), ('dead-mummified', 'mummified (dead, skin holding bones)'), ('dead-disarticulated', 'disarticulated (dead, no soft tissue remaining)'), ('other', 'other')], default='na', help_text='On a scale from the Fresh Prince of Bel Air to 80s Hair Metal: how dead and decomposed is the animal?', max_length=300, verbose_name='Health status'),
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
            name='scanned_for_pit_tags',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Scanned for PIT tags'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='tagging_scars',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Tagging scars'),
        ),
        migrations.AlterField(
            model_name='tagobservation',
            name='status',
            field=models.CharField(choices=[('ordered', 'ordered from manufacturer'), ('produced', 'produced by manufacturer'), ('delivered', 'delivered to HQ'), ('allocated', 'allocated to field team'), ('attached', 'first association with animal'), ('recaptured', 're-sighted associated with animal'), ('removed', 'taken off animal'), ('found', 'found detached'), ('returned', 'returned to HQ'), ('decommissioned', 'decommissioned'), ('destroyed', 'destroyed'), ('observed', 'observed in any other context, see comments')], default='recaptured', help_text='The status this tag was seen in, or brought into.', max_length=300, verbose_name='Tag status'),
        ),
        migrations.AlterField(
            model_name='turtledamageobservation',
            name='body_part',
            field=models.CharField(choices=[('head', 'head'), ('plastron', 'plastron'), ('carapace', 'carapace'), ('tail', 'tail'), ('flipper-front-left-1', 'front left flipper, 1st scale from body'), ('flipper-front-left-2', 'front left flipper, 2nd scale from body'), ('flipper-front-left-3', 'front left flipper, 3rd scale from body'), ('flipper-front-left', 'front left flipper'), ('flipper-front-right-1', 'front right flipper, 1st scale from body'), ('flipper-front-right-2', 'front right flipper, 2nd scale from body'), ('flipper-front-right-3', 'front right flipper, 3rd scale from body'), ('flipper-front-right', 'front right flipper'), ('flipper-rear-left', 'rear left flipper'), ('flipper-rear-right', 'rear right flipper'), ('whole', 'whole turtle')], default='whole-turtle', help_text='The body part affected by the observed damage.', max_length=300, verbose_name='Affected body part'),
        ),
        migrations.AlterField(
            model_name='turtlenestencounter',
            name='habitat',
            field=models.CharField(choices=[('na', 'not observed'), ('beach', 'beach (below vegetation line)'), ('bays-estuaries', 'bays, estuaries and other enclosed shallow soft sediments'), ('dune', 'dune'), ('dune-constructed-hard-substrate', 'dune, constructed hard substrate (concrete slabs, timber floors, helipad)'), ('dune-grass-area', 'dune, grass area'), ('dune-compacted-path', 'dune, hard compacted areas (road ways, paths)'), ('dune-rubble', 'dune, rubble, usually coral'), ('dune-bare-sand', 'dune, bare sand area'), ('dune-beneath-vegetation', 'dune, beneath tree or shrub'), ('slope-front-dune', 'dune, front slope'), ('sand-flats', 'sand flats'), ('slope-grass', 'slope, grass area'), ('slope-bare-sand', 'slope, bare sand area'), ('slope-beneath-vegetation', 'slope, beneath tree or shrub'), ('below-mean-spring-high-water-mark', 'below the mean spring high water line or current level of inundation'), ('lagoon-patch-reef', 'lagoon, patch reef'), ('lagoon-open-sand', 'lagoon, open sand areas'), ('mangroves', 'mangroves'), ('reef-coral', 'coral reef'), ('reef-crest-front-slope', 'reef crest (dries at low water) and front reef slope areas'), ('reef-flat', 'reef flat, dries at low tide'), ('reef-seagrass-flats', 'coral reef with seagrass flats'), ('reef-rocky', 'rocky reef'), ('open-water', 'open water')], default='na', help_text='The habitat in which the nest was encountered.', max_length=500, verbose_name='Habitat'),
        ),
    ]