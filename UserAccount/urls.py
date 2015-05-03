from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login/', 'UserAccount.views.login', name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
    url(r'^logout/$', 'UserAccount.views.logout', name='logout'),
    url(r'^signup/$', 'UserAccount.views.signup', name='signup'),
)