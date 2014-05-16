from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile of a Yapster user
    """
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    handle = models.CharField(max_length=64, unique=True)
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

    def delete(self, using=None):
        self.is_active = False
        return

class GroupPermission(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=24, unique=True)
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        return

class CmsUser (models.Model):
    """
    CMS User account
    """
    user = models.OneToOneField(User, primary_key=True, related_name='account')
    username = models.CharField(max_length=64)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)
    group = models.ForeignKey(to=GroupPermission, blank=True, related_name='members')
    occupation = models.CharField(max_length=64, blank=True)
    department = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.user = User.objects._create_user(username=self.username, email=self.email, password=self.password, is_staff=False,
                                              is_superuser=False, first_name=self.firstname, last_name=self.lastname)
        super(CmsUser, self).save()
        return self

    def delete(self, using=None):
        self.is_active = False
        return


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

    def delete(self, using=None):
        self.is_active = False
        return


class NotificationType(models.Model):
    """
    For different types of notifications
    """
    notification_type_id = models.AutoField(primary_key=True)
    notification_name = models.CharField(max_length=24, unique=True)
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        return

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

    def delete(self, using=None):
        self.is_active = False
        return