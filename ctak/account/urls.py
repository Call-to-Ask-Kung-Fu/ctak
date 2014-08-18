from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^change_password/$', views.changepassword, name='pwchange'),
    url(r'^add_profile/$', views.producer_update.as_view(), name='add_profile'),
    url(r'^producer_info/$', views.producer_info, name='producer_info'),
    url(r'^newavatar/$', views.newavatar, name='newavatar'),
    # url(r'^resetpassword/$', views.password_reset, name='password_reset'),
    # url(r'^resetpassword/passwordsent/$', views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.password_reset_confirm, name='password_reset_confirm'),
    )
