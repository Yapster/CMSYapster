from operator import attrgetter
from django.shortcuts import render
from api.serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
import datetime
from datetime import timedelta



class HomePageStatistics(APIView):
    def post(self,request):
        total_number_of_users = User.objects.count()
        total_number_of_active_users = User.objects.filter(is_active=True).count()

        #Trending Hashtags
        minutes = 5000
        amount = 12
        time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        yaps = Yap.objects.filter(hashtags_flag=True,is_active=True,is_private=False,date_created__gte=time)
        hashtags_list = Hashtag.objects.filter(yaps__in=yaps,is_blocked=False)
        #Use variable hashtags to return the hashtags top hashtags.
        hashtags = sorted(set(hashtags_list),key=attrgetter('hashtag_name'))[:amount]

        #Average And Total Listening Time
        total_number_of_listens = Listen.objects.count()
        total_number_of_active_listens = Listen.objects.filter(is_active=True).count()

        total_time_listened = Listen.objects.aggregate(Sum('time_listened'))
        total_time_listened = total_time_listened['time_listened__sum']

        total_active_time_listened = Listen.objects.filter(is_active=True).aggregate(Sum('time_listened'))
        total_active_time_listened = total_active_time_listened['time_listened__sum']

        average_time_listened = Listen.objects.aggregate(Avg('time_listened'))
        average_time_listened = average_time_listened['time_listened__avg']

        average_active_time_listened = Listen.objects.filter(is_active=True).aggregate(Avg('time_listened'))
        average_active_time_listened = average_active_time_listened['time_listened__avg']

        average_number_of_listens_per_user = total_number_of_listens / total_number_of_users
        average_number_of_active_listens_per_active_user = total_number_of_active_listens / total_number_of_active_users
        average_time_listened_per_user = average_time_listened / total_number_of_users
        average_active_time_listened_per_active_user = average_active_time_listened / total_number_of_active_users

        #Average and Total # of Yaps
        total_number_of_yaps = Yap.objects.count()
        total_number_of_active_yaps = Yap.objects.filter(is_active=True).count()

        total_number_of_time_yapped = Yap.objects.aggregate(Sum('length'))
        total_number_of_time_yapped = total_number_of_time_yapped['length__sum']

        total_number_of_active_time_yapped = Yap.objects.filter(is_active=True).aggregate(Sum('length'))
        total_number_of_active_time_yapped = total_number_of_active_time_yapped['length__sum']

        average_number_of_yaps_per_users = total_number_of_yaps / total_number_of_users
        average_number_of_active_yaps_per_active_users = total_number_of_active_yaps / total_number_of_active_users
        average_number_of_time_yapped_per_user = total_number_of_time_yapped / total_number_of_users
        average_number_of_active_time_yapped_per_user = total_number_of_active_time_yapped / total_number_of_active_users


        #Average and Total # of Likes
        total_number_of_likes = Like.objects.count()
        total_number_of_active_likes = Like.objects.filter(is_active=True).count()
        average_number_of_likes_per_user = total_number_of_likes / total_number_of_users
        average_number_of_active_likes_per_active_user = total_number_of_active_likes / total_number_of_active_users

        total_number_of_reyaps = Reyap.objects.count()
        total_number_of_active_reyaps = Reyap.objects.filter(is_active=True).count()
        average_number_of_reyaps_per_user = total_number_of_reyaps / total_number_of_users
        average_number_of_active_reyaps_per_active_user = total_number_of_active_reyaps / total_number_of_active_users
