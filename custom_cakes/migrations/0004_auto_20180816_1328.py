# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-16 20:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_cakes', '0003_auto_20180816_1230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customcakeorderconfigoption',
            options={'ordering': ('sort',)},
        ),
        migrations.AlterModelOptions(
            name='customcakeorderconfigoptionitem',
            options={'ordering': ('sort',)},
        ),
    ]
