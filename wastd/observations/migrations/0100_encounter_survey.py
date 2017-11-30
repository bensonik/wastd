# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 06:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0099_auto_20171130_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='encounter',
            name='survey',
            field=models.ForeignKey(blank=True, help_text='The survey during which this encounter happened.', null=True, on_delete=django.db.models.deletion.CASCADE, to='observations.Survey', verbose_name='Survey'),
        ),
    ]
