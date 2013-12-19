from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from freeper import settings
from web.views import AppView
from api.views import FacebookApiView, SaveApiView, ResetApiView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'freeper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', AppView.as_view(), name='app_index'),

    url(r'^api/friendlist/sync/$', SaveApiView.as_view(), name='api_save'),
    url(r'^api/friendlist/reset/$', ResetApiView.as_view(), name='api_reset'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()