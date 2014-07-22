from django.db import models
from location.models import *
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class DeactivateUserLog(models.Model):
    deactivate_user_log_id = models.AutoField(primary_key=True)
    user_deactivate_user_log_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="deactivate_user_logs")
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Deactivation log objects cannot be deleted.')


class BlackList(models.Model):
    blacklist_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,unique=True)
    account_created_flag = models.BooleanField(default=False)
    account_created_date = models.DateTimeField(blank=True,null=True)
    blacklisted_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('BlackList cannot be deleted.')


class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User,primary_key=True,related_name="profile")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    follower_count = models.BigIntegerField(default=0)
    following_count = models.BigIntegerField(default=0)
    yap_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    listen_count = models.BigIntegerField(default=0)
    reyap_count = models.BigIntegerField(default=0)
    description = models.CharField(blank=True,max_length=255)
    profile_picture_flag = models.BooleanField(default=False)
    profile_picture_path = models.CharField(blank=True,max_length=255)
    profile_picture_cropped_flag = models.BooleanField(default=False)
    profile_picture_cropped_path = models.CharField(blank=True,max_length=255)
    date_of_birth = models.DateField(null=True,blank=True)
    user_city = models.ForeignKey(City,related_name="profile_user_city",null=True,blank=True)
    user_us_state = models.ForeignKey(USState,related_name="profile_user_state",null=True,blank=True)
    user_us_zip_code = models.ForeignKey(USZIPCode,related_name="profile_user_zip_code",null=True,blank=True)
    user_country = models.ForeignKey(Country,related_name="profile_user_country",null=True,blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    high_security_account_flag = models.BooleanField(default=False)
    verified_account_flag = models.BooleanField(default=False)
    listen_stream_public = models.BooleanField(default=True)
    posts_are_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Profile cannot be deleted.')


class UserInfo(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=30,unique=True)
    date_of_birth = models.DateField()
    user_city = models.ForeignKey(City,related_name="user_city",blank=True,null=True)
    user_us_state = models.ForeignKey(USState,related_name="user_state",blank=True,null=True)
    user_us_zip_code = models.ForeignKey(USZIPCode,related_name="user_zip_code",blank=True,null=True)
    user_country = models.ForeignKey(Country,related_name="user_country",blank=True,null=True)
    last_account_modified_date = models.DateTimeField(auto_now_add=True)
    high_security_account_flag = models.BooleanField(default=False)
    verified_account_flag = models.BooleanField(default=False)
    facebook_connection_flag = models.BooleanField(default=False)
    facebook_account_id = models.BigIntegerField(blank=True,null=True)
    facebook_share_reyap = models.BooleanField(default=True)
    twitter_connection_flag = models.BooleanField(default=False)
    twitter_account_id = models.BigIntegerField(blank=True,null=True)
    twitter_share_reyap = models.BooleanField(default=True)
    google_plus_connection_flag = models.BooleanField(default=False)
    google_plus_account_id = models.BigIntegerField(blank=True,null=True)
    google_plus_share_reyap = models.BooleanField(default=True)
    linkedin_connection_flag = models.BooleanField(default=False)
    linkedin_account_id = models.BigIntegerField(blank=True,null=True)
    linkedin_share_reyap = models.BooleanField(default=True)
    profile_picture_flag = models.BooleanField(default=False)
    profile_picture_path = models.CharField(blank=True,max_length=255)
    profile_picture_cropped_flag = models.BooleanField(default=False)
    profile_picture_cropped_path = models.CharField(blank=True,max_length=255)
    listen_stream_public = models.BooleanField(default=True)
    posts_are_private = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    notify_for_mentions = models.BooleanField(default=True)
    notify_for_reyaps = models.BooleanField(default=True)
    notify_for_likes = models.BooleanField(default=True)
    notify_for_new_followers = models.BooleanField(default=True)
    notify_for_yapster = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)
    user_deleted_date = models.DateField(blank=True,null=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('UserInfo cannot be deleted.')


class Settings(models.Model):
    user = models.OneToOneField(User, primary_key=True,related_name="settings")
    notify_for_mentions = models.BooleanField(default=True)
    notify_for_reyaps = models.BooleanField(default=True)
    notify_for_likes = models.BooleanField(default=True)
    notify_for_listens = models.BooleanField(default=True)
    notify_for_new_followers = models.BooleanField(default=True)
    notify_for_yapster = models.BooleanField(default=True)
    facebook_connection_flag = models.BooleanField(default=False)
    facebook_account_id = models.BigIntegerField(blank=True,null=True)
    facebook_share_reyap = models.BooleanField(default=False)
    twitter_connection_flag = models.BooleanField(default=False)
    twitter_account_id = models.BigIntegerField(blank=True,null=True)
    twitter_share_reyap = models.BooleanField(default=False)
    google_plus_connection_flag = models.BooleanField(default=False)
    google_plus_account_id = models.BigIntegerField(blank=True,null=True)
    google_plus_share_reyap = models.BooleanField(default=False)
    linkedin_connection_flag = models.BooleanField(default=False)
    linkedin_account_id = models.BigIntegerField(blank=True,null=True)
    linkedin_share_reyap = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Settings cannot be deleted.')


class Recommended(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user_recommendation_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name='recommended')
    date_recommended = models.DateTimeField(auto_now_add=True)
    date_will_be_deactivated = models.DateTimeField(null=True,blank=True)
    date_deactivated = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Recommended cannot be deleted.')


class ForgotPasswordRequest(models.Model):
    forgot_password_id = models.AutoField(primary_key=True)
    user_forgot_password_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="forgot_password_requests")
    user_email = models.EmailField()
    reset_password_security_code = models.CharField(max_length=255,blank=True,null=True)
    reset_password_security_code_used_flag = models.BooleanField(default=False)
    date_used = models.DateTimeField(blank=True,null=True)
    user_signed_in_after_without_using_flag = models.BooleanField(default=False)
    date_signed_in_without_using = models.DateTimeField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_created']

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('ForgotPasswordRequest cannot be deleted.')


class UserFunctions(models.Model):
    user = models.OneToOneField(User, primary_key=True,related_name="functions")
    is_user_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('UserFunctions object cannot be deleted.')

class SessionVerification(models.Model):
    session_id = models.AutoField(primary_key=True)
    user_session_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="sessions")
    session_device_token = models.CharField(max_length=255,blank=True,null=True)
    session_manually_closed_flag = models.BooleanField(default=False)
    session_logged_out_flag = models.BooleanField(default=False)
    session_timed_out_flag = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('SessionVerification cannot be deleted.')