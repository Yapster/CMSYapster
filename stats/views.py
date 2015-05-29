from boto.connection import HTTPResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from announcements.models import Announcement
from location.models import *
from chat.signals import *
from yap.views import HomePageStatistics
from cms_location.models import *
from yap.sub_views import get_home_data, get_users_data, get_yaps_data, get_country_data, get_hashtags_data, get_listens_data, get_reyaps_data
from stats.tools import *

import logging

logger = logging.getLogger(__name__)



@login_required(login_url='/login/')
@csrf_exempt
def homepage(request):
    """
    Display general stats
    """

    announcements = Announcement.objects.all()
    users = User.objects.exclude(username=request.user.username)
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')

    return render(request, 'stats/home.html', {"announcements": announcements,
                                               "conversations": conversations,
                                               "user": request.user,
                                               "chaters": users})


@login_required(login_url='/login/')
@csrf_exempt
def stats_usership(request):
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()

    # Statistiques handling
    countries = CmsCountry.objects.all()

    return render(request, 'stats/statistics.html', {"announcements": announcements,
                                                     "user": request.user,
                                                     "conversations": conversations,
                                                     "countries": countries,
                                                     "type": "usership"})


@login_required(login_url='/login')
@csrf_exempt
def stats_yaps(request):
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()

    # Statistiques handling
    countries = CmsCountry.objects.all()

    return render(request, 'stats/statistics.html', {"announcements": announcements,
                                                     "user": request.user,
                                                     "conversations": conversations,
                                                     "countries": countries,
                                                     "type": "yaps"})


@login_required(login_url='/login')
@csrf_exempt
def stats_reyaps(request):
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()

    # Statistiques handling
    countries = CmsCountry.objects.all()

    return render(request, 'stats/statistics.html', {"announcements": announcements,
                                                     "user": request.user,
                                                     "conversations": conversations,
                                                     "countries": countries,
                                                     "type": "reyaps"})


@login_required(login_url='/login')
@csrf_exempt
def stats_listens(request):
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()

    # Statistiques handling
    countries = CmsCountry.objects.all()

    return render(request, 'stats/statistics.html', {"announcements": announcements,
                                                     "user": request.user,
                                                     "conversations": conversations,
                                                     "countries": countries,
                                                     "type": "listens"})

@csrf_exempt
def home_stats(request):
    """
    Display stats for
    """
    #stats = HomePageStatistics.get_teasing_stats(request).data.items()
    kwargs = {"time_start": datetime.datetime.now()}
    data = get_home_data(**kwargs)
    print data
    return render(request, 'sub_templates/home_stats.html', {"data": data})


@csrf_exempt
def more_data(request):
    """
    Called by Javascript load_col_stats()
    Display one column of Data, depending one _time
    if time_end == null => Now
    :param request:
    :return:
    """

    specific_data = None
    time_start = datetime.datetime.now() - datetime.timedelta(minutes=int(request.POST['time']))
    # TODO: Get time_end and convert to date time
    #if request.POST['time_end']:

    kwargs = {"time_start": time_start}
    time = float(request.POST['time'])
    type_stats = request.POST['type_stats']
    if type_stats == 'usership':
        #specific_data = HomePageStatistics.get_users_stats(request, _time=time).data.items()
        specific_data = get_users_data(**kwargs)
    elif type_stats == 'yaps':
        #specific_data = HomePageStatistics.get_yaps_stats(request, _time=time).data.items()
        specific_data = get_yaps_data(**kwargs)
    elif type_stats  == 'reyaps':
        specific_data = get_reyaps_data(**kwargs)
    elif type_stats == 'listens':
        specific_data = get_listens_data(**kwargs)
    elif type_stats == 'countries':
        specific_data = get_country_data(**kwargs)
    elif type_stats == 'hashtags':
        specific_data = get_hashtags_data(**kwargs)
    return render(request,
                  'stats/sub_templates/col_stats_div.html',
                  {"specific_data": specific_data,
                   "type_time": request.POST['type_time'],
                   "interval": request.POST['time'],
                   "type_stats": request.POST['type_stats']})


@csrf_exempt
def more_data_yaps(request):
    datas = HomePageStatistics.get_yaps_stats(request).data.items()

    datas_year = HomePageStatistics.get_yaps_stats(request, _time=525949).data
    datas_month = HomePageStatistics.get_yaps_stats(request, _time=43829.0639).data
    datas_week = HomePageStatistics.get_yaps_stats(request, _time=10080).data

    more_data = True
    return render(request, 'stats/more_stats.html', {"datas": datas,
                                                     "more_data": more_data,
                                                     "datas_year": datas_year,
                                                     "datas_month": datas_month,
                                                     "datas_week": datas_week})


