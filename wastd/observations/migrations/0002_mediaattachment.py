# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 11:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(blank=True, choices=[('data_sheet', 'Original data sheet'), ('photograph', 'Photograph'), ('other', 'Other')], help_text='What is the attached file about?', max_length=300, null=True, verbose_name='Attachment type')),
                ('title', models.CharField(blank=True, help_text='Give the attachment a representative name', max_length=300, null=True, verbose_name='Attachment name')),
                ('attachment', models.FileField(help_text='Upload the file', upload_to='media/%Y/%m/%d/', verbose_name='File attachment')),
                ('observation', models.ForeignKey(help_text='Which Observation does this attachment relate to?', on_delete=django.db.models.deletion.CASCADE, to='observations.Observation', verbose_name='Observation')),
            ],
        ),
    ]
