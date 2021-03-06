# Generated by Django 2.1.7 on 2019-03-01 01:44

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190225_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='aliases',
            field=models.TextField(blank=True, help_text='Any names this user is known as in other databases and data collection forms. Separate names by comma.', verbose_name='Aliases of User'),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=255, verbose_name='Preferred name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='The primary contact number including national prefix, e.g. +61 412 345 678. Spaces are accepted but will be removed on saving.', max_length=128, null=True, verbose_name='Phone Number'),
        ),
    ]
