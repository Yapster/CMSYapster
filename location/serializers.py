from django.contrib.auth.models import User
from rest_framework import serializers
from location.models import *

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country

class USZIPCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = USZIPCode

class USStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = USState

class CitySerializer(serializers.ModelSerializer):

    country = CountrySerializer
    usstates = USStateSerializer

    class Meta:
        model = City