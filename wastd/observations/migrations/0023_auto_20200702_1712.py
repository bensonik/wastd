# Generated by Django 2.2.13 on 2020-07-02 09:12

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0022_auto_20200702_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='status',
            field=django_fsm.FSMField(choices=[('new', 'New'), ('proofread', 'Proofread'), ('curated', 'Curated'), ('published', 'Published'), ('flagged', 'Flagged'), ('rejected', 'Rejected')], db_index=True, default='new', max_length=50, verbose_name='QA Status'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='status',
            field=django_fsm.FSMField(choices=[('new', 'New'), ('proofread', 'Proofread'), ('curated', 'Curated'), ('published', 'Published'), ('flagged', 'Flagged'), ('rejected', 'Rejected')], default='new', max_length=50, verbose_name='QA Status'),
        ),
    ]