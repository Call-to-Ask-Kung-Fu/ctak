from django.conf.urls import patterns, url
from .views import detail, listshow, new_project, ProjectDelete, projectmanage, listbyp

urlpatterns = patterns('',
    # Examples:
    url(r'^$', new_project, name='newproject'),
    url(r'^(?P<project_id>\d+)/$', detail, name='htmldetail'),
    url(r'^producer/(?P<producer_id>\d+)/$', listbyp, name='listbyp'),
    url(r'^list/$', listshow, name='htmllist'),
    url(r'^projectmanage/$', projectmanage, name='projectmanage'),
    url(r'^(?P<pk>\d+)/delete/$', ProjectDelete.as_view(), name='projectdelete'),
)
