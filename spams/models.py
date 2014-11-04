from django.db import models

class Spam(models.Model):
    spam_id = models.AutoField(primary_key=True)
    spam_name = models.CharField(max_length=24)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default=True)