# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-08 11:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fatturazione', '0010_elementofattura_iva_fk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elementofattura',
            old_name='iva_fk',
            new_name='esenzione_iva',
        ),
    ]
