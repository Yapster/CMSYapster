from django.db import models
from django.contrib.auth.models import User

class CmsNotificationType(models.Model):
    """
    For different types of cms_notifications
    """
    notification_type_id = models.AutoField(primary_key=True)
    notification_name = models.CharField(max_length=24, unique=True)
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        self.save()
        return

class CmsNotification(models.Model):
    """
    Notification for CMS Users
    """
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='cms_notifications')
    notification_type = models.ForeignKey(CmsNotificationType, related_name='cms_notifications')
    description = models.CharField(blank=True, max_length=255)
    been_seen = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        self.save()
        return