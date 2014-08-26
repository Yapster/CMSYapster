from django.db import models
from django.contrib.auth.models import User

class CmsSearchLog(models.Model):
    search_id = models.AutoField(primary_key=True)
    user_searching = models.ForeignKey(User,related_name="cms_searches")
    type_search = models.CharField(max_length=64)
    text_searched = models.CharField(max_length=255)

    longitude = models.FloatField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    date_searched = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def create(params, **kwargs):
        kwargs['user_searching'] = params['current_user']
        kwargs['type_search'] = params['type_search']
        if 'searchexp' in params:
            kwargs['text_searched'] = params['searchexp']

        CmsSearchLog.objects.create(**kwargs)
        return

    class Meta:
        ordering = ['-date_searched']