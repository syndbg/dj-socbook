from django.conf.urls import patterns, include, url

urlpatterns = patterns('website.views',
                       url(r'^search/$', 'search', name='search'),
                       url(r'^$', 'index', name='index'),
                       )
