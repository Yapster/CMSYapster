from django.db import models
from admins.models import Profile, User


class Search(models.Model):
    """
    Research made by a CMS User
    """
    search_id = models.AutoField(primary_key=True)
    user_searching = models.ForeignKey(User, related_name="searches")


class Yap(models.Model):
    """
    Yap stats
    """
    yap_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, related_name="Yaps")
    title = models.CharField(max_length=24)
    date_created = models.DateTimeField(auto_now_add=True)
    listen_count = models.BigIntegerField(default=0)
    reyaps_count = models.BigIntegerField(default=0)
    likes_count = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)


class Group(models.Model):
    """
    Group page stats
    """
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    members_count = models.BigIntegerField(default=0)
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class Hashtag(models.Model):
    """
    Hashtag stats
    """
    hashtag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    used_count = models.BigIntegerField(default=0)
    date_created = models.DateTimeField()


class Reyap(models.Model):
    """
    Reyap table
    """
    reyap_id = models.AutoField(primary_key=True)
    yap = models.ForeignKey(to=Yap, related_name="reyaps")
    user = models.ForeignKey(to=User, related_name="reyaps")
    likes_count = models.BigIntegerField(default=0)
    listen_count = models.BigIntegerField(default=0)
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class Listen(models.Model):
    """
    Listened table
    """
    listen_id = models.AutoField(primary_key=True)
    yap = models.ForeignKey(to=Yap, related_name="listens")
    user = models.ForeignKey(to=User, related_name="listens")
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class Like(models.Model):
    """
    Liked table
    """
    like_id = models.AutoField(primary_key=True)
    yap = models.ForeignKey(to=Yap, related_name="likes")
    user = models.ForeignKey(to=User, related_name="likes")
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class Stat(models.Model):
    """
    Statistic for an interval of time (to determinate)
    """
    stat_id = models.AutoField(primary_key=True)
    users_count = models.BigIntegerField(default=0)
    active_users_count = models.BigIntegerField(default=0)
    new_users_count = models.BigIntegerField(default=0)
    yaps_count = models.BigIntegerField(default=0)
    new_yaps_count = models.BigIntegerField(default=0)
    yaps_from = models.CharField(max_length=255, blank=True)
    new_yaps_from = models.CharField(max_length=255, blank=True)
    users_from = models.CharField(max_length=255, blank=True)
    new_users_from = models.CharField(max_length=255, blank=True)
    active_users_from = models.CharField(max_length=255, blank=True)
    total_listens_count = models.BigIntegerField(default=0)
    listens_from = models.CharField(max_length=255, blank=True)
    yaps_listened_from = models.CharField(max_length=255, blank=True)
    most_listened_from = models.CharField(max_length=255, blank=True)
    likes_average = models.FloatField(default=0)
    listens_per_user_count = models.FloatField(default=0, )
    listens_per_total_users_average = models.FloatField(default=0)
    likes_per_total_users_average = models.FloatField(default=0)
    yaps_per_total_users_average = models.FloatField(default=0)
    listens_per_total_active_users_average = models.FloatField(default=0)
    likes_per_total_active_users_average = models.FloatField(default=0)
    yaps_per_total_active_users_average = models.FloatField(default=0)
    yaps_time = models.DateTimeField()
    listened_time = models.DateTimeField()
    listening_to_relationships_count = models.FloatField(default=0)
    listeners_relationships_count = models.BigIntegerField(default=0)
    relationships_count = models.BigIntegerField(default=0)
    reyaps_count = models.BigIntegerField(default=0)
    reyaps_per_user_average = models.FloatField(default=0)
    reyaps_per_total_users_average = models.FloatField(default=0)
    reyaps_per_active_users_average = models.FloatField(default=0)
    photos_yapped_count = models.BigIntegerField(default=0)
    links_yapped_count = models.BigIntegerField(default=0)
    facebook_connected_count = models.BigIntegerField(default=0)
    twitter_connected_count = models.BigIntegerField(default=0)
    age_users_average = models.FloatField(default=0)
    age_active_users_average = models.FloatField(default=0)
    age_new_users_average = models.FloatField(default=0)
    hashtags_average = models.FloatField(default=0)
    hashtags_per_user_count = models.FloatField(default=0)
    hashtags_per_active_users = models.FloatField(default=0)
    hashtags_popular = models.ManyToManyField(to=Hashtag, related_name="top_tags")
    users_popular = models.ManyToManyField(to=User, related_name="top_users")
    reyaps_popular = models.ManyToManyField(to=Reyap, related_name="top_reyaps")
    yaps_popular = models.ManyToManyField(to=Yap, related_name="top_yaps")
    liked_yaps_popular = models.ManyToManyField(to=Like, related_name="top_likes")
    played_yaps_popular = models.ManyToManyField(to=Yap, related_name="top_played_yaps")
    yaps_per_user_count = models.FloatField(default=0)
    requests_count = models.BigIntegerField(default=0)
    cost_per_user_average = models.FloatField(default=0)
    total_cost_count = models.FloatField(default=0)