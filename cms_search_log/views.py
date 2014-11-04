from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from psycopg2 import _param_escape
from datetime import date
from cms_location.models import *
from cms_search_log.models import *
from cms_search_log.tools import *
from cms_search_log.queries import *
from yap.models import *
from report.models import *


@csrf_exempt
def form_fields(request):
    if 'type_search' in request.POST:
        if request.POST['type_search'] == "1":
            countries = CmsCountry.objects.all()
            cities = CmsCity.objects.all()
            states = CmsUSState.objects.all()
            return render(request, "search/form_users.html", {"countries": countries,
                                                              "cities": cities,
                                                              "states": states})
        if request.POST['type_search'] == "2":
            return render(request, "search/form_yaps.html", {})
        if request.POST['type_search'] == "3":
            return render(request, "search/form_reyaps.html", {})
        if request.POST['type_search'] == "4":
            return render(request, "search/form_likes.html", {})
        if request.POST['type_search'] == "5":
            return render(request, "search/form_listens.html", {})
        if request.POST['type_search'] == "6":
            return render(request, "search/form_channels.html", {})
        if request.POST['type_search'] == "7":
            return render(request, "search/form_hashtags.html", {})
        if request.POST['type_search'] == "8":
            return render(request, "search/form_reports.html", {})
    return

