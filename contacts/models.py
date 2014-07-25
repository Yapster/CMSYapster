from django.contrib.admindocs.views import model_detail
from users.models import User
from django.db import models
from users.models import Profile
from groups.models import GroupPermission, Page
from cms_location.models import *

class List(models.Model):
    """
    List of contacts. Link to one/many groups
    """
    list_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128, blank=True)
    created_by = models.ForeignKey(to=User, related_name='contact_lists')
    groups = models.ManyToManyField(to=GroupPermission, related_name='groups_perms')
    is_active = models.BooleanField(default=True)

    def create(self):
        """
        Create a list and Create a page associated
        """


    def delete(self, using=None):
        self.is_active = False
        self.save()
        return

    def activate(self, using=None):
        self.is_active = True
        self.save()
        return

class Contact(models.Model):
    """
    Contact of a person known by Yapster team
    """
    contact_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=64, blank=True)
    lastname = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=20, blank=True, default="No Phone")
    email = models.EmailField(max_length=64, blank=True, default="No Email")
    description = models.CharField(max_length=100, blank=True, default="No Description")
    birthday = models.DateField(blank=True, null=True)
    city = models.ForeignKey(CmsCity, blank=True, null=True)
    state = models.ForeignKey(CmsUSState, blank=True, null=True)
    zipcode = models.ForeignKey(CmsUSZIPCode, blank=True, null=True)
    country = models.ForeignKey(CmsCountry, blank=True, null=True)
    lists = models.ManyToManyField(to=List, related_name='contacts')
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        self.save()
        return

    def activate(self, using=None):
        self.is_active = True
        self.save()
        return


class Website(models.Model):
    website_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    url = models.URLField(max_length=128)
    contact = models.ForeignKey(to=Contact, related_name='websites')
    is_active = models.BooleanField(default=True)


class Note(models.Model):
    """
    Note leave by any Cmsuser concerning the contact
    """
    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    date_last = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, related_name='created_notes')
    contact = models.ForeignKey(to=Contact, related_name='notes')
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        self.save()
        return

    def activate(self, using=None):
        self.is_active = True
        self.save()
        return