# Generated by Django 2.1.7 on 2019-03-28 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conservation', '0016_auto_20190327_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conservationthreat',
            name='area_affected_percent',
            field=models.DecimalField(blank=True, decimal_places=0, help_text='The estimated percentage (0-100) of the specified occurrence area affected by this threat.', max_digits=3, null=True, verbose_name='Area affected [%]'),
        ),
    ]