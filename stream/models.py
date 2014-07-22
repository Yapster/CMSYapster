from django.db import models
from users.models import User
from yap.models import Yap, Reyap

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

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Stream objects cannot be deleted.')
