from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from CMSYapster import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CMSYapster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'admins.views.login_user'),
    url(r'^home/', 'stats.views.homepage'),
    url(r'^statistics/$', 'stats.views.stats'),
    url(r'^search/$', 'stats.views.search'),
    url(r'^announcements/', 'admins.views.annoucements_manage'),
    url(r'^cmsusers/$', 'admins.views.users_manage'),
    url(r'^cmsusers/(?P<username>[a-zA-Z0-9_.-]+)/$', 'admins.views.cmsuser'),
    url(r'^users/(?P<username>[a-zA-Z0-9_.-]+)/$', 'admins.views.profile'),
    url(r'^hashtag/(?P<tag>[a-zA-Z0-9_.-]+)/$', 'stats.views.hashtag'),
    url(r'^group/(?P<tag>[a-zA-Z0-9_.-]+)/$', 'stats.views.group_page'),
)