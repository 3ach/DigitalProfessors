# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
