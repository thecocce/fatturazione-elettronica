# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-08 15:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fatturazione', '0026_auto_20200708_1743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fattura',
            old_name='mopag_nuova',
            new_name='mopag',
        ),
    ]