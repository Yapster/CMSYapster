from django.contrib.auth.models import User
from rest_framework import serializers
from notification.models import *

class NotificationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationType

class SingleNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
