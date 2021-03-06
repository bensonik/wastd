# Generated by Django 2.1.7 on 2019-06-06 09:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('conservation', '0024_auto_20190606_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityconservationlisting',
            name='source_id',
            field=models.CharField(default=uuid.UUID('5001cf4b-883a-11e9-a870-40f02f6195e0'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
        migrations.AlterField(
            model_name='conservationthreat',
            name='encountered_on',
            field=models.DateTimeField(blank=True, db_index=True, help_text='The datetime of the original encounter, entered in the local time zone GMT+08 (Perth/Australia).', null=True, verbose_name='Encountered on'),
        ),
        migrations.AlterField(
            model_name='taxonconservationlisting',
            name='source_id',
            field=models.CharField(default=uuid.UUID('5001cf4b-883a-11e9-a870-40f02f6195e0'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
    ]
