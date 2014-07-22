from operator import attrgetter
from django.shortcuts import render
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
    def get(request,  amount=5, _time=5000, country=0, state=0, city=0, gender="n", min_age=0, max_age=99):
        data = OrderedDict()
        
        data['Total Users'] = User.objects.using('yte_1_db').count()
        if data['Total Users']:
            data['Total Number of Active Users'] = User.objects.using('yte_1_db').filter(is_active=True).count()

            #Trending Hashtags
            data['time'] = datetime.datetime.now() - datetime.timedelta(minutes=_time)
            data['Yaps'] = Yap.objects.filter(hashtags_flag=True,is_active=True,is_private=False,date_created__gte=data['time'])
            data['Hashtags List'] = Hashtag.objects.filter(yaps__in=data['Yaps'],is_blocked=False)
            #Use variable hashtags to return the hashtags top hashtags.
            data['Hashtags'] = sorted(set(data['Hashtags List']),key=attrgetter('hashtag_name'))[:amount]

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
                data['Average Number of Listens per User'] = round(data['Total Number of Listens'] / data['Total Users'], 3)
            if data['Total Number of Active Listens']:
                data['Average Number of Active Listens per User'] = round(data['Total Number of Active Listens'] / data['Total Number of Active Users'], 3)
            if data['Average Time Listened']:
                data['Average Time Listened per User'] = round(data['Average Time Listened'] / data['Total Users'], 3)
            if data['Average Active Time Listened']:
                data['Average Active Time Listened per Active User'] = round(data['Average Active Time Listened'] / data['Total Number of Active Users'], 3)

            #Average and Total # of Yaps
            data['Total Number of Yaps'] = Yap.objects.count()
            data['Total Number of Active Yaps'] = Yap.objects.filter(is_active=True).count()

            data['Total Number of Time Yapped'] = Yap.objects.aggregate(Sum('length'))
            data['Total Number of Time Yapped'] = round(data['Total Number of Time Yapped']['length__sum'], 3)

            data['Total Number of Active Time Yapped'] = Yap.objects.filter(is_active=True).aggregate(Sum('length'))
            data['Total Number of Active Time Yapped'] = round(data['Total Number of Active Time Yapped']['length__sum'], 3)

            if data['Total Number of Yaps']:
                data['Average Number of Yaps per Users'] = round(data['Total Number of Yaps'] / data['Total Users'], 3)
            if data['Total Number of Active Yaps']:
                data['Average Number of Active Yaps per Active Users'] = round(data['Total Number of Active Yaps'] / data['Total Number of Active Users'], 3)
            if data['Total Number of Time Yapped']:
                data['Average Number of Time Yapped per Users'] = round(data['Total Number of Time Yapped'] / data['Total Users'], 3)
            if data['Total Number of Active Time Yapped']:
                data['Average Number of Active Time Yapped per Users'] = round(data['Total Number of Active Time Yapped'] / data['Total Number of Active Users'], 3)


            #Average and Total # of Likes
            data['Total Number of Likes'] = Like.objects.count()
            data['Total Number of Active Likes'] = Like.objects.filter(is_active=True).count()
            if data['Total Number of Likes']:
                data['Average Number of Likes per User'] = round(data['Total Number of Likes'] / data['Total Users'], 3)
            if data['Total Number of Active Likes']:
                data['Average Number of Active Likes per Active User'] = round(data['Total Number of Active Likes'] / data['Total Number of Active Users'], 3)

            data['Total Number of Reyaps'] = Reyap.objects.count()
            data['Total Number of Active Reyaps'] = Reyap.objects.filter(is_active=True).count()
            if data['Total Number of Reyaps']:
                data['Average Number of Reyaps per User'] = round(data['Total Number of Reyaps'] / data['Total Users'], 3)
            if data['Total Number of Active Reyaps']:
                data['Average Number of active Reyaps per active User'] = round(data['Total Number of Active Reyaps'] / data['Total Number of Active Users'], 3)

        return Response(data)


    def get_teasing_stats(request,_time=5000, amount=5):
        data = OrderedDict()

        time = datetime.datetime.now() - datetime.timedelta(minutes=_time)
        yaps = Yap.objects.filter(hashtags_flag=True,is_active=True,is_private=False,date_created__gte=time)
        data['Yaps'] = Yap.objects.count()
        data['Total Number of Active Users'] = User.objects.using('yte_1_db').filter(is_active=True).count()
        data['Total Number of Listens'] = Listen.objects.count()
        data['Average Time Listened'] = round(Listen.objects.aggregate(Avg('time_listened'))['time_listened__avg'], 3)
        list_hashtags = Hashtag.objects.filter(yaps__in=yaps, is_blocked=False)
        data['Hashtags'] = sorted(set(list_hashtags),key=attrgetter('hashtag_name'))[:amount]

        return Response(data)