#!/usr/bin/python
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump utility.
#
# Written by : Rahul Kumar
# Website: http://tecadmin.net
# Created date: Dec 03, 2013
# Last modified: Dec 03, 2013
# Tested with : Python 2.6.6
# Script Revision: 1.1
#
##########################################################

import os, sys
import time
import datetime
from django.conf import settings

# Setup up Django standalone script
#
dir_path = os.path.dirname(os.path.realpath(__file__))
proj_path = os.path.dirname(os.path.dirname((os.path.dirname(dir_path))))
project_app = os.path.basename(proj_path)
print "proj_path: %s" % proj_path
print "project_app: %s" % project_app

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % project_app)
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databses names one on each line and assignd to DB_NAME variable.

# DATABASES = {
#  'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'USER': 'root',
#         'PASSWORD': 'password',
#         'NAME': 'my_db',
#         'TEST': {
#             'NAME': 'mytestdatabase',
#         },
#     },
# }

DB_HOST = 'localhost'
DB_USER = settings.DATABASES['default']['USER']
DB_USER_PASSWORD = settings.DATABASES['default']['PASSWORD']
DB_NAME = settings.DATABASES['default']['NAME']
BACKUP_PATH = '/backup/db/'

# Getting current datetime to create seprate backup folder like "12012013-071334".
DATETIME = time.strftime('%m%d%Y-%H%M%S')

TODAYBACKUPPATH = BACKUP_PATH + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
print "creating backup folder"
if not os.path.exists(TODAYBACKUPPATH):
    os.makedirs(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print "checking for databases names file."
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print "Databases file found..."
    print "Starting backup of all dbs listed in file " + DB_NAME
else:
    print "Databases file not found..."
    print "Starting backup of database " + DB_NAME
    multi = 0

# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")

   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       dumpcmd = "sudo mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
       os.system(dumpcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "sudo mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
   os.system(dumpcmd)

print "Backup script completed"
print "Your backups has been created in '" + TODAYBACKUPPATH + "' directory"
