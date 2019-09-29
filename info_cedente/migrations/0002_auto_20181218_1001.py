# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-18 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_cedente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cedente',
            name='codice_fiscale',
            field=models.CharField(blank=True, max_length=20, verbose_name='Codice fiscale'),
        ),
        migrations.AddField(
            model_name='cedente',
            name='indirizzo_email_commerciale',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Indirizzo email commerciale'),
        ),
    ]