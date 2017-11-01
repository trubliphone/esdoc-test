# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 09:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('LOCAL', 'Local'), ('TEST', 'Test'), ('DEV', 'Development'), ('PROD', 'Production')], max_length=128)),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='q_site', to='sites.Site')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Questionnaire Sites',
                'verbose_name': 'Questionnaire Site',
            },
        ),
    ]