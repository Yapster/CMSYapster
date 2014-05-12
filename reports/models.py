from django.db import models
from admins.models import User


class ReportType(models.Model):
    """
    Type of a report : User to User, Yap, General
    """
    report_type_id = models.AutoField(primary_key=True)
    report_name = models.CharField(max_length=24, unique=True)


class Report(models.Model):
    """
    Report from users
    """
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, related_name="reports")
    cms_user = models.ForeignKey(to=User, related_name="reports_in_charge")
    report_type = models.ForeignKey(to=ReportType, related_name="reports")
    title = models.CharField(max_length=24)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default=True)
