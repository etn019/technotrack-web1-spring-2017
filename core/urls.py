from django.conf.urls import url
from django.contrib.auth.views import logout, login
from core.views import Index, RegisterFormView, UserInfoView


urlpatterns = [
    url(r'^login/$', login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^register/$', RegisterFormView.as_view(), name='register'),
    url(r'^id(?P<pk>\d+)/$', UserInfoView.as_view(), name='userinfo'),
]