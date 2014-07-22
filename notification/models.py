from django.db import models
from yap.models import Reyap, Like, Yap, Listen, FollowerRequest
from users.models import User

class NotificationType(models.Model):
    notification_type_id = models.AutoField(primary_key=True)
    notification_name = models.CharField(max_length=100,unique=True)
    notification_picture_path = models.CharField(max_length=255,blank=True)
    notification_message = models.CharField(max_length=255,blank=True)
    is_yapster_notification = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('NotificationTypes cannot be deleted.')


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
    user_clicked_flag = models.BooleanField(default=False)
    user_clicked_date = models.DateTimeField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Notifications cannot be deleted.')
