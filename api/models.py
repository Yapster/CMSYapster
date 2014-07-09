from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

class USState(models.Model):
    us_states_id = models.AutoField(primary_key=True)
    us_state_name = models.CharField(max_length=255)
    us_state_abbreviation = models.CharField(max_length=2,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)


class USZIPCode(models.Model):
    us_zip_code_id = models.AutoField(primary_key=True)
    us_zip_code = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)
    us_zip_code = models.ForeignKey(USZIPCode,related_name="city_us_zip_code",null=True,blank=True)
    us_state = models.ForeignKey(USState,related_name="city_us_state",null=True,blank=True)
    country = models.ForeignKey(Country,related_name="city_country")
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)


class GeographicTarget(models.Model):
    geographic_target_id = models.AutoField(primary_key=True)
    geographic_countries_flag = models.BooleanField(default=False)
    geographic_countries = 	models.ManyToManyField(Country, related_name="geographic_countries",blank=True,null=True) #foreign key to Countries
    geographic_states_flag = models.BooleanField(default=False)
    geographic_states = models.ManyToManyField(USState,related_name="geographic_states",blank=True,null=True)
    geographic_zip_codes_flag = models.BooleanField(default=False)
    geographic_zip_codes = models.ManyToManyField(USZIPCode, related_name="geographic_zip_codes",blank=True,null=True)
    geographic_cities_flag = models.BooleanField(default=False)
    geographic_cities = models.ManyToManyField(City, related_name="geographic_cities",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)
    is_active = models.BooleanField(default=True)


class Hashtag(models.Model):
    '''hashtag table'''
    hashtag_id = models.AutoField(primary_key=True)
    hashtag_name = models.CharField(max_length=255,unique=True) #name of tag as string
    date_created = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    def __unicode__(self):
        return self.hashtag_name

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


class Yap(models.Model):
    yap_id = models.AutoField(primary_key=True)
    user_yap_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="yaps")
    title = models.CharField(max_length=255)
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
    web_link_flag = models.BooleanField(default=False)
    web_link = models.URLField(max_length=255,null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
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
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

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
    reyap_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    listen_count = models.BigIntegerField(default=0)
    is_unreyapped = models.BooleanField(default=False)
    unreyapped_date = models.DateTimeField(blank=True,null=True)
    deleted_date = models.DateTimeField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user_like_id = models.BigIntegerField(default=1)
    yap = models.ForeignKey(Yap,related_name='likes')
    user = models.ForeignKey(User,related_name='likes')
    reyap_flag = models.BooleanField(default=False)
    reyap = models.ForeignKey(Reyap,blank=True, null=True,related_name='likes')
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    is_unliked = models.BooleanField(default=False)
    unliked_date = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

    @classmethod
    def name(self):
        return "like"

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
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

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
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

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
    is_unrequested = models.BooleanField(default=False)
    date_unrequested = models.DateTimeField(blank=True,null=True)
    is_accepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField(null=True,blank=True)
    is_denied = models.BooleanField(default=False)
    date_denied = models.DateTimeField(null=True,blank=True)
    is_unfollowed = models.BooleanField(default=False)
    date_unfollowed = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

class NotificationType(models.Model):
    notification_type_id = models.AutoField(primary_key=True)
    notification_name = models.CharField(max_length=100,unique=True)
    notification_picture_path = models.CharField(max_length=255,blank=True)
    notification_message = models.CharField(max_length=255,blank=True)
    is_yapster_notification = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


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


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user_report_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="reported")
    reported_yap_flag = models.BooleanField(default=False)
    reported_yap = models.ForeignKey(Yap,null=True,blank=True,related_name="reports")
    reported_reyap_flag = models.BooleanField(default=False)
    reported_reyap = models.ForeignKey(Reyap,null=True,blank=True,related_name="reports")
    reported_user_flag = models.BooleanField(default=False)
    reported_user = models.ForeignKey(User,null=True,blank=True,related_name="reports")
    reported_bug_flag = models.BooleanField(default=False)
    reported_general_flag = models.BooleanField(default=False)
    contact_email = models.EmailField(null=True,blank=True)
    contact_phone_number = models.CharField(max_length=20, null=True,blank=True)
    description = models.CharField(max_length=255,null=True,blank=True)
    datetime_reported = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)


class Search(models.Model):
    search_id = models.AutoField(primary_key=True)
    user_search_id = models.BigIntegerField(default=1)
    user_searching = models.ForeignKey(User,related_name="searches")
    explore_searched_flag = models.BooleanField(default=False)
    stream_searched_flag = models.BooleanField(default=False)
    profile_searched_flag = models.BooleanField(default=False)
    yap_searched_flag = models.BooleanField(default=False)
    profile_searched = models.ForeignKey(User,blank=True,null=True)
    profile_posts_stream_searched_flag = models.BooleanField(default=False)
    profile_likes_stream_searched_flag = models.BooleanField(default=False)
    profile_listens_stream_searched_flag = models.BooleanField(default=False)
    hashtags_searched_flag = models.BooleanField(default=False)
    hashtags_searched = models.ManyToManyField(Hashtag,related_name="in_searches",blank=True,null=True)
    channels_searched_flag = models.BooleanField(default=False)
    channels_searched = models.ManyToManyField(Channel,related_name="in_searches",blank=True,null=True)
    user_handles_searched_flag = models.BooleanField(default=False)
    user_handles_searched = models.ManyToManyField(User,related_name="in_searches",blank=True,null=True)
    general_searched_flag = models.BooleanField(default=False)
    text_searched = models.CharField(max_length=255)
    longitude = models.FloatField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    is_after_request = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_recent = models.BooleanField(default=False)
    is_people = models.BooleanField(default=False)
    date_searched = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_searched']

