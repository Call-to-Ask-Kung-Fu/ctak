from django.conf.urls import patterns, url
from .views import detail, listshow, Create

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Create, name='createqr'),
    url(r'^(?P<qr_id>\d+)/$', detail, name='qrdetail'),
    url(r'^list/$', listshow, name='qrlist'),

)
