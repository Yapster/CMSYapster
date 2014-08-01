from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView

from calendars.models import *

urlpatterns = patterns(
    '',
    url(r'^calendar/(?P<username>[a-zA-Z0-9_.-]+)/', 'calendars.views.calendar'),
    )