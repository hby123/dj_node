# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_node', '0002_update_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercontent',
            name='site',
        ),
        migrations.DeleteModel(
            name='UserContent',
        ),
    ]
