from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from posts.views import BlogList, BlogView, PostView, EditBlog, CreateBlog, CreatePost, PostDetail, EditPost, PostList, PostLikeAjaxView, CommentsView

urlpatterns = [
    url(r'^blogs/$', BlogList.as_view(), name='showBloglist'),
    url(r'^blogs/(?P<pk>\d+)/$', BlogView.as_view(), name='showBlog'),
    url(r'^posts/(?P<pk>\d+)/$', PostDetail.as_view(), name='showComments'),
    url(r'^posts/(?P<pk>\d+)/comments/$', CommentsView.as_view(), name='onlyComments'),
    url(r'^posts/(?P<pk>\d+)/like/$', login_required(PostLikeAjaxView.as_view()), name='post_ajax_like'),
    url(r'^blogs/add/$', login_required(CreateBlog.as_view()), name='createblog'),
    url(r'^blogs/(?P<pk>\d+)/add/$', login_required(CreatePost.as_view()), name='createpost'),
    url(r'^blogs/(?P<pk>\d+)/edit/$', EditBlog.as_view(), name='editblog'),
    url(r'^posts/(?P<pk>\d+)/edit/$', EditPost.as_view(), name='editpost'),
    url(r'^feed/$', PostList.as_view(), name='showFeed'),
]
