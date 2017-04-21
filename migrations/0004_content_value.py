# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_node', '0003_token_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='value',
            field=models.TextField(null=True, blank=True),
        ),
    ]
