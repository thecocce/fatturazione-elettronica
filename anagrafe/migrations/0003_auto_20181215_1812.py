# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-15 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafe', '0002_auto_20181215_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='allegiva',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Allegati IVA'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='capcor',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='CAP corrispondente'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='datanasc',
            field=models.DateField(blank=True, null=True, verbose_name='Data nascita'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='indircor',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Indirizzo corrispondente'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='local',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Località'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='localcor',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Località corrispondente'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='luona',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Luogo nascita'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nazionecor',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Nazione corrispondente'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='provcor',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Provincia corrispondente'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='provna',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Provincia nascita'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='ressec',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Residenza secondaria'),
        ),
    ]
