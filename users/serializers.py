from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import *

class DeactivateUserLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeactivateUserLog

class BlackListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlackList

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo

class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Settings

class RecommendedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommended

class ForgotPasswordRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForgotPasswordRequest

class UserFunctionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFunctions

class SessionVerificiationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SessionVerification

class ManualOverrideSerializer(serializers.ModelSerializer):

    class Meta:
        model = SessionVerification

