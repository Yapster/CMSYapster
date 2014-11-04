from django.contrib.auth.models import User
from rest_framework import serializers
from search.models import *

class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search