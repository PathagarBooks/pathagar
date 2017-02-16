# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import models, migrations

def load_fixture(apps, schema_editor):
    call_command('loaddata', 'initial_fixture', app='books')


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture)
    ]
