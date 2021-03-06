# Generated by Django 2.2.10 on 2020-06-22 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0019_auto_20200609_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatchrecord',
            name='sent_to',
            field=models.ForeignKey(blank=True, default=1, help_text='The receiver of the dispatch.', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='Sent to'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='observer',
            field=models.ForeignKey(default=1, help_text='The person who encountered the subject, and executed any measurements. The observer is the source of measurement bias.', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='observer', to=settings.AUTH_USER_MODEL, verbose_name='Observed by'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='reporter',
            field=models.ForeignKey(default=1, help_text='The person who wrote the initial data sheet in the field. The reporter is the source of handwriting and spelling errors. ', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='reporter', to=settings.AUTH_USER_MODEL, verbose_name='Recorded by'),
        ),
        migrations.AlterField(
            model_name='expedition',
            name='site',
            field=models.ForeignKey(blank=True, help_text='The entire surveyed area.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='observations.Area', verbose_name='Surveyed area'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='reporter',
            field=models.ForeignKey(blank=True, default=1, help_text='The person who captured the start point, ideally this person also recoreded the encounters and end point.', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Recorded by'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='site',
            field=models.ForeignKey(blank=True, help_text='The surveyed site, if known.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='observations.Area', verbose_name='Surveyed site'),
        ),
        migrations.AlterField(
            model_name='surveyend',
            name='reporter',
            field=models.ForeignKey(blank=True, default=1, help_text='The person who captured the start point, ideally this person also recoreded the encounters and end point.', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Recorded by'),
        ),
        migrations.AlterField(
            model_name='surveyend',
            name='site',
            field=models.ForeignKey(blank=True, help_text='The surveyed site, if known.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='observations.Area', verbose_name='Surveyed site'),
        ),
        migrations.AlterField(
            model_name='tagobservation',
            name='handler',
            field=models.ForeignKey(blank=True, default=1, help_text='The person in physical contact with the tag or sample', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tag_handler', to=settings.AUTH_USER_MODEL, verbose_name='Handled by'),
        ),
        migrations.AlterField(
            model_name='tagobservation',
            name='recorder',
            field=models.ForeignKey(blank=True, default=1, help_text='The person who records the tag observation', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tag_recorder', to=settings.AUTH_USER_MODEL, verbose_name='Recorded by'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='light_sources_present',
            field=models.CharField(choices=[('na', 'NA'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Light sources present during emergence'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='outlier_tracks_present',
            field=models.CharField(choices=[('na', 'NA'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Outlier tracks present'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceoutlierobservation',
            name='outlier_group_size',
            field=models.PositiveIntegerField(blank=True, help_text='', null=True, verbose_name='Number of tracks in outlier group'),
        ),
        migrations.AlterField(
            model_name='turtlemorphometricobservation',
            name='handler',
            field=models.ForeignKey(blank=True, help_text='The person conducting the measurements.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='morphometric_handler', to=settings.AUTH_USER_MODEL, verbose_name='Measured by'),
        ),
        migrations.AlterField(
            model_name='turtlemorphometricobservation',
            name='recorder',
            field=models.ForeignKey(blank=True, help_text='The person recording the measurements.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='morphometric_recorder', to=settings.AUTH_USER_MODEL, verbose_name='Recorded by'),
        ),
    ]
