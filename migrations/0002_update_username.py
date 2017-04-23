# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection, models, migrations
from django.db.utils import OperationalError

def update_user_model(apps, schema_editor):
    cursor = connection.cursor()
    query = "ALTER TABLE auth_user MODIFY username VARCHAR(80);";

    try:
        cursor.execute(query)
    except OperationalError, e:
        print "Query is not executed {}.".format(query)

class Migration(migrations.Migration):

    dependencies = [
        ('dj_node', '0001_initial'),
    ]

    operations = [
       migrations.RunPython(update_user_model),
    ]