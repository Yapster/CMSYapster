from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
from yap.models import *
import datetime
import time

class NotificationType(models.Model):
    notification_type_id = models.AutoField(primary_key=True)
    notification_name = models.CharField(max_length=100,unique=True)
    notification_picture_path = models.CharField(max_length=255,blank=True)
    notification_message = models.CharField(max_length=255,blank=True)
    is_yapster_notification = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def delete(self,user):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=['is_active'])
            return True
        else:
            return False

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=['is_active'])
            return True
        else:
            return False

class Notification(models.Model):
    """created and origin depends on why the object is sent and where it is sent from"""
    notification_id = models.AutoField(primary_key=True)
    user_notification_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="notifications")
    notification_type = models.ForeignKey(NotificationType,related_name="notifications")
    origin_yap_flag = models.BooleanField(default=False)
    origin_yap = models.ForeignKey(Yap,blank=True,null=True)
    origin_reyap_flag = models.BooleanField(default=False)
    origin_reyap = models.ForeignKey(Reyap,null=True,blank=True)
    acting_user = models.ForeignKey(User,related_name="notifications_sent")
    created_like_flag = models.BooleanField(default=False)
    created_like = models.ForeignKey(Like,blank=True,null=True,related_name="notifications")
    created_reyap_flag = models.BooleanField(default=False)
    created_reyap = models.ForeignKey(Reyap,null=True,blank=True,related_name="notifications")
    created_follower_request_flag = models.BooleanField(default=False)
    created_follower_request = models.ForeignKey(FollowerRequest,null=True,blank=True,related_name="notifications")
    created_listen_flag = models.BooleanField(default=False)
    created_listen = models.ForeignKey(Listen,null=True,blank=True,related_name="notifications")
    is_yapster_notification = models.BooleanField(default=False)
    user_verified_flag = models.BooleanField(default=False)
    user_unverified_flag = models.BooleanField(default=False)
    user_recommended_flag = models.BooleanField(default=False)
    user_unrecommended_flag = models.BooleanField(default=False)
    user_read_flag = models.BooleanField(default=False)
    user_read_date = models.DateTimeField(blank=True,null=True)
    user_read_latitude = models.FloatField(null=True,blank=True)
    user_read_longitude = models.FloatField(null=True,blank=True)
    user_read_point = models.PointField(srid=4326,null=True,blank=True)
    user_clicked_flag = models.BooleanField(default=False)
    user_clicked_date = models.DateTimeField(blank=True,null=True)
    user_clicked_latitude = models.FloatField(null=True,blank=True)
    user_clicked_longitude = models.FloatField(null=True,blank=True)
    user_clicked_point = models.PointField(srid=4326,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)
    objects = models.GeoManager()

    class Meta:
        ordering = ['-date_created']


    def delete(self,is_user_deleted=False):
        if self.is_active == True:
            if is_user_deleted == True:
                self.is_active = False
                self.is_user_deleted = True
                self.save(update_fields=['is_active','is_user_deleted'])
            elif is_user_deleted == False:
                self.is_active = False
                self.save(update_fields=['is_active'])
        elif self.is_active == False and self.is_user_deleted == False:
            return 'This UserFunctions object is already deleted.'
        elif self.is_active == False and self.is_user_deleted == True:
            return 'This user has already been deleted.'

    def activate(self,is_user_activated=False):
        if self.is_active == False:
            if is_user_activated == True:
                self.is_active = True
                self.is_user_deleted = False
                self.save(update_fields=['is_active','is_user_deleted'])
            elif is_user_activated == False:
                return 'To activate a UserFunctions, you must activate a user (is_user_activated=True).'
        elif self.is_active == True and self.is_user_deleted == False:
            return 'This UserFunctions is already activated.'

    def read(self):
        self.user_read_flag = True
        self.user_read_date = datetime.datetime.now()
        self.save(update_fields=['user_read_flag','user_read_date'])
        return 'This notification has been read.'

    def clicked(self):
        self.user_clicked_flag = True
        self.user_clicked_date = datetime.datetime.now()
        self.save(update_fields=['user_clicked_flag','user_clicked_date'])
        return 'This notification has been clicked.'
