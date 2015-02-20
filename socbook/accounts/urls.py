from django.conf.urls import patterns, url


urlpatterns = patterns('accounts.views',
                       url(r'', 'signin'),
                       url(r'^signin/$', 'signin', name='signin'),
                       url(r'^signup/$', 'signup', name='signup'),
                       url(r'^signout/$', 'signout', name='signout'),
                       url(r'^settings/$', 'account_settings', name='settings'),
                       url(r'^password_forgotten/', 'password_forgotten', name='password_forgotten'),
                       url(r'^settings/account/$', 'account_settings', name='account_settings'),
                       url(r'^settings/password/$', 'password_settings', name='password_settings'),
                       url(r'^settings/picture/$', 'picture_settings', name='picture_settings'),
                       url(r'^settings/friends/$', 'friends_settings', name='friends_settings'),
                       url(r'^(?P<username>\w+)/$', 'profile', name='profile')
)
