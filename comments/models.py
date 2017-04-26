from __future__ import unicode_literals
from posts.models import Post
from django.db import models
from core.models import User
from django.conf import settings


class Comment(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')
    post = models.ForeignKey(Post)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)