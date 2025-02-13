from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView

from calendars.models import *

urlpatterns = patterns(
    '',
    url(r'update_task/$', 'tasks.views.update_task'),
    url(r'new_task/$', 'tasks.views.update_task'),
    url(r'save_members/$', 'tasks.views.save_members'),
    url(r'new_note/$', 'tasks.views.new_note'),
    url(r'', 'tasks.views.tasks'),
    )