from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import models
from location.models import *
from django.dispatch import receiver
from operator import attrgetter
from django.contrib.gis.db import models
from stats.models import HashtagManager, YapManager, ReyapManager, LikeManager, ListenManager
import re

class Hashtag(models.Model):
    '''hashtag table'''
    hashtag_id = models.AutoField(primary_key=True)
    hashtag_name = models.CharField(max_length=255,unique=True) #name of tag as string
    date_created = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    stats = HashtagManager()

    def __unicode__(self):
        return self.hashtag_name

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Tags cannot be deleted.')

class Channel(models.Model):
    '''table of organizational groups'''
    channel_id = models.AutoField(primary_key=True)
    channel_name = models.CharField(max_length=255,unique=True) #name of Channel as string
    channel_description = models.CharField(max_length=255) #description of the Channel
    icon_explore_path_clicked = models.CharField(unique=True,max_length=255) #location icon is stored
    icon_explore_path_unclicked = models.CharField(unique=True,max_length=255) #location icon is stored
    icon_yap_path_clicked = models.CharField(unique=True,max_length=255) #location icon is stored
    icon_yap_path_unclicked = models.CharField(unique=True,max_length=255) #location icon is stored
    is_bonus_channel = models.BooleanField(default=False) #True if the Channel is not one of the originals
    is_promoted = models.BooleanField(default=True)
    geographic_target = models.ForeignKey(GeographicTarget,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.channel_name

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Channels cannot be deleted.')

class WebsiteLink(models.Model):
    website_link_id = models.AutoField(primary_key=True)
    website_link = models.URLField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.website_link

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Tags cannot be deleted.')


class Yap(models.Model):
    yap_id = models.AutoField(primary_key=True)
    user_yap_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="yaps")
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    hashtags_flag = models.BooleanField(default=False)
    hashtags = models.ManyToManyField(Hashtag, related_name="yaps",blank=True,null=True) #foreign key to tags
    channel_flag = models.BooleanField(default=False)
    channel = models.ForeignKey(Channel, blank=True, null=True,related_name="yaps") #foreign key to Channel
    user_tags_flag = models.BooleanField(default=False)
    user_tags = models.ManyToManyField(User,related_name="yaps_in")
    length = models.BigIntegerField() #time in seconds
    listen_count = models.BigIntegerField(default=0)
    reyap_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    website_links_flag = models.BooleanField(default=False)
    website_links = models.ManyToManyField(WebsiteLink, related_name="yaps",blank=True,null=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    point = models.PointField(srid=4326,null=True,blank=True)
    audio_path = models.CharField(unique=True, max_length=255) #location of the audio file
    picture_flag = models.BooleanField(default=False)
    picture_path = models.CharField(unique=True, max_length=255,blank=True,null=True)
    picture_cropped_flag = models.BooleanField(default=False)
    picture_cropped_path = models.CharField(blank=True,max_length=255)
    facebook_shared_flag = models.BooleanField(default=False)
    facebook_account_id = models.BigIntegerField(blank=True,null=True)
    twitter_shared_flag = models.BooleanField(default=False)
    twitter_account_id = models.BigIntegerField(blank=True,null=True)
    google_plus_shared_flag = models.BooleanField(default=False)
    google_plus_account_id = models.BigIntegerField(blank=True,null=True)
    linkedin_shared_flag = models.BooleanField(default=False)
    linkedin_account_id = models.BigIntegerField(blank=True,null=True)
    deleted_date = models.DateTimeField(blank=True,null=True)
    deleted_latitude = models.FloatField(null=True,blank=True)
    deleted_longitude = models.FloatField(null=True,blank=True)
    deleted_point = models.PointField(srid=4326,null=True,blank=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)
    objects = models.GeoManager()
    stats = YapManager()

    class Meta:
        ordering = ['-date_created']


    @classmethod
    def name(self):
        return "yap"


class Reyap(models.Model):
    '''Reyap table'''
    reyap_id = models.AutoField(primary_key=True)
    user_reyap_id = models.BigIntegerField(default=1)
    yap = models.ForeignKey(Yap,related_name='reyaps')
    user = models.ForeignKey(User, related_name='reyaps')
    reyap_flag = models.BooleanField(default=False)
    reyap_reyap = models.ForeignKey("self",blank=True, null=True,related_name="reyaps")
    facebook_connection_flag = models.BooleanField(default=False)
    facebook_account_id = models.BigIntegerField(blank=True,null=True)
    twitter_connection_flag = models.BooleanField(default=False)
    twitter_account_id = models.BigIntegerField(blank=True,null=True)
    google_plus_connection_flag = models.BooleanField(default=False)
    google_plus_account_id = models.BigIntegerField(blank=True,null=True)
    linkedin_connection_flag = models.BooleanField(default=False)
    linkedin_account_id = models.BigIntegerField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    point = models.PointField(srid=4326,null=True,blank=True)
    reyap_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    listen_count = models.BigIntegerField(default=0)
    is_unreyapped = models.BooleanField(default=False)
    unreyapped_date = models.DateTimeField(blank=True,null=True)
    unreyapped_latitude = models.FloatField(null=True,blank=True)
    unreyapped_longitude = models.FloatField(null=True,blank=True)
    unreyapped_point = models.PointField(srid=4326,null=True,blank=True)
    deleted_date = models.DateTimeField(blank=True,null=True)
    deleted_latitude = models.FloatField(null=True,blank=True)
    deleted_longitude = models.FloatField(null=True,blank=True)
    deleted_point = models.PointField(srid=4326,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)
    objects = models.GeoManager()
    stats = ReyapManager()

    class Meta:
        ordering = ['-date_created']

    @classmethod
    def name(self):
        return "reyap"


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user_like_id = models.BigIntegerField(default=1)
    yap = models.ForeignKey(Yap,related_name='likes')
    user = models.ForeignKey(User,related_name='likes')
    reyap_flag = models.BooleanField(default=False)
    reyap = models.ForeignKey(Reyap,blank=True, null=True,related_name='likes')
    date_created = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    point = models.PointField(srid=4326,null=True,blank=True)
    is_unliked = models.BooleanField(default=False)
    unliked_date = models.DateTimeField(null=True,blank=True)
    unliked_latitude = models.FloatField(null=True,blank=True)
    unliked_longitude = models.FloatField(null=True,blank=True)
    unliked_point = models.PointField(srid=4326,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)
    objects = models.GeoManager()
    stats = LikeManager()

    class Meta:
        ordering = ['-date_created']

    @classmethod
    def name(self):
        return "like"


#complete
class Listen(models.Model):
    '''table for a yap or reyap listen'''
    listen_id = models.AutoField(primary_key=True)
    user_listen_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User, related_name='listens')
    yap = models.ForeignKey(Yap, related_name='listens')
    reyap_flag = models.BooleanField(default=False)
    reyap = models.ForeignKey(Reyap,related_name='listens',blank=True,null=True)
    listen_click_count = models.BigIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    time_listened = models.BigIntegerField(blank=True,null=True) #amount of time listened. defaults to 0 seconds and the `set_time` function can be used to edit
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    point = models.PointField(srid=4326,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)
    objects = models.GeoManager()

    class Meta:
        ordering = ['-date_created']

    @classmethod
    def name(self):
        return "listen"


