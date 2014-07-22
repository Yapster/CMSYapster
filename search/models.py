from django.db import models
from yap.models import Hashtag, Channel
from users.models import User

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

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Searches cannot be deleted.')