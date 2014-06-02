from django.db import models
from django.contrib.auth.models import User

class Announcement(models.Model):
    """
    Annoucements for homepage
    """
    announcement_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='announces')
    title = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_edit = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        return