class ListenClick(models.Model):
    listen_click_id = models.AutoField(primary_key=True)
    user_listen_click_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name='user_listen_clicked')
    listen = models.ForeignKey(Listen,related_name='listen_clicked')
    hashtag_clicked_flag = models.BooleanField(default=False)
    hashtag_clicked = models.ForeignKey(Hashtag,related_name='listen_clicked',null=True,blank=True)
    user_handle_clicked_flag = models.BooleanField(default=False)
    user_handle_clicked = models.ForeignKey(User,related_name='listen_handle_clicked',null=True,blank=True)
    user_yapped_clicked_flag = models.BooleanField(default=False)
    user_reyapped_clicked_flag = models.BooleanField(default=False)
    web_link_clicked_flag = models.BooleanField(default=False)
    picture_clicked_flag = models.BooleanField(default=False)
    skipped_flag = models.BooleanField(default=False)
    liked_flag = models.BooleanField(default=False)
    unliked_flag = models.BooleanField(default=False)
    liked_like = models.ForeignKey(Like,related_name='listens_liked',blank=True,null=True)
    reyapped_flag = models.BooleanField(default=False)
    unreyapped_flag = models.BooleanField(default=False)
    reyapped_reyap = models.ForeignKey(Reyap,related_name='listens_reyapped',blank=True,null=True)
    time_clicked = models.BigIntegerField()
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    point = models.PointField(srid=4326,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)
    objects = models.GeoManager()

    class Meta:
        ordering = ['-date_created']


class FollowerRequest(models.Model):
    follower_request_id = models.AutoField(primary_key=True)
    user_follower_request_id = models.BigIntegerField(default=1)
    #user is the person asking to listen
    user = models.ForeignKey(User, related_name='requests')
    #user_requested is the person being asked to be listen to
    user_requested = models.ForeignKey(User, related_name='requested')
    date_created = models.DateTimeField(auto_now_add=True)
    created_latitude = models.FloatField(null=True,blank=True)
    created_longitude = models.FloatField(null=True,blank=True)
    created_point = models.PointField(srid=4326,null=True,blank=True)
    is_unrequested = models.BooleanField(default=False)
    date_unrequested = models.DateTimeField(blank=True,null=True)
    unrequested_latitude = models.FloatField(null=True,blank=True)
    unrequested_longitude = models.FloatField(null=True,blank=True)
    unrequested_point = models.PointField(srid=4326,null=True,blank=True)
    is_accepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField(null=True,blank=True)
    accepted_latitude = models.FloatField(null=True,blank=True)
    accepted_longitude = models.FloatField(null=True,blank=True)
    accepted_point = models.PointField(srid=4326,null=True,blank=True)
    is_denied = models.BooleanField(default=False)
    date_denied = models.DateTimeField(null=True,blank=True)
    denied_latitude = models.FloatField(null=True,blank=True)
    denied_longitude = models.FloatField(null=True,blank=True)
    denied_point = models.PointField(srid=4326,null=True,blank=True)
    is_unfollowed = models.BooleanField(default=False)
    unfollowed_latitude = models.FloatField(null=True,blank=True)
    unfollwed_longitude = models.FloatField(null=True,blank=True)
    unfollwed_point = models.PointField(srid=4326,null=True,blank=True)
    date_unfollowed = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)
    objects = models.GeoManager()

    class Meta:
        ordering = ['-date_created']

    @classmethod
    def name(self):
        return "request"