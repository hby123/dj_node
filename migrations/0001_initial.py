# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=500)),
                ('user_id', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name=b'related object')),
                ('content_type', models.ForeignKey(verbose_name=b'content page', blank=True, to='contenttypes.ContentType', null=True)),
                ('site', models.ForeignKey(blank=True, to='sites.Site', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=50, null=True, blank=True)),
                ('display_name', models.CharField(max_length=30, null=True, blank=True)),
                ('user_id', models.IntegerField(null=True, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name=b'related object')),
                ('content_type', models.ForeignKey(verbose_name=b'content page', blank=True, to='contenttypes.ContentType', null=True)),
                ('site', models.ForeignKey(blank=True, to='sites.Site', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaillingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'primary', max_length=30, null=True, blank=True)),
                ('email', models.EmailField(max_length=30, null=True, blank=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('site', models.ForeignKey(blank=True, to='sites.Site', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=50, null=True, blank=True)),
                ('display_name', models.CharField(max_length=500)),
                ('user_id', models.IntegerField(null=True, blank=True)),
                ('review', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('rating', models.IntegerField(default=0, null=True, blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name=b'related object')),
                ('content_type', models.ForeignKey(verbose_name=b'content page', blank=True, to='contenttypes.ContentType', null=True)),
                ('site', models.ForeignKey(blank=True, to='sites.Site', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50)),
                ('domain', models.CharField(max_length=50, null=True, blank=True)),
                ('url', models.CharField(max_length=500, null=True, blank=True)),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('token', models.CharField(unique=True, max_length=200)),
                ('used', models.NullBooleanField(default=False)),
                ('expire', models.DateField()),
                ('site', models.ForeignKey(blank=True, to='sites.Site', null=True)),
            ],
        ),
    ]
