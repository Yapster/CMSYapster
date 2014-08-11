from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView

from calendars.models import *

urlpatterns = patterns(
    '',
    url(r'details_event/$', 'calendars.views.details_event'),
    url(r'event/', 'calendars.views.event'),
    url(r'year/$', 'calendars.views.by_years'),
    url(r'month/$', 'calendars.views.by_month'),
    url(r'week/$', 'calendars.views.by_week'),
    url(r'day/$', 'calendars.views.by_day'),
    url(r'', 'calendars.views.calendar'),
    )