# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-08 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fatturazione', '0015_auto_20200708_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliquotaiva',
            name='natura_esenzione',
            field=models.CharField(blank=True, choices=[('N1', 'N1'), ('N2', 'N2'), ('N3', 'N3'), ('N4', 'N4'), ('N5', 'N5'), ('N6', 'N6'), ('N7', 'N7')], max_length=5, verbose_name='natura esenzione'),
        ),
    ]
