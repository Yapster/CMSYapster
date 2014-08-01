from operator import attrgetter
from django.shortcuts import render
import operator
from yap.serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
import datetime
from datetime import timedelta
from collections import OrderedDict

class HomePageStatistics(APIView):
    @staticmethod
    def get_yaps_stats(request,  amount=5, _time=100000, country=0, state=0, city=0, gender="n", min_age=0, max_age=99):
        data = OrderedDict()

        users_count = User.objects.using('ye_1_db_1').count()


        if users_count:
            active_users_count = User.objects.using('ye_1_db_1').filter(is_active=True).count()

            #Trending Hashtags
            time = datetime.datetime.now() - datetime.timedelta(minutes=_time)
            yaps = Yap.objects.filter(hashtags_flag=True,is_active=True,is_private=False,date_created__gte=time)
            hashtags_list = Hashtag.objects.filter(yaps__in=yaps,is_blocked=False)
            #Use variable hashtags to return the hashtags top hashtags.
            data['Hashtags'] = sorted(set(hashtags_list),key=attrgetter('hashtag_name'))[:amount]

            #Average And Total Listening Time
            data['Total Number of Listens'] = Listen.objects.count()
            data['Total Number of Active Listens'] = Listen.objects.filter(is_active=True).count()

            data['Total Time Listened'] = Listen.objects.aggregate(Sum('time_listened'))
            data['Total Time Listened'] = data['Total Time Listened']['time_listened__sum']

            data['Total Active Time Listened'] = Listen.objects.filter(is_active=True).aggregate(Sum('time_listened'))
            data['Total Active Time Listened'] = data['Total Active Time Listened']['time_listened__sum']

            data['Average Time Listened'] = Listen.objects.aggregate(Avg('time_listened'))
            data['Average Time Listened'] = round(data['Average Time Listened']['time_listened__avg'], 3)

            data['Average Active Time Listened'] = Listen.objects.filter(is_active=True).aggregate(Avg('time_listened'))
            data['Average Active Time Listened'] = round(data['Average Active Time Listened']['time_listened__avg'])

            if data['Total Number of Listens']:
                data['Average Number of Listens per User'] = round(data['Total Number of Listens'] / users_count, 3)
            if data['Total Number of Active Listens']:
                data['Average Number of Active Listens per User'] = round(data['Total Number of Active Listens'] / active_users_count, 3)
            if data['Average Time Listened']:
                data['Average Time Listened per User'] = round(data['Average Time Listened'] / users_count, 3)
            if data['Average Active Time Listened']:
                data['Average Active Time Listened per Active User'] = round(data['Average Active Time Listened'] / active_users_count, 3)

            #Average and Total # of Yaps
            data['Total Number of Yaps'] = Yap.objects.count()
            data['Total Number of Active Yaps'] = Yap.objects.filter(is_active=True).count()

            data['Total Number of Time Yapped'] = Yap.objects.aggregate(Sum('length'))
            data['Total Number of Time Yapped'] = round(data['Total Number of Time Yapped']['length__sum'], 3)

            data['Total Number of Active Time Yapped'] = Yap.objects.filter(is_active=True).aggregate(Sum('length'))
            data['Total Number of Active Time Yapped'] = round(data['Total Number of Active Time Yapped']['length__sum'], 3)

            if data['Total Number of Yaps']:
                data['Average Number of Yaps per Users'] = round(data['Total Number of Yaps'] / users_count, 3)
            if data['Total Number of Active Yaps']:
                data['Average Number of Active Yaps per Active Users'] = round(data['Total Number of Active Yaps'] / active_users_count, 3)
            if data['Total Number of Time Yapped']:
                data['Average Number of Time Yapped per Users'] = round(data['Total Number of Time Yapped'] / users_count, 3)
            if data['Total Number of Active Time Yapped']:
                data['Average Number of Active Time Yapped per Users'] = round(data['Total Number of Active Time Yapped'] / active_users_count, 3)


            #Average and Total # of Likes
            data['Total Number of Likes'] = Like.objects.count()
            data['Total Number of Active Likes'] = Like.objects.filter(is_active=True).count()
            if data['Total Number of Likes']:
                data['Average Number of Likes per User'] = round(data['Total Number of Likes'] / users_count, 3)
            if data['Total Number of Active Likes']:
                data['Average Number of Active Likes per Active User'] = round(data['Total Number of Active Likes'] / active_users_count, 3)

            data['Total Number of Reyaps'] = Reyap.objects.count()
            data['Total Number of Active Reyaps'] = Reyap.objects.filter(is_active=True).count()
            if data['Total Number of Reyaps']:
                data['Average Number of Reyaps per User'] = round(data['Total Number of Reyaps'] / users_count, 3)
            if data['Total Number of Active Reyaps']:
                data['Average Number of active Reyaps per active User'] = round(data['Total Number of Active Reyaps'] / active_users_count, 3)

        return Response(data)

    @staticmethod
    def get_teasing_stats(request,_time=100000, amount=5):
        data = OrderedDict()

        time = datetime.datetime.now() - datetime.timedelta(minutes=_time)
        yaps = Yap.objects.filter(hashtags_flag=True,is_active=True,is_private=False,date_created__gte=time)
        data['Yaps'] = Yap.objects.count()
        data['Total Number of Active Users'] = User.objects.using('ye_1_db_1').filter(is_active=True).count()
        data['Total Number of Listens'] = Listen.objects.count()
        data['Average Time Listened'] = round(Listen.objects.aggregate(Avg('time_listened'))['time_listened__avg'], 3)
        list_hashtags = Hashtag.objects.filter(yaps__in=yaps, is_blocked=False)
        data['Hashtags'] = sorted(set(list_hashtags),key=attrgetter('hashtag_name'))[:amount]

        return Response(data)

    @staticmethod
    def get_users_stats(request,  amount=5, _time=100000, country=0, state=0, city=0, gender="n", min_age=0, max_age=99):
        data = OrderedDict()
        users = User.objects.using('ye_1_db_1').all()
        print(1)
        time = datetime.datetime.now() - datetime.timedelta(minutes=_time)
        users_count = len(users)
        if users:
            print(2)
            data['Total Number of Active Users'] = users.filter(is_active=True).count()
            print(3)
            data['Total New Users'] = users.filter(date_joined__gte=time).count()
            print(4)
            # Get top [amount]
            d_countries = {}
            for country in Country.objects.all():
                d_countries[country.country_name] = users.filter(profile__user_country_id=country.country_id).count()
            data['Top Countries Users'] = sorted(d_countries.iteritems(), key=operator.itemgetter(1), reverse=True)[:amount]
            print(5)
            data['Birthdays this Month'] = users.filter(profile__date_of_birth__month=datetime.date.today().month)
            print(6)
            data['Birthdays Today'] = users.filter(profile__date_of_birth__month=datetime.date.today().month,
                                                   profile__date_of_birth__day=datetime.date.today().day)
            print(7)

            # data['Average Age of Users'] = User.objects.using('ye_1_db_1').filter(is_active=True).count()
            # data['Average Age of Active Users'] = User.objects.using('ye_1_db_1').filter(is_active=True).count()
            # data['Average Age of New Users'] = User.objects.using('ye_1_db_1').filter(is_active=True).count()
            # data['Top 5 Most Popular Users'] = User.objects.using('ye_1_db_1').filter(is_active=True).count()

        return Response(data)