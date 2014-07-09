from django.db import models
from django.contrib.auth.models import User
from groups.models import GroupPermission


class Profile(models.Model):
    """
    Profile of a Yapster user
    """
    GENDER_CHOICE = {
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    }

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
        self.save()
        return

class CmsUser (models.Model):
    """
    CMS User account
    """
    user = models.OneToOneField(User, primary_key=True, related_name='account')
    username = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    group = models.ManyToManyField(to=GroupPermission, blank=True, related_name='members')
    occupation = models.CharField(max_length=64, blank=True)
    department = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)

    def new_user(*args, **kwargs):
        username = kwargs["username"]
        password = kwargs.pop('password')
        email = kwargs["email"]
        first_name = kwargs["first_name"]
        last_name = kwargs["last_name"]
        user = User.objects.create_user(username=username, email=email,
                                        password=password, first_name=first_name,
                                        last_name=last_name)
        kwargs["user"] = user
        CmsUser.objects.create(**kwargs)
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

#TODO: Write Userfunction model to call different functions