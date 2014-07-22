from django.contrib.auth.models import User
from rest_framework import serializers
from report.models import *

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report