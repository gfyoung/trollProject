# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('target_os', models.CharField(
                    max_length=200, verbose_name="Target OS")),
                ('filename', models.CharField(
                    max_length=200, verbose_name="Filename")),
                ('description', models.CharField(
                    max_length=200, verbose_name="Description")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
