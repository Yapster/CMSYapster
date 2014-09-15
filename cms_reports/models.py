from django.db import models
from django.contrib.auth.models import User


class TypeReport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=24)
    color = models.CharField(max_length=6)

class CmsReport(models.Model):
    TODO = 'TO'
    IN_PROGRESS = 'IP'
    DONE = 'DO'
    STATUS_CHOICES = (
        (TODO, 'Todo'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
    )
    id = models.AutoField(primary_key=True)
    report_id = models.IntegerField(default=0)
    user_in_charge = models.ForeignKey(User, related_name="user_in_charge")
    #status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=TODO)
    #kind = models.ForeignKey(to='TypeReport', related_name="kind")
    date_created = models.DateTimeField(auto_now_add=True)

class ReportNote(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(to=User, related_name='report_note_owner')
    report = models.ForeignKey(to=CmsReport, related_name='notes')
    text = models.CharField(max_length=255)
    date_last = models.DateTimeField(auto_now=True)