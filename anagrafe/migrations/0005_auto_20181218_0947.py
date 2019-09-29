# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-18 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafe', '0004_auto_20181215_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='codice_univoco',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Codice univoco'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='indirizzo_pec',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True, verbose_name='Indirizzo PEC'),
        ),
    ]