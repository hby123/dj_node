# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_node', '0002_update_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
