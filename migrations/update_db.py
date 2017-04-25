# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection, models, migrations
from django.db.utils import OperationalError, ProgrammingError

def update_user_model(apps, schema_editor):
    """
        from dj_node.migrations.update_db import *
        update_user_model(None, None)
    """
    cursor = connection.cursor()
    query = "ALTER TABLE auth_user MODIFY username VARCHAR(80);";

    try:
        cursor.execute(query)
    except (OperationalError, ProgrammingError), e:
        print e
        print "Query is not executed {}.".format(query)

    try:
        cursor.execute("ALTER TABLE auth_user ALTER COLUMN username TYPE varchar(80);")
    except (OperationalError, ProgrammingError), e:
        print e
        print "Query is not executed {}.".format(query)


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
       migrations.RunPython(update_user_model),
    ]