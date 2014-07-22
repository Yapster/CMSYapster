from django.db import models
from users.models import User
from yap.models import Yap, Reyap

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user_report_id = models.BigIntegerField(default=1)
    user = models.ForeignKey(User,related_name="reported")
    reported_yap_flag = models.BooleanField(default=False)
    reported_yap = models.ForeignKey(Yap,null=True,blank=True,related_name="report")
    reported_reyap_flag = models.BooleanField(default=False)
    reported_reyap = models.ForeignKey(Reyap,null=True,blank=True,related_name="report")
    reported_user_flag = models.BooleanField(default=False)
    reported_user = models.ForeignKey(User,null=True,blank=True,related_name="report")
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

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Reports cannot be deleted.')