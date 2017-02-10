# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection, models, migrations

def update_user_model(apps, schema_editor):
    # select all rows in echo_project
    cursor = connection.cursor()
    query = "ALTER TABLE auth_user MODIFY username VARCHAR(80);";
    cursor.execute(query)


class Migration(migrations.Migration):

    dependencies = [
        ('dj_node', '0001_initial'),
    ]

    operations = [
       migrations.RunPython(update_user_model),
    ]