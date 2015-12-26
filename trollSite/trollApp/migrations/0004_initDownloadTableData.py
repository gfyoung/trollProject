# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

platforms = ["Windows", "Linux", "Mac"]
programs = {
    "displaySuccessCall": "Test Download",
    "infiniteTrollSongLoop": 'Troll Song Infinite Loop',
    "persistentTkCall": "Persistent Tkinter Display",
    "massiveFileWriteCall": "Write a Ton of Useless Files"
}


def populateDownloadTable(apps, schema_editor):
    Download = apps.get_model("trollApp", "Download")

    for platform in platforms:
        for program, description in programs.items():
            newDownload = Download.objects.create(
                target_os=platform, filename=program, description=description)
            newDownload.save()


class Migration(migrations.Migration):

    dependencies = [
        ('trollApp', '0003_createConfigOptionTable'),
    ]

    operations = [
        migrations.RunPython(populateDownloadTable)
    ]
