from django.conf.urls import patterns, url
from .views import bousou

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qr.views.home', name='home'),
    url(r'^$', bousou, name='bousou'),

)