@csrf_exempt
def results(request):
    if 'form' in request.POST:
        params = get_params(request.POST['form'])
        params['current_user'] = request.user
        CmsSearchLog.create(params)
        kwargs = {}
        if params['type_search'] == "1":
            if 'user_id' in params:
                kwargs['id'] = params['user_id']
            if 'username' in params:
                kwargs['username__startswith'] = params['username']
            if 'firstname' in params:
                kwargs['first_name__startswith'] = params['firstname']
            if 'lastname' in params:
                kwargs['last_name__startswith'] = params['lastname']
            if 'email' in params:
                kwargs['email__startswith'] = params['email']
            if 'phone_number' in params:
                kwargs['profile__phone_number__startswith'] = params['phone_number']
            if 'gender'in params and params['gender'] != 'N':
                kwargs['profile__gender'] = params['gender']
            if params['country'] != "0":
                kwargs['profile__user_country_id'] = params['country']
            if 'state'in params and params['state'] != "0":
                kwargs['profile__user_us_state_id'] = params['state']
            if 'city' in params and params['city'] != "0":
                kwargs['profile__user_city_id'] = params['city']
            if 'is_inactive' in params:
                kwargs['is_active'] = False
            users = User.objects.using('ye_1_db_1').filter(**kwargs)
            return render(request,
                          "listings/users.html",
                          {"users": users,
                           "title": "Results Search"})
        if params['type_search'] == "2":
            if 'yap_id' in params:
                kwargs['yap_id'] = params['yap_id']
            if 'user_id' in params:
                kwargs['user_id'] = params['user_id']
            if 'title' in params:
                kwargs['title__startswith'] = params['title']
            # if 'hashtag' in params:
            #     kwargs['hashtags__'] = params['hashtag']
            if 'channel' in params:
                kwargs['channel__channel_name__startswith'] = params['channel']
            if 'max_length' in params:
                kwargs['length__lte'] = params['max_length']
            if 'min_length' in params:
                kwargs['length__gte'] = params['min_length']
            if 'max_listens' in params:
                kwargs['listen_count__lte'] = params['max_listens']
            if 'min_listens' in params:
                kwargs['listen_count__gte'] = params['min_listens']
            if 'max_reyaps' in params:
                kwargs['reyap_count__lte'] = params['max_reyaps']
            if 'min_reyaps' in params:
                kwargs['reyap_count__gte'] = params['min_reyaps']
            if 'max_likes' in params:
                kwargs['like_count__lte'] = params['max_likes']
            if 'min_likes' in params:
                kwargs['like_count__gte'] = params['min_likes']
            if 'date_created' in params:
                year, month, day = params['date_created'].split('-')
                kwargs['date_created__startswith'] = date(int(year), int(month), int(day))
            if 'date_deleted' in params:
                year, month, day = params['date_created'].split('-')
                kwargs['deleted_date__startswith'] = date(int(year), int(month), int(day))
            if 'is_inactive' in params:
                kwargs['is_active'] = False
            if 'user_is_inactive' in params:
                kwargs['is_user_deleted'] = True
            yaps = Yap.objects.filter(**kwargs)
            return render(request,
                          "listings/yaps.html",
                          {"yaps": yaps,
                           "title": "Results Search"})
        if params['type_search'] == "3":
            if 'reyap_id' in params:
                kwargs['reyap_id'] = params['reyap_id']
            if 'user_id' in params:
                kwargs['user_id'] = params['user_id']
            if 'yap_id' in params:
                kwargs['yap_id'] = params['yap_id']
            # if 'hashtag' in params:
            #     kwargs['hashtags__'] = params['hashtag']
            if 'title_yap' in params:
                kwargs['yap__title__startswith'] = params['title_yap']
            if 'max_listens' in params:
                kwargs['listen_count__lte'] = params['max_listens']
            if 'min_listens' in params:
                kwargs['listen_count__gte'] = params['min_listens']
            if 'max_reyaps' in params:
                kwargs['reyap_count__lte'] = params['max_reyaps']
            if 'min_reyaps' in params:
                kwargs['reyap_count__gte'] = params['min_reyaps']
            if 'max_likes' in params:
                kwargs['like_count__lte'] = params['max_likes']
            if 'min_likes' in params:
                kwargs['like_count__gte'] = params['min_likes']
            if 'date_created' in params:
                year, month, day = params['date_created'].split('-')
                kwargs['date_created__startswith'] = date(int(year), int(month), int(day))
            if 'date_deleted' in params:
                year, month, day = params['date_created'].split('-')
                kwargs['deleted_date__startswith'] = date(int(year), int(month), int(day))
            if 'is_unreyapped' in params:
                kwargs['is_unreyapped'] = True
            if 'is_inactive' in params:
                kwargs['is_active'] = False
            if 'user_is_inactive' in params:
                kwargs['is_user_deleted'] = True
            reyaps = Reyap.objects.filter(**kwargs)
            return render(request,
                          "listings/reyaps.html",
                          {"reyaps": reyaps,
                           "title": "Results Search"})
        if params['type_search'] == "4":
            if 'like_id' in params:
                kwargs['like_id'] = params['like_id']
            if 'user_id' in params:
                kwargs['user_id'] = params['user_id']
            if 'yap_id' in params:
                kwargs['yap_id'] = params['yap_id']
            if 'user_liked_id' in params:
                kwargs['user_like_id'] = params['user_liked_id']
            if 'reyap_id' in params:
                kwargs['yap_id'] = params['reyap_id']
            if 'date_created' in params:
                year, month, day = params['date_created'].split('-')
                kwargs['date_created__startswith'] = date(int(year), int(month), int(day))
            if 'is_unliked' in params:
                kwargs['is_unliked'] = True
            if 'date_unliked' in params:
                year, month, day = params['date_unliked'].split('-')
                kwargs['unliked_date__startswith'] = date(int(year), int(month), int(day))
            if 'is_inactive' in params:
                kwargs['is_active'] = False
            if 'user_is_inactive' in params:
                kwargs['is_user_deleted'] = True
            likes = Like.objects.filter(**kwargs)
            return render(request,
                          "listings/likes.html",
                          {"likes": likes,
                           "title": "Results Search"})
        if params['type_search'] == "5":
            if 'listen_id' in params:
                kwargs['listen_id'] = params['listen_id']
            if 'user_id' in params:
                kwargs['user_id'] = params['user_id']
            if 'yap_id' in params:
                kwargs['yap_id'] = params['yap_id']
            if 'user_listened_id' in params:
                kwargs['user_listened_id'] = params['user_listened_id']
            if 'reyap_id' in params:
                kwargs['yap_id'] = params['reyap_id']
            if 'max_listen_click_count' in params:
                kwargs['listen_click_count__lte'] = params['max_listen_click_count']
            if 'min_listen_click_count' in params:
                kwargs['listen_click_count__gte'] = params['min_listen_click_count']
            if 'max_time_listened' in params:
                kwargs['time_listened__lte'] = params['max_time_listened']
            if 'min_listen_click_count' in params:
                kwargs['time_listened__gte'] = params['min_listen_click_count']
            if 'date_created' in params:
                year, month, day = params['date_created'].split('-')
                kwargs['date_created__startswith'] = date(int(year), int(month), int(day))
            if 'is_inactive' in params:
                kwargs['is_active'] = False
            if 'user_is_inactive' in params:
                kwargs['is_user_deleted'] = True
            listens = Listen.objects.filter(**kwargs)
            return render(request, "listings/listens.html", {"listens": listens})
        if params['type_search'] == "6":
            if 'channel_id' in params:
                kwargs['channel_id'] = params['channel_id']
            if 'channel_name' in params:
                kwargs['channel_name__startswith'] = params['channel_name']
            if 'is_bonus' in params:
                kwargs['is_bonus_channel'] = True
            if 'is_not_promoted' in params:
                kwargs['is_promoted'] = False
            if 'date_created' in params:
                year, month, day = params['date_created'].split('-')
                kwargs['date_created__startswith'] = date(int(year), int(month), int(day))
            if 'is_inactive' in params:
                kwargs['is_active'] = False
            if 'date_deactivated' in params:
                year, month, day = params['date_deactivated'].split('-')
                kwargs['date_deactivated__startswith'] = date(int(year), int(month), int(day))
            channels = Channel.objects.filter(**kwargs)
            return render(request, "listings/channels.html", {"title": "Results Search",
                                                              "channels": channels})
        if params['type_search'] == "7":
            if 'hashtag_id' in params:
                kwargs['hashtag_id'] = params['hashtag_id']
            if 'hashtag_name' in params:
                kwargs['hashtag_name__startswith'] = params['hashtag_name']
            if 'date_created' in params:
                year, month, day = params['date_created'].split('-')
                kwargs['date_created__startswith'] = date(int(year), int(month), int(day))
            if 'is_blocked' in params:
                kwargs['is_blocked'] = True
            if 'is_inactive' in params:
                kwargs['is_active'] = False
            hashtags = Hashtag.objects.filter(**kwargs)
            return render(request, "listings/hashtags.html", {"title":  "Results Search",
                                                              "hashtags": hashtags})
        if params['type_search'] == "8":
            reports = Report.objects.all()
            return render(request, "listings/reports.html", {"reports": reports})



    return