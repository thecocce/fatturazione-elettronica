# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-08 07:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fatturazione', '0009_auto_20200523_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementofattura',
            name='iva_fk',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='fatturazione.EsenzioneIva'),
        ),
    ]