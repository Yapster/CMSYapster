from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView

from wiki.views import *

urlpatterns = patterns(
    '',
    url(r'search/', 'wiki.views.search_results'),
    url(r'bookmarks/$', 'wiki.views.bookmarks'),
    url(r'save_favorite/$', 'wiki.views.save_bookmark'),
    url(r'del_favorite/$', 'wiki.views.del_bookmark'),
    url(r'recently_viewed/$', 'wiki.views.recently_viewed'),
    url(r'^new/edit/$', 'wiki.views.new_article'),
    url(r'^(?P<page>[a-zA-Z0-9_.-]+)/section/new/edit/$', 'wiki.views.new_section'),
    url(r'^(?P<page>[a-zA-Z0-9_.-]+)/section/(?P<section>[a-zA-Z0-9_.-]+)/edit/$', 'wiki.views.edit_section'),
    url(r'^(?P<page>[a-zA-Z0-9_.-]+)/edit/$', 'wiki.views.edit_article'),
    url(r'^(?P<page>[a-zA-Z0-9_.-]+)/$', 'wiki.views.article'),
    url(r'', 'wiki.views.home'),
    )