from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('accounts.urls', namespace='accounts')),

                       url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
                           {'template_name': 'password_reset.html'}, name='password_reset'),
                       url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'},
                           name='password_reset_done'),
                       url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
                       url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_done.html'},
                           name='password_reset_complete'),
                       )
