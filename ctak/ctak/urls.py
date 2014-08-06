from django.conf.urls import patterns, include, url
from ctak import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ctak.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^966/qr/', include('qrmaker.urls')),
    url(r'^kihara/bousou/', include('bousoukanji.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
