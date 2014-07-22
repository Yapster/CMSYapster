from django.db import models
from django.contrib.auth.models import User
from yap.models import Hashtag, Channel

class CmsSearchLog(models.Model):
    search_id = models.AutoField(primary_key=True)
    user_search_id = models.BigIntegerField(default=1)
    user_searching = models.ForeignKey(User,related_name="cms_searches")
    user_searched_flag = models.BooleanField(default=False)
    yap_searched_flag = models.BooleanField(default=False)
    reyap_searched_flag = models.BooleanField(default=False)
    like_searched_flag = models.BooleanField(default=False)
    listen_searched_flag = models.BooleanField(default=False)
    channel_searched_flag = models.BooleanField(default=False)
    hashtag_searched_flag = models.BooleanField(default=False)
    report_searched_flag = models.BooleanField(default=False)
    general_searched_flag = models.BooleanField(default=False)
    text_searched = models.CharField(max_length=255)

    longitude = models.FloatField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    date_searched = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_searched']