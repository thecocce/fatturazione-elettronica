# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-08 12:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fatturazione', '0017_auto_20200708_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elementofattura',
            old_name='iva',
            new_name='old_iva',
        ),
    ]
