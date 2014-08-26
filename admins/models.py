from collections import defaultdict
from django.db import models
from django.contrib.auth.models import User
from groups.models import GroupPermission
from calendars.models import MyCalendar

import logging

logger = logging.getLogger(__name__)


class CmsUser (models.Model):
    """
    CMS User account
    """
    user = models.OneToOneField(User, primary_key=True, related_name='account')
    yapster_user_id = models.CharField(max_length=10, default="")
    username = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    group = models.ManyToManyField(to=GroupPermission, blank=True, related_name='members')
    occupation = models.CharField(max_length=64, blank=True)
    department = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def new_user(*args, **kwargs):
        username = kwargs["username"]
        password = kwargs.pop('password')
        email = kwargs["email"]
        first_name = kwargs["first_name"]
        last_name = kwargs["last_name"]
        try:
            user = User.objects.create_user(username=username, email=email,
                                        password=password, first_name=first_name,
                                        last_name=last_name)
        except:
            return False
        kwargs["user"] = user
        group = None
        try:
            group = kwargs.pop('group')
        except KeyError:
            pass
        cmsuser = CmsUser.objects.create(**kwargs)
        if group:
                cmsuser.group.add(group)
        cal_name = first_name + " " + last_name
        MyCalendar.objects.create_calendar(user=user, name=cal_name)
        return user

    def update(self, *args, **kwargs):
        user = User.objects.get(username=self.username)
        if 'password' in kwargs:
            user.set_password(kwargs['password'])
            kwargs.pop('password')
        for (key, value) in kwargs.items():
            setattr(user, key, value)
            setattr(self, key, value)
        user.save()
        self.save()
        return self

    def delete(self, using=None):
        user = User.objects.get(pk=self.user)
        user.is_active = False
        self.is_active = False
        self.save()
        return