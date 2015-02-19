from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('account.views',
    url(r'^admin/', include(admin.site.urls)),
)
