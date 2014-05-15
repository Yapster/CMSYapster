from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile of a Yapster user
    """
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    yap_count = models.BigIntegerField(default=0)
    listener_count = models.BigIntegerField(default=0)
    listening_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    listen_count = models.BigIntegerField(default=0)
    reyap_count = models.BigIntegerField(default=0)
    description = models.CharField(blank=True, max_length=255)
    profile_picture_path = models.CharField(blank=True, max_length=255)
    location_city = models.CharField(blank=True, max_length=255)
    location_state = models.CharField(blank=True, max_length=2)
    is_active = models.BooleanField(default=True)


class Announcement(models.Model):
    """
    Annoucements for homepage
    """
    announcement_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='announces')
    title = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_edit = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class NotificationType(models.Model):
    """
    For different types of notifications
    """
    notification_type_id = models.AutoField(primary_key=True)
    notification_name = models.CharField(max_length=24, unique=True)
    is_active = models.BooleanField(default=True)


class Notification(models.Model):
    """
    Notification for CMS Users
    """
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='notifications')
    notification_type = models.ForeignKey(NotificationType, related_name='notifications')
    description = models.CharField(blank=True, max_length=255)
    been_seen = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class GroupPermission(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=24, unique=True)
