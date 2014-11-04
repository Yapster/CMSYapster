from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.admin import User
#from schedule.models import *
import random


class MyEventManager(models.Manager):
    def new_event(self, participants=[], **kwargs):
        new = self.create(**kwargs)
        cal = MyCalendar.objects.get(pk=kwargs.pop('mycalendar'))
        cal.my_events.add(new)
        for part in participants:
            new.participants.add(part)
        return new


class MyEvent(Event):
    participants = models.ManyToManyField(to=User, related_name='participants')
    mycalendar = models.ForeignKey('MyCalendar', related_name='mycalendar')
    objects = MyEventManager()


class MyCalendarManager(models.Manager):
    def create_calendar(self, user, name, public=False):
        try:
            calendar = self.create()
            calendar.owner.add(user)
            calendar.name = name
            calendar.public = public
            r = lambda: random.randint(0,255)
            calendar.color = ('%02X%02X%02X' % (r(),r(),r()))
            calendar.save()
            return calendar
        except:
            return None

    def get_calendars(self, user):
        try:
            calendars = self.filter(owner=user)
            return calendars
        except ObjectDoesNotExist:
            return None

    def get_calendar(self, user):
        try:
            calendar = self.filter(owner=user)[0]
            return calendar
        except ObjectDoesNotExist:
            return None

    def delete_calendar(self, pk):
        try:
            self.get(pk).delete()
            return True
        except:
            return False


class MyCalendar(Calendar):
    owner = models.ManyToManyField(to=User, related_name='owner')
    color = models.CharField(max_length=6, default="15D400")
    my_events = models.ManyToManyField(to=MyEvent, related_name='my_events')
    is_active = models.BooleanField(default=True)
    public = models.BooleanField(default=False)
    objects = MyCalendarManager()

    def set_color(self, color):
        events = self.my_events.all()
        for e in events:
            e.color = color
            e.save()
        self.color = color
        self.save()
