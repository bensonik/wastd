# Generated by Django 2.1.5 on 2019-02-11 03:33

import uuid

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django_fsm
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('occurrence', '0017_auto_20190204_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', django_fsm.FSMField(choices=[('new', 'New'), ('proofread', 'Proofread'), ('curated', 'Curated'), ('published', 'Published')], default='new', max_length=50, verbose_name='QA Status')),
            ],
            options={
                'verbose_name': 'Observation Group',
            },
        ),
        migrations.AlterField(
            model_name='areaencounter',
            name='area_type',
            field=models.PositiveIntegerField(choices=[(0, 'Ephemeral Site'), (1, 'Permanent Site'), (3, 'Partial survey'), (2, 'Critical Habitat'), (10, 'TEC Boundary'), (11, 'TEC Buffer'), (12, 'TEC Site'), (20, 'Flora Population'), (21, 'Flora Subpopulation'), (30, 'Fauna Site'), (40, 'Marine Protected Area'), (41, 'Locality')], default=0, help_text='What type describes the area occupied by the encounter most accurately? The area can be an opportunistic, once-off chance encounter (point), a fixed survey site (polygon), a partial or a complete survey of an area occupied by the encountered subject (polygon).', verbose_name='Area type'),
        ),
        migrations.AlterField(
            model_name='areaencounter',
            name='geom',
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, help_text='The exact extent of the area occupied by the encountered subject as polygon in WGS84, if available.', null=True, srid=4326, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='areaencounter',
            name='northern_extent',
            field=models.FloatField(blank=True, editable=False, help_text='The northernmost latitude is derived from location polygon or point and serves to sort areas.', null=True, verbose_name='Northernmost latitude'),
        ),
        migrations.AlterField(
            model_name='areaencounter',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, help_text='A point representing the area occupied by the encountered subject. If empty, the point will be calculated as the centroid of the polygon extent.', null=True, srid=4326, verbose_name='Representative Point'),
        ),
        migrations.AlterField(
            model_name='areaencounter',
            name='source_id',
            field=models.CharField(default=uuid.UUID('c7232db8-2dad-11e9-a86f-ecf4bb19b5fc'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
        migrations.AddField(
            model_name='observationgroup',
            name='encounter',
            field=models.ForeignKey(help_text='The Area Encounter during which the observation group was observed.', on_delete=django.db.models.deletion.CASCADE, to='occurrence.AreaEncounter', verbose_name='Area Encounter'),
        ),
        migrations.AddField(
            model_name='observationgroup',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_occurrence.observationgroup_set+', to='contenttypes.ContentType'),
        ),
    ]
