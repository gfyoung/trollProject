# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def populateConfigOptionTable(apps, schema_editor):
    ConfigOption = apps.get_model("trollApp", "ConfigOption")

    trollRedirectProb = ConfigOption.objects.create(name="trollRedirectProb", value=0.1)
    updateFrequency = ConfigOption.objects.create(name="updateFrequency", value=0.05)

    trollRedirectProb.save()
    updateFrequency.save()

class Migration(migrations.Migration):

    dependencies = [
        ('trollApp', '0004_initDownloadTableData'),
    ]

    operations = [
       migrations.RunPython(populateConfigOptionTable)
    ]
