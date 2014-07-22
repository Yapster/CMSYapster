from django.contrib.auth.models import User
from rest_framework import serializers
from yap.models import *


#THESE ARE THE MODEL SERIALIZERS
class PlatformUserSerializer(serializers.ModelSerializer):

    profile_picture_path = serializers.SerializerMethodField('get_profile_picture_path')
    profile_cropped_picture_path = serializers.SerializerMethodField('get_profile_cropped_picture_path')

    class Meta:
        model = User
        fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path")



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







