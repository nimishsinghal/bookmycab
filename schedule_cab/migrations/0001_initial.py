# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=70, null=True, unique=True)),
                ('source_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('source_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('destination_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('destination_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('schedule_time', models.IntegerField(db_index=True)),
                ('install_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'schedule_cab',
            },
        ),
    ]
