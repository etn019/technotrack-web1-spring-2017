# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from core.models import User


class Blog(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blogs')
    title = models.CharField(max_length=140)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class Post(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=140)
    text = models.TextField()
    liked = models.IntegerField(default=0)
    shared = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

class Like(models.Model):

    liker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes')
    post = models.ForeignKey(Post, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)