from django.conf.urls import patterns, include, url
from django.contrib import admin

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
    url(r'^announcements/$', 'announcements.views.annoucements_manage'),
    url(r'^contacts/$', 'contacts.views.contacts_lists'),
    url(r'^contacts/lists/(?P<list>[a-zA-Z0-9_.-]+)/$', 'contacts.views.contacts_lists_details'),
    url(r'^contacts/lists/(?P<list>[a-zA-Z0-9_.-]+)/contacts/(?P<contact>[a-zA-Z0-9_.-]+)/$', 'contacts.views.contacts_details'),
    url(r'^permissionsgroups/$', 'groups.views.group_manage'),
    url(r'^permissionsgroups/(?P<group>[a-zA-Z0-9_.-]+)/$', 'groups.views.group_details'),
    url(r'^cmsusers/$', 'admins.views.users_manage'),
    url(r'^cmsusers/(?P<username>[a-zA-Z0-9_.-]+)/$', 'admins.views.cmsuser'),
    url(r'^cmsusers/(?P<username>[a-zA-Z0-9_.-]+)/edit/$', 'admins.views.edit_cmsuser'),
    url(r'^users/(?P<username>[a-zA-Z0-9_.-]+)/$', 'admins.views.profile'),
    url(r'^users/(?P<username>[a-zA-Z0-9_.-]+)/photos/$', 'admins.views.edit_profile_pic'),
    url(r'^hashtag/(?P<tag>[a-zA-Z0-9_.-]+)/$', 'stats.views.hashtag'),
    url(r'^group/(?P<group>[a-zA-Z0-9_.-]+)/$', 'stats.views.group_page'),
    url(r'^$', 'stats.views.homepage'),
)