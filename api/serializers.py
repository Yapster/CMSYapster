from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import *

#THESE ARE THE MODEL SERIALIZERS
class PlatformUserSerializer(serializers.ModelSerializer):

    profile_picture_path = serializers.SerializerMethodField('get_profile_picture_path')
    profile_cropped_picture_path = serializers.SerializerMethodField('get_profile_cropped_picture_path')

    class Meta:
        model = User
        fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path")

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

class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag

class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel

class YapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Yap

class ReyapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reyap

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like

class ListenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listen

class ListenClickSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListenClick

class FollowerRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowerRequest


class NotificationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationType

class SingleNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report

class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search

class StreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stream

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

