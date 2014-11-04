from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from admins.decorators import active_and_login_required
from calendars.models import *
import calendar as cals
import time


mnames = "January February March April May June July August September October November December"
mnames = mnames.split()
hours = "9am 10am 11am 12am 1pm 2pm 3pm 4pm 5pm 6pm 7pm 8pm"
hours = hours.split()


@active_and_login_required
@csrf_exempt
def calendar(request):
    errors = []
    if request.POST:
        params = request.POST.copy()
        is_public = params['public'] != "false"
        if params['name'] == "":
            return False
        elif MyCalendar.objects.filter(owner=request.user, name=params['name']):
            return False
        else:
            MyCalendar.objects.create_calendar(request.user, params['name'], is_public)

    calendars = MyCalendar.objects.filter(Q(public=True)|Q(owner__username=request.user.username))

    return render(request,
                  'calendars/calendar.html',
                  {"calendars": calendars,
                   "errors": errors})


@active_and_login_required
@csrf_exempt
def by_years(request):
    year = 0
    calendars = MyCalendar.objects.filter(Q(public=True)|Q(owner__username=request.user.username))

    if 'offset' in request.POST:
        year = int(request.POST['offset'])
    else:
        year = time.localtime()[0]

    now_year, now_month = time.localtime()[:2]
    lst = []

    # create a list of months for each year, indicating ones that contain events and current
    mlst = []
    for n, month in enumerate(mnames):
        current = False   # are there entry(s) for this month; current month?
        events = MyEvent.objects.filter(start__year=year, start__month=n+1, mycalendar__in=calendars)
        entry = len(events)
        if n+1 == now_month:
            current = True
        mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
    lst.append((now_year, mlst))
    return render(request,
                  "calendars/calendar_year.html",
                  {"years": lst,
                   "user": request.user,
                   "current_year":year,
                   "mlst": mlst})


@active_and_login_required
@csrf_exempt
def by_month(request):
    calendars = MyCalendar.objects.filter(Q(public=True)|Q(owner__username=request.user.username))

    year, month = time.localtime()[:2]
    if 'offset' in request.POST:
        year, month = request.POST['offset'].split(" ")
        year = int(year)
        month = int(month)
    cal = cals.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    for day in month_days:
        events = current = False
        if day:
            events = MyEvent.objects.filter(start__year=year, start__month=month, start__day=day, mycalendar__in=calendars)
            if day == nday and year == nyear and month == nmonth:
                current = True

        lst[week].append((day, events, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render(request,
                  "calendars/calendar_month.html",
                  {"year":year,
                   "month":month,
                   "user": request.user,
                   "month_days":lst,
                   "mname":mnames[month-1]})



@active_and_login_required
@csrf_exempt
def by_week(request):
    calendars = MyCalendar.objects.filter(Q(public=True)|Q(owner__username=request.user.username))

    today = datetime.date.today()
    if 'date' in request.POST:
        month, day, year = request.POST['date'].split("/")
        today = datetime.date(year=int(year), month=int(month), day=int(day))
    if 'offset' in request.POST:
        year, month, day = request.POST['offset'].split(" ")
        today = datetime.date(year=int(year), month=int(month), day=int(day))
    weekday = today.weekday()
    start_delta = datetime.timedelta(days=weekday)
    start_of_week = today - start_delta
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]

    nyear, nmonth, nday = time.localtime()[:3]
    lst = []

    for day in week_dates:
        current = False
        events = MyEvent.objects.filter(start__year=day.year, start__month=day.month, start__day=day.day, mycalendar__in=calendars)
        if day.day == nday and day.year == nyear and day.month == nmonth:
            current = True
        lst.append((day, events, current))
    return render(request,
                  "calendars/calendar_week.html",
                  {"weekdays": lst,
                   "hours": hours,
                   "start_of_week": start_of_week})


@active_and_login_required
@csrf_exempt
def by_day(request):
    calendars = MyCalendar.objects.filter(Q(public=True)|Q(owner__username=request.user.username))
    today = datetime.datetime.today()
    if 'offset' in request.POST:
        year, month, day = request.POST['offset'].split(" ")
        today = datetime.date(year=int(year), month=int(month), day=int(day))
    delta = datetime.timedelta(days=1)
    events = MyEvent.objects.filter(start__year=today.year, start__month=today.month, start__day=today.day, mycalendar__in=calendars)
    return render(request,
                  "calendars/calendar_day.html",
                  {"today": today,
                   "delta": delta,
                   "hours": hours,
                   "events": events})

@active_and_login_required
@csrf_exempt
def event(request):
    errors = []
    if request.POST:
        post_params = request.POST.copy()
        params = {}
        if not request.POST['start']:
            errors.append('No starting Date for the Event')
        if not request.POST['end']:
            errors.append('No ending Date for the Event')
        if not errors:
            start_year, start_month, start_day = post_params['start'].split('-')
            end_year, end_month, end_day = post_params['end'].split('-')
            start_hours, start_minutes = post_params['from_time'].split(':')
            end_hours, end_minutes = post_params['to_time'].split(':')
            current_cal = MyCalendar.objects.get(pk=post_params['choose_calendar'])

            params['start'] = datetime.datetime(year=int(start_year),
                                                month=int(start_month),
                                                day=int(start_day),
                                                hour=int(start_hours),
                                                minute=int(start_minutes))
            params['end'] =  datetime.datetime(year=int(end_year),
                                               month=int(end_month),
                                               day=int(end_day),
                                               hour=int(end_hours),
                                               minute=int(end_minutes))
            params['creator'] = request.user
            params['title'] = post_params['title']
            params['mycalendar'] = current_cal
            params['description'] = post_params['description']
            MyEvent.objects.new_event(participants=[], **params)

            return HttpResponseRedirect('/calendar/')

    calendars = MyCalendar.objects.filter(Q(public=True)|Q(owner__username=request.user.username))
    return render(request,
                  "calendars/event.html",
                  {"calendars": calendars,
                   "errors": errors})

@active_and_login_required
@csrf_exempt
def details_event(request):
    if request.POST:
        event = MyEvent.objects.get(pk=request.POST['id_event'])
        return render(request,
                      "calendars/details_event.html",
                      {"event": event})