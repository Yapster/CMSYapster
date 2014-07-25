from django.conf.urls import patterns, include, url
from django.contrib import admin
from yap.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'CMSYapster.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/', 'admins.views.login_user'),
                       url(r'^home/', 'stats.views.homepage'),
                       url(r'^statistics/usership/$', 'stats.views.stats_usership'),
                       url(r'^statistics/yaps/$', 'stats.views.stats_yaps'),
                       url(r'^get/home_stats/$', 'stats.views.home_stats'),
                       url(r'^get/location_option/$', 'stats.views.location_option'),
                       url(r'^post/specific_search/$', 'stats.views.specific_search'),
                       url(r'^post/more_data/$', 'stats.views.more_data'),
                       url(r'^post/messenger/$', 'chat.views.chat'),
                       url(r'^post/search/$', 'cms_search_log.views.form_fields'),
                       url(r'^post/search/results/$', 'cms_search_log.views.results'),
                       url(r'^search/$', 'stats.views.search'),
                       url(r'^api/$', HomePageStatistics.as_view()),
                       url(r'^announcements/$', 'announcements.views.annoucements_manage'),
                       url(r'^databases/$', 'db_manager.views.home_database'),
                       url(r'^databases/rds/graph/$', 'db_manager.views.graph_rds'),
                       url(r'^databases/rds/(?P<instance>[a-zA-Z0-9_.-]+)/$', 'db_manager.views.rds_details'),
                       url(r'^databases/ec2/(?P<instance>[a-zA-Z0-9_.-]+)/$', 'db_manager.views.ec2_details'),
                       url(r'^contacts/$', 'contacts.views.contacts_lists'),
                       url(r'^contacts/lists/(?P<list>[a-zA-Z0-9_.-]+)/$', 'contacts.views.contacts_lists_details'),
                       url(r'^contacts/lists/(?P<list>[a-zA-Z0-9_.-]+)/contacts/(?P<contact>[a-zA-Z0-9_.-]+)/$', 'contacts.views.contacts_details'),
                       url(r'^permissionsgroups/$', 'groups.views.group_manage'),
                       url(r'^permissionsgroups/(?P<group>[a-zA-Z0-9_.-]+)/$', 'groups.views.group_details'),
                       url(r'^cmsusers/$', 'admins.views.users_manage'),
                       url(r'^cmsusers/(?P<username>[a-zA-Z0-9_.-]+)/edit/$', 'admins.views.edit_cmsuser'),
                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$', 'admins.views.profile'),
                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/photos/$', 'admins.views.edit_profile_pic'),
                       url(r'^$', 'stats.views.homepage'),
                       )