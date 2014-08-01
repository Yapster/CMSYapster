from django.db import models
from django.contrib.auth.admin import User
from schedule.models import *

class MyEvent(Event):
    id_event = models.AutoField(primary_key=True)
    calendars = models.ManyToManyField(to='MyCalendar', null=True, blank=True, related_name='calendars')

class MyCalendar(Calendar):
    id_calendar = models.AutoField(primary_key=True)
    events = models.ManyToManyField(to='MyEvent', null=True, blank=True, related_name='events')
    owner = models.ForeignKey(to=User, related_name='owner')