@login_required(login_url='/login/')
def search(request):
    """
    Display research view
    """
    if 'search_button' in request.POST:
        searchexp = request.POST['searchexp']
        postdate = request.POST['postdate']
        birthday = request.POST['birthday']
        numbers = request.POST['numbers']
        registerdate = request.POST['registerdate']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()

    return render(request, 'search/index.html',{"announcements": announcements,
                                                "user": request.user,
                                                "conversations": conversations})


@csrf_exempt
def spec_stats(request):
    """
    get stats for a specific stat en return the graph
    @:param start_time, end_time = for Graph if not, all time
    @:param type_stats = User, Hashtag, Yap, Reyap...
    @:return Html for one stat
    """
    global stat_method
    data = []
    if request.POST:
        # Set parameters for method

        now = datetime.datetime.now()
        time_start = now - datetime.timedelta(minutes=int(request.POST['time_start']))
        if 'time_end' not in request.POST:
            time_end = now
        else:
            time_end = now - datetime.timedelta(minutes=int(request.POST['time_end']))
        kwargs = {'time_start': time_start,
                  'time_end': time_end,
                  'type_search': request.POST['type_search']}

        stat_method = get_stat_method(request.POST['name_method'], request.POST['type_stats'])
        data = stat_method(**kwargs)
    return render(request, "stats/sub_templates/spec_stats.html", {"data": data,
                                                                   "title": request.POST['name_method'],
                                                                   "time_start": time_start,
                                                                   "time_end": time_end,
                                                                   "type_stats": request.POST['type_stats']})


@csrf_exempt
def custom_graph(request):
    """
    Return graph with specific start and end datetime, accuracy
    """
    global stat_method
    errors = []
    data = None

    stat_method = get_stat_method(request.POST['name_method'], request.POST['type_stats'])
    time_start = get_time(request.POST['date_start'], request.POST['time_start'])
    time_end = get_time(request.POST['date_end'], request.POST['time_end'])
    if not time_start:
        errors.append("Start time error: the start time is not valid")
    if not time_end:
        errors.append("End time error: the end time is not valid")
    kwargs = {
        'time_start': time_start,
        'time_end': time_end,
        'type_search': request.POST['type_search'],
        'accuracy': int(request.POST['accuracy'])
    }
    if time_end and time_start:
        data = stat_method(**kwargs)

    return render(request, "stats/sub_templates/spec_stats.html", {"data": data,
                                                                   "title": request.POST['name_method'],
                                                                   "time_start": time_start,
                                                                   "time_end": time_end,
                                                                   "errors": errors})


@csrf_exempt
def location_option(request):
    if 'country' in request.POST:
        if request.POST['country'] == '184':
            states = CmsUSState.objects.all()
            return render(request, 'stats/location_option.html', {"states": states})
        cities = CmsCity.objects.filter(country=CmsCountry.objects.get(pk=request.POST['country']))
        if not cities:
            return False
        return render(request, 'stats/location_option.html', {"cities": cities})

    if 'state' in request.POST:
        cities = CmsCity.objects.filter(us_state=USState.objects.get(pk=request.POST['state']))
        if not cities:
            return False
        return render(request, 'stats/location_option.html', {"cities": cities})
    return

# @csrf_exempt
# def export_pdf(request):
#     return render_to_pdf("stats/export_pdf.html",
#         {
#             'pagesize': 'A4',
#         })

@csrf_exempt
def specific_search(request):
    #Add line depending search
    if 'new_line' in request.POST:
        logger.warning(request.POST)
        state = 0
        city = 0
        if 'state' in request.POST:
            state = request.POST['state']
        if 'city' in request.POST:
            city = request.POST['city']
        type_stats = request.POST['type_stats'].split('/')[-2]
        if type_stats == "yaps":
            new_data = HomePageStatistics.get_yaps_stats(request,
                                                         country=request.POST['country'],
                                                         state=state,
                                                         city=city,
                                                         gender=request.POST['gender'],
                                                         min_age=request.POST['from_age'],
                                                         max_age=request.POST['to_age']
            ).data.items()
        elif type_stats == "usership":
            new_data = HomePageStatistics.get_users_stats(request,
                                                          country=request.POST['country'],
                                                          state=state,
                                                          city=city,
                                                          gender=request.POST['gender'],
                                                          min_age=request.POST['from_age'],
                                                          max_age=request.POST['to_age'])
    return render(request, 'stats/specific_search.html', {"new_data": new_data})



    # @login_required(login_url='/login/')
    # def hashtag(request, tag):
    #     """
    #     Display hashtag with count of people that used it and few yaps
    #     """
    #
    #     current_tag = Hashtag.objects.get(name=tag)
    #     return render(request, 'stats/hashtag.html', {'tag': current_tag})
    #
    #
    # @login_required(login_url='/login/')
    # def group_page(request, group):
    #     """
    #     Display group page with count people in it and few yaps
    #     """
    #     current_group = Group.objects.get(pk=group)
    #     return render(request, 'stats/group.html', {'group': current_group})

