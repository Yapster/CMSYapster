from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView

from cms_reports.models import *

urlpatterns = patterns(
    '',
    url(r'post/take_in_charge/', 'cms_reports.views.post_actions'),
    url(r'post/checked/', 'cms_reports.views.post_actions'),
    url(r'^(?P<report_id>[a-zA-Z0-9_.-]+)/$', 'cms_reports.views.report'),
    url(r'', 'cms_reports.views.reports'),
    )