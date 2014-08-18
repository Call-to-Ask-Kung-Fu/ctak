from django.conf.urls import patterns, include, url
from ctak import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ctak.views.home', name='home'),
    url(r'^bay/lay/good/though/mode/duck/low/$', 'account.views.reg', name='reg'),
    url(r'^success/$', 'ctak.views.success', name='success'),
    url(r'^account/', include('account.urls')),
    url(r'^966/qr/', include('qrmaker.urls')),
    url(r'^kihara/bousou/', include('bousoukanji.urls')),
    url(r'^html/', include('html.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS}),
)
