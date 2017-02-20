import uuid
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# add extra fields to user
User.add_to_class('website', models.CharField(max_length=50, null=True, blank=True))
User.add_to_class('actual_email', models.CharField(max_length=50, null=True, blank=True))
User.add_to_class('display_name', models.CharField(max_length=50, null=True, blank=True))
User.add_to_class('display_name_slug', models.CharField(max_length=50, null=True, blank=True))

class Comment(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True)
    domain= models.CharField(max_length=50, null=True, blank=True)
    display_name = models.CharField(max_length=30, null=True, blank=True,)
    user_id = models.IntegerField(null=True, blank=True,)
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True,)

    content_type = models.ForeignKey(
        ContentType,
        verbose_name= 'content page',
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )
    content_object = generic.GenericForeignKey('content_type', 'object_id')


class Review(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True,)
    domain = models.CharField(max_length=50, null=True, blank=True,)
    display_name = models.CharField(max_length=500)
    user_id = models.IntegerField(null=True, blank=True,)
    review = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True,)
    rating = models.IntegerField(default=0, null=True, blank=True,)

    content_type = models.ForeignKey(
        ContentType,
        verbose_name='content page',
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )
    content_object = generic.GenericForeignKey('content_type', 'object_id')


class Bookmark(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True,)
    display_name = models.CharField(max_length=500)
    user_id = models.IntegerField()
    date = models.DateTimeField(auto_now=True, null=True, blank=True,)

    content_type = models.ForeignKey(
        ContentType,
        verbose_name='content page',
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )
    content_object = generic.GenericForeignKey('content_type', 'object_id')

class MaillingList(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True,)
    name = models.CharField(max_length=30, null=True, blank=True, default="primary")
    email = models.EmailField(max_length=30, null=True, blank=True,)
    date = models.DateTimeField(auto_now=True, null=True, blank=True,)


class Token(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True)
    type = models.CharField(max_length=50)
    domain = models.CharField(max_length=50, null=True, blank=True,)
    url = models.CharField(max_length=500, null=True, blank=True,)
    email = models.EmailField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=200, unique=True)
    used = models.NullBooleanField(default=False)
    expire = models.DateField()

    @staticmethod
    def generate_token():
        return uuid.uuid4()
