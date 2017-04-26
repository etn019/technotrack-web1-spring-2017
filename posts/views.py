# coding: utf-8
import time, json
from django import forms
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, resolve_url, HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View

from comments.models import Comment
from models import Blog, Post, Like


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description')

        # title = forms.CharField()
        # description = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=(
        ('title', u'по заголовку'),
        ('updated_at', u'по дате обновления'),
        ('description', u'по описанию')
    )
    )
    search = forms.CharField(required=False)


class CreateBlog(CreateView):
    form_class = BlogForm
    template_name = 'posts/addblog.html'
    model = Blog

    # fields = ('title', 'description')

    def get_success_url(self):
        return resolve_url('posts:showBloglist')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        resp = super(CreateBlog, self).form_valid(form)
        return HttpResponse("ok")


class EditBlog(UpdateView):
    template_name = 'posts/editblog.html'
    model = Blog
    fields = ('title', 'description')
    blogobject = None

    def get_success_url(self):
        return resolve_url('posts:showBloglist')

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.blogobject = get_object_or_404(Blog, id=pk)
        return super(EditBlog, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(EditBlog, self).get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(EditBlog, self).get_context_data(**kwargs)
        context['blog'] = self.blogobject
        return context

    def form_valid(self, form):
        resp = super(EditBlog, self).form_valid(form)
        return HttpResponse("ok")


class CreatePost(CreateView):
    form_class = PostForm
    template_name = 'posts/addpost.html'
    model = Post
    # fields = ('title', 'text', 'blog')
    blogobject = None

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.blogobject = get_object_or_404(Blog, id=pk)
        return super(CreatePost, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = self.blogobject
        resp = super(CreatePost, self).form_valid(form)
        return HttpResponse('ok')

    def get_success_url(self):
        return resolve_url('posts:showBlog', pk=self.blogobject.id)

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context['blog'] = self.blogobject
        return context


class EditPost(UpdateView):
    form_class = PostForm
    template_name = 'posts/editpost.html'
    model = Post
    postobject = None

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.postobject = get_object_or_404(Post, id=pk)
        return super(EditPost, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('posts:showComments', pk=self.postobject.id)

    def get_context_data(self, **kwargs):
        context = super(EditPost, self).get_context_data(**kwargs)
        context['post'] = self.postobject
        return context

    def get_queryset(self):
        return super(EditPost, self).get_queryset().filter(author=self.request.user)

    def form_valid(self, form):
        resp = super(EditPost, self).form_valid(form)
        return HttpResponse("ok")


class BlogList(ListView):
    queryset = Blog.objects.all()
    template_name = 'posts/blogs.html'
    sortform = None

    def dispatch(self, request, *args, **kwargs):
        self.sortform = SortForm(self.request.GET)
        return super(BlogList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['sortform'] = self.sortform
        return context

    def get_queryset(self):
        qs = super(BlogList, self).get_queryset()
        if self.sortform.is_valid():
            qs = qs.order_by(self.sortform.cleaned_data['sort'])
            if self.sortform.cleaned_data['sort'] == 'updated_at':
                qs = qs.reverse()
            if self.sortform.cleaned_data['search']:
                qs = qs.filter(title__icontains=self.sortform.cleaned_data['search'])
        return qs


class BlogView(DetailView):
    queryset = Blog.objects.all()
    template_name = 'posts/blog.html'


class PostView(DetailView):
    queryset = Post.objects.all()
    template_name = 'posts/post.html'


class CommentsView(DetailView):
    queryset = Post.objects.all()
    template_name = 'posts/commentsdiv.html'


class PostDetail(CreateView):
    model = Comment
    template_name = 'posts/post.html'
    fields = ('text',)

    def get_success_url(self):
        return resolve_url('posts:showComments', pk=self.postobject.id)

    def form_valid(self, form):
        form.instance.post = self.postobject
        form.instance.author = self.request.user
        return super(PostDetail, self).form_valid(form)

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.postobject = get_object_or_404(Post, id=pk)
        return super(PostDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = self.postobject
        context['likesnumber'] = self.postobject.likes.count()
        context['isLiked'] = self.postobject.likes.filter(liker=self.request.user).exists()
        return context


class PostList(ListView):
    queryset = Post.objects.all().order_by("created_at").reverse()
    template_name = "posts/feed.html"

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        liked_by_user = []
        for post in self.queryset:
            if post.likes.filter(liker=self.request.user).exists():
                liked_by_user.append(int(post.id))
        context['liked_by_user'] = liked_by_user
        return context


class PostLikeAjaxView(View):
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.postobject = get_object_or_404(Post, id=pk)
        return super(PostLikeAjaxView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        if not self.postobject.likes.filter(liker=self.request.user).exists():
            like = Like(post=self.postobject, liker=self.request.user)
            like.save()
        else:
            Like.objects.filter(liker=self.request.user, post=self.postobject).delete()
        self.postobject.liked = Like.objects.filter(post=self.postobject).count()
        self.postobject.save()

        return HttpResponse(self.postobject.likes.filter(liker=self.request.user).exists())

    def get(self, request):
        likers = []

        response_data = {}

        for like in self.postobject.likes.all():
            response_data[like.liker.id] = like.liker.username


        #for like in self.postobject.likes.all():
         #   likers.append(like.liker.id)
        #print likers
        print response_data
        if self.request.user.id in likers:
            likers.remove(self.request.user.id)
            likers.insert(0, self.request.user.id)
        print likers
        return JsonResponse(response_data)
