# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-15 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='piva',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Partita IVA'),
        ),
    ]
