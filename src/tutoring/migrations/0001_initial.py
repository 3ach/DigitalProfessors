# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 21:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('phone', models.IntegerField()),
                ('website', models.URLField()),
                ('wifi_ssid', models.TextField(max_length=128)),
                ('wifi_password', models.TextField(max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('distance', models.FloatField()),
                ('billed', models.DecimalField(decimal_places=2, max_digits=12)),
                ('paid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutoring.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutoring.Professor'),
        ),
    ]
