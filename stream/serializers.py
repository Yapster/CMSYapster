from django.contrib.auth.models import User
from rest_framework import serializers
from stream.models import *


class StreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stream