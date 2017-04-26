# coding: utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.shortcuts import resolve_url
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.conf import settings

from comments.models import Comment
from posts.models import Blog, Post
from core.models import User


# Create your views here.

class Index(TemplateView):

    #blogs_number = Blog.objects.all().count()
    #posts_number = Post.objects.all().count()
    #comments_number = Comment.objects.all().count()
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all().count()
        context['blogs'] = Blog.objects.all().count()
        context['comments'] = Comment.objects.all().count()
        return context

class RegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2")
        #field_classes = {'username': UsernameField}

class RegisterFormView(FormView):
    form_class = RegistrationForm
    template_name = "core/register.html"

    def get_success_url(self):
        return resolve_url('core:login')


    def form_valid(self, form):

        form.save()
        return super(RegisterFormView, self).form_valid(form)


class UserInfoView(DetailView):
    queryset = User.objects.all()
    template_name = 'core/userinfo.html'
