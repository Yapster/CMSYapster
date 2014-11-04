from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView

from calendars.models import *

urlpatterns = patterns(
    '',
    url(r'^new/$', 'cms_channels.views.new_channel'),
    url(r'^update_pix/$', 'cms_channels.views.channel'),
    url(r'^(?P<id>[a-zA-Z0-9_.-]+)/$', 'cms_channels.views.channel'),
    )