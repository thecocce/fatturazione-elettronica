# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-08 11:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fatturazione', '0011_auto_20200708_1332'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EsenzioneIva',
            new_name='AliquotaIva',
        ),
        migrations.AlterModelOptions(
            name='aliquotaiva',
            options={'verbose_name': 'alituota IVA', 'verbose_name_plural': 'aliquote IVA'},
        ),
    ]
