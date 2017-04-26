from django.views.generic import ListView
from models import Comment
from posts.models import Post
from django import forms

#Won't write my code here

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')