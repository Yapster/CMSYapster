from django.db import models
from admins.models import User


class ReportType(models.Model):
    report_type_id = models.AutoField(primary_key=True)
    report_name = models.CharField(max_length=24, unique=True)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, related_name="reports")
    report_type = models.ForeignKey(to=ReportType, related_name="reports")
    title = models.CharField(max_length=24)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default=True)
