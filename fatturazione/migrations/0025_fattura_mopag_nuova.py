# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-08 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fatturazione', '0024_modalitapagamento_codice_pagamento_fattura_elettronica'),
    ]

    operations = [
        migrations.AddField(
            model_name='fattura',
            name='mopag_nuova',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='fatturazione.ModalitaPagamento'),
        ),
    ]