class Stream(models.Model):
    '''table containing each post for each user that goes to their stream'''
    post_id = models.AutoField(primary_key=True)
    user_post_id = models.BigIntegerField(blank=True) #a number corresponding to the number post in an individual users stream
    user = models.ForeignKey(User,related_name="stream")
    user_posted = models.ForeignKey(User,related_name="posted_to",null=True,blank=True)
    yap = models.ForeignKey(Yap,related_name="stream")
    reyap_flag = models.BooleanField(default=False)
    reyap = models.ForeignKey(Reyap, null=True, blank=True,related_name="stream")
    date_created = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']
        #Changed user_posting to user_posted

class DeactivateUserLog(models.Model):
    deactivate_user_log_id = models.AutoField(primary_key=True)
    user_deactivate_user_log_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="deactivate_user_logs")
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']


class BlackList(models.Model):
    blacklist_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,unique=True)
    account_created_flag = models.BooleanField(default=False)
    account_created_date = models.DateTimeField(blank=True,null=True)
    blacklisted_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


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


class Recommended(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user_recommendation_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name='recommended')
    date_recommended = models.DateTimeField(auto_now_add=True)
    date_will_be_deactivated = models.DateTimeField(null=True,blank=True)
    date_deactivated = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_user_deleted = models.BooleanField(default=False)


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


class UserFunctions(models.Model):
    user = models.OneToOneField(User, primary_key=True,related_name="functions")
    is_user_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class SessionVerification(models.Model):
    session_user = models.OneToOneField(User,related_name="session",primary_key=True)
    session_id = models.BigIntegerField(null=True,blank=True)
    session_udid = models.CharField(max_length=255,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)


class ManualOverride(models.Model):
    manual_override_id = models.AutoField(primary_key=True)
    user_manual_override_id = models.BigIntegerField(default=1)
    manual_override_description = models.CharField(max_length=255)
    user_override_flag = models.BooleanField(default=False)
    user_override_object = models.ForeignKey(User,related_name="manual_overrides")
    blacklist_override_flag = models.BooleanField(default=False)
    blacklist_override_object = models.ForeignKey(BlackList,related_name="manual_overrides")
    profile_override_flag = models.BooleanField(default=False)
    profile_override_object = models.ForeignKey(Profile,related_name="manual_overrides")
    user_info_override_flag = models.BooleanField(default=False)
    user_info_override_object = models.ForeignKey(UserInfo,related_name="manual_overrides")
    settings_override_flag = models.BooleanField(default=False)
    settings_override_object = models.ForeignKey(Settings,related_name="manual_overrides")
    recommended_override_flag = models.BooleanField(default=False)
    recommended_override_object = models.ForeignKey(Recommended,related_name="manual_overrides")
    forgot_password_request_override_flag = models.BooleanField(default=False)
    forgot_password_request_override_object = models.ForeignKey(ForgotPasswordRequest,related_name="manual_overrides")
    user_functions_override_flag = models.BooleanField(default=False)
    user_functions_override_object = models.ForeignKey(UserFunctions,related_name="manual_overrides")
    session_verification_override_flag = models.BooleanField(default=False)
    session_verification_override_object = models.ForeignKey(SessionVerification,related_name="manual_overrides")
    stream_override_flag = models.BooleanField(default=False)
    stream_override_object = models.ForeignKey(Stream,related_name="manual_overrides")
    hashtag_override_flag = models.BooleanField(default=False)
    hashtag_override_object = models.ForeignKey(Hashtag,related_name="manual_overrides")
    channel_override_flag = models.BooleanField(default=False)
    channel_override_object = models.ForeignKey(Channel,related_name="manual_overrides")
    yap_override_flag = models.BooleanField(default=False)
    yap_override_object = models.ForeignKey(Yap,related_name="manual_overrides")
    reyap_override_flag = models.BooleanField(default=False)
    reyap_override_object = models.ForeignKey(Reyap,related_name="manual_overrides")
    like_override_flag = models.BooleanField(default=False)
    like_override_object = models.ForeignKey(Like,related_name="manual_overrides")
    listen_override_flag = models.BooleanField(default=False)
    listen_override_object = models.ForeignKey(Listen,related_name="manual_overrides")
    listen_click_override_flag = models.BooleanField(default=False)
    listen_click_override_object = models.ForeignKey(ListenClick,related_name="manual_overrides")
    follower_request_override_flag = models.BooleanField(default=False)
    follower_request_override_object = models.ForeignKey(FollowerRequest,related_name="manual_overrides")
    notification_type_override_flag = models.BooleanField(default=False)
    notification_type_override_object = models.ForeignKey(NotificationType,related_name="manual_overrides")
    notification_override_flag = models.BooleanField(default=False)
    notification_override_object = models.ForeignKey(Notification,related_name="manual_overrides")
    search_override_flag = models.BooleanField(default=False)
    search_override_object = models.ForeignKey(Search,related_name="manual_overrides")
    report_override_flag = models.BooleanField(default=False)
    report_override_object = models.ForeignKey(Report,related_name="manual_overrides")
    geographic_target_override_flag = models.BooleanField(default=False)
    geographic_target_override_object = models.ForeignKey(GeographicTarget,related_name="manual_overrides")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_created']

