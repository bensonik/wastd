# Generated by Django 2.0.8 on 2018-12-04 11:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0010_auto_20181130_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='source',
            field=models.PositiveIntegerField(choices=[(0, 'Direct entry'), (1, 'Manual entry from paper datasheet'), (2, 'Digital data capture (ODK)'), (10, 'Threatened Fauna'), (11, 'Threatened Flora'), (12, 'Threatened Communities'), (13, 'Threatened Communities Boundaries'), (14, 'Threatened Communities Buffers'), (15, 'Threatened Communities Sites'), (20, 'Turtle Tagging Database WAMTRAM2'), (21, 'Ningaloo Turtle Program'), (22, 'Broome Turtle Program'), (23, 'Pt Hedland Turtle Program'), (24, 'Gnaraloo Turtle Program'), (25, 'Eco Beach Turtle Program'), (30, 'Cetacean Strandings Database'), (31, 'Pinniped Strandings Database')], default=0, help_text='Where was this record captured initially?', verbose_name='Data Source'),
        ),
        migrations.AddField(
            model_name='community',
            name='source_id',
            field=models.CharField(default=uuid.UUID('f14f768e-f7b4-11e8-a86f-40f02f6195e0'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
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
            model_name='hbvvernacular',
            name='name',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='hbvvernacular',
            name='vernacular',
            field=models.CharField(blank=True, help_text='', max_length=1000, null=True, verbose_name='Vernacular Name'),
        ),
    ]
