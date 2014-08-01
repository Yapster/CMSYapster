from django.shortcuts import render, get_object_or_404
from calendars.models import *

def calendar(request, username):
    c = get_object_or_404(MyCalendar, owner=request.user)

    return render(request,
                  'calendars/calendar.html',
                  {"calendar": c})