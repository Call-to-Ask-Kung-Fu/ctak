from django.conf.urls import patterns, include, url
from ctak import settings
from django.contrib import admin
from .views import IndexDelete
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ctak.views.home', name='home'),
    url(r'^newindex/$', 'ctak.views.newindex', name='newindex'),
    url(r'^indexmanage/$', 'ctak.views.indexmanage', name='indexmanage'),
    url(r'^ctak/(?P<pk>\d+)/delete/$', IndexDelete.as_view(), name='indexdelete'),
    url(r'^bay/lay/good/though/mode/duck/low/$', 'account.views.reg', name='reg'),
    url(r'^success/$', 'ctak.views.success', name='success'),
    url(r'^account/', include('account.urls')),
    url(r'^qr/', include('qrmaker.urls')),
    url(r'^html/', include('html.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS}),
    url(r'^admin/', include(admin.site.urls)),
)
