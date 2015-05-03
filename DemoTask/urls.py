from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url=reverse_lazy('todo:home'))),
	url(r'^user/', include('UserAccount.urls',namespace='user')),
	url(r'^todo/', include('Todo.urls',namespace='todo')),
    url(r'^admin/', include(admin.site.urls)),
)
