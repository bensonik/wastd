# Generated by Django 2.1.7 on 2019-06-06 09:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('occurrence', '0040_auto_20190606_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaencounter',
            name='encountered_on',
            field=models.DateTimeField(blank=True, db_index=True, help_text='The datetime of the original encounter, entered in the local time zone GMT+08 (Perth/Australia).', null=True, verbose_name='Encountered on'),
        ),
        migrations.AlterField(
            model_name='areaencounter',
            name='source_id',
            field=models.CharField(default=uuid.UUID('5001cf4a-883a-11e9-a870-40f02f6195e0'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
    ]
