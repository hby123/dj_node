# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('dj_node', '0003_auto_20170221_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=50, null=True, blank=True)),
                ('display_name', models.CharField(max_length=500)),
                ('user_id', models.IntegerField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('rating', models.IntegerField(default=0, null=True, blank=True)),
                ('site', models.ForeignKey(blank=True, to='sites.Site', null=True)),
            ],
        ),
    ]
