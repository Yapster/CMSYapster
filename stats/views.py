from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from announcements.models import Announcement
from location.models import *
from chat.signals import *
from yap.views import HomePageStatistics
from cms_location.models import *

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


def stats_yaps(request):

    return render(request, 'stats/statistics.html', {})

@login_required(login_url='/login/')
@csrf_exempt
def stats_usership(request):
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()

    # Statistiques handling
    countries = CmsCountry.objects.all()
    datas = HomePageStatistics.get_users_stats(request).data.items()

    return render(request, 'stats/statistics.html', {"announcements": announcements,
                                                     "user": request.user,
                                                     "conversations": conversations,
                                                     "countries": countries,
                                                     "datas": datas})


@login_required(login_url='/login')
@csrf_exempt
def stats_yaps(request):
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()

# Statistiques handling
    countries = CmsCountry.objects.all()
    datas = HomePageStatistics.get_yaps_stats(request).data.items()

    return render(request, 'stats/statistics.html', {"announcements": announcements,
                                                     "user": request.user,
                                                     "conversations": conversations,
                                                     "countries": countries,
                                                     "datas": datas})

@csrf_exempt
def more_data_usership(request):
    datas = HomePageStatistics.get_users_stats(request).data.items()
    datas_month = HomePageStatistics.get_users_stats(request, _time=43829.0639).data
    datas_week = HomePageStatistics.get_users_stats(request, _time=10080).data
    datas_day = HomePageStatistics.get_users_stats(request, _time=1440).data
    datas_hour = HomePageStatistics.get_users_stats(request, _time=60).data
    datas_min = HomePageStatistics.get_users_stats(request, _time=1).data
    more_data = True
    return render(request, 'stats/more_stats.html', {"datas": datas,
                                                     "more_data": more_data,
                                                     "datas_month": datas_month,
                                                     "datas_week": datas_week,
                                                     "datas_day": datas_day,
                                                     "datas_hour": datas_hour,
                                                     "datas_min": datas_min})

@csrf_exempt
def more_data_yaps(request):
    datas = HomePageStatistics.get_yaps_stats(request).data.items()
    datas_month = HomePageStatistics.get_yaps_stats(request, _time=43829.0639).data
    datas_week = HomePageStatistics.get_yaps_stats(request, _time=10080).data
    datas_day = HomePageStatistics.get_yaps_stats(request, _time=1440).data
    datas_hour = HomePageStatistics.get_yaps_stats(request, _time=60).data
    datas_min = HomePageStatistics.get_yaps_stats(request, _time=1).data
    more_data = True
    return render(request, 'stats/more_stats.html', {"datas": datas,
                                                     "more_data": more_data,
                                                     "datas_month": datas_month,
                                                     "datas_week": datas_week,
                                                     "datas_day": datas_day,
                                                     "datas_hour": datas_hour,
                                                     "datas_min": datas_min})

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


def home_stats(request):
    stats = HomePageStatistics.get_teasing_stats(request).data.items()

    return render(request, 'sub_templates/home_stats.html', {"stats": stats})

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
        new_data = HomePageStatistics.get(request,
                                          country=request.POST['country'],
                                          state=state,
                                          city=city,
                                          gender=request.POST['gender'],
                                          min_age=request.POST['from_age'],
                                          max_age=request.POST['to_age']
        ).data.items()
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