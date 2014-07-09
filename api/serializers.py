from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import *


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        exclude = ["is_active","date_activated","date_deactivated"]

class USZIPCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = USZIPCode
        exclude = ["is_active","date_activated","date_deactivated"]

class USStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = USState
        exclude = ["is_active","date_activated","date_deactivated"]

class CitySerializer(serializers.ModelSerializer):

    country = CountrySerializer
    usstates = USStateSerializer

    class Meta:
        model = City
        exclude = ["is_active","date_activated","date_deactivated"]

class NotificationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationType
        exclude = ["is_active","origin_yap_flag","origin_yap","origin_reyap_flag","origin_reyap","created_like_flag","created_like","created_reyap_flag","created_reyap","created_listener_request_flag","created_listener_request","created_listen_flag","created_listen","is_yapster_notification","manual_override","override_description"] #Front end doesn't need to know if it's active. The fact that they're receiving it means it's active.

class SingleNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        exclude = ["is_active","origin_yap_flag","origin_yap","origin_reyap_flag","origin_reyap","created_like_flag","created_like","created_reyap_flag","created_reyap","created_listener_request_flag","created_listener_request","created_listen_flag","created_listen","user_viewed_date","user_clicked_flag","user_clicked_date","manual_override","override_description"] #Front end doesn't need to know if it's active. The fact that they're receiving it means it's active.

class AbstractNotificationSerializer(serializers.ModelSerializer):
    liked_by_viewer = serializers.SerializerMethodField('get_liked_by_viewer')
    listened_by_viewer = serializers.SerializerMethodField('get_listened_by_viewer')
    reyapped_by_viewer = serializers.SerializerMethodField('get_reyapped_by_viewer')
    reyap_flag = serializers.SerializerMethodField('get_reyap_flag')
    reyap_id = serializers.SerializerMethodField('get_reyap_id')
    reyap_user = serializers.SerializerMethodField('get_reyap_user')
    date_created = serializers.SerializerMethodField('get_date_created')


    class Meta:
        model = Yap
        fields = ("reyap_flag","reyap_id","reyap_user","liked_by_viewer","listened_by_viewer","reyapped_by_viewer","date_created")

    def get_date_created(self,obj):
        return self.context['date_action_done']


class NotificationSerializer(serializers.Serializer):

    notification_id = serializers.SerializerMethodField('get_notification_id')
    notification_type = NotificationTypeSerializer()
    notification_info = serializers.SerializerMethodField('get_notification_info')
    notification_created_info = serializers.SerializerMethodField('get_notification_created_info')


class ExploreSearchResultsSerializer(serializers.Serializer):
    yap_id = serializers.SerializerMethodField("get_post_id")
    post_info = serializers.SerializerMethodField("get_post_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")


class ExplorePeopleSearchSerializer(serializers.ModelSerializer):
    following_info = serializers.SerializerMethodField("get_user_following_info")
    profile_picture_path = serializers.SerializerMethodField("get_profile_picture_path")
    profile_cropped_picture_path = serializers.SerializerMethodField("get_profile_cropped_picture_path")
    user_following_listed_user = serializers.SerializerMethodField("get_user_following_listed_user")

    class Meta:
        model = User
        fields = ("id","username","first_name","last_name","profile_picture_path","profile_cropped_picture_path","user_following_listed_user")


class ProfileSearchResultsSerializer(serializers.Serializer):
    date_created = serializers.SerializerMethodField("get_date_created")
    post_info = serializers.SerializerMethodField("get_post_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")


class StreamSearchResultsSerializer(serializers.Serializer):
    user_post_id = serializers.SerializerMethodField("get_user_post_id")
    post_info = serializers.SerializerMethodField("get_post_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")

class UserSerializer(serializers.ModelSerializer):

    profile_picture_path = serializers.SerializerMethodField('get_profile_picture_path')
    profile_cropped_picture_path = serializers.SerializerMethodField('get_profile_cropped_picture_path')

    class Meta:
        model = User
        fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path")


class ListUserSerializer(serializers.ModelSerializer):

    profile_picture_path = serializers.SerializerMethodField("get_profile_picture_path")
    profile_cropped_picture_path = serializers.SerializerMethodField("get_profile_cropped_picture_path")
    description = serializers.SerializerMethodField("get_description")

    class Meta:
        model = User
        fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path","description")

class RecommendedSerializer(serializers.ModelSerializer):

    user = ListUserSerializer()

    class Meta:
        model = Recommended
        fields = ("user",)

class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Settings
        exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

class AbstractPostSerializer(serializers.ModelSerializer):
    liked_by_viewer = serializers.SerializerMethodField('get_liked_by_viewer')
    listened_by_viewer = serializers.SerializerMethodField('get_listened_by_viewer')
    reyapped_by_viewer = serializers.SerializerMethodField('get_reyapped_by_viewer')
    reyap_flag = serializers.SerializerMethodField('get_reyap_flag')
    reyap_id = serializers.SerializerMethodField('get_reyap_id')
    reyap_user = serializers.SerializerMethodField('get_reyap_user')
    date_created = serializers.SerializerMethodField('get_date_created')

    class Meta:
        model = Yap
        fields = ("reyap_flag","reyap_id","reyap_user","liked_by_viewer","listened_by_viewer","reyapped_by_viewer","date_created")


class PostSerializer(serializers.Serializer):
    user_post_id = serializers.SerializerMethodField("get_post_id")
    post_info = serializers.SerializerMethodField("get_post_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")


class ProfileInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True) #not return all info in this
    following_info = serializers.SerializerMethodField("get_following_info")
    user_city = CitySerializer()
    user_country = CountrySerializer()
    user_us_state = USStateSerializer()
    user_us_zip_code = USZIPCodeSerializer()
    last_user_yap_id = serializers.SerializerMethodField("get_last_user_yap_id")

    class Meta:
        model = Profile
        exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']


class EditProfileInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True) #not return all info in this
    user_city = CitySerializer()
    user_country = CountrySerializer()
    user_us_state = USStateSerializer()
    user_us_zip_code = USZIPCodeSerializer()

    class Meta:
        model = Profile
        exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

class EditUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True) #not return all info in this
    user_city = CitySerializer()
    user_country = CountrySerializer()
    user_us_state = USStateSerializer()
    user_us_zip_code = USZIPCodeSerializer()

    class Meta:
        model = UserInfo

class ProfileStreamSerializer(serializers.Serializer):
    post_info = serializers.SerializerMethodField("get_post_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")


#Profile Stream Serializer for Posts

class ProfilePostStreamSerializer(serializers.Serializer):
    post_date_created = serializers.SerializerMethodField("get_post_date_created")
    post_info = serializers.SerializerMethodField("get_post_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")


class ProfileLikeStreamSerializer(serializers.Serializer):
    like_id = serializers.SerializerMethodField("get_like_id")
    post_info = serializers.SerializerMethodField("get_post_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")


class ProfileListenStreamSerializer(serializers.Serializer):
    listen_id = serializers.SerializerMethodField("get_listen_id")
    post_info = serializers.SerializerMethodField("get_post_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")



class PushNotificationObjectSerializer(serializers.Serializer):
    object_id = serializers.SerializerMethodField("get_object_id")
    object_info = serializers.SerializerMethodField("get_object_info")
    yap_info = serializers.SerializerMethodField("get_yap_info")


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        exclude = ["date_activated","date_deactivated","is_active","manual_override","manual_override_description","icon_explore_path_clicked","icon_explore_path_unclicked","icon_yap_path_clicked","icon_yap_path_unclicked"]

class YapChannelListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        exclude = ["icon_explore_path_clicked","icon_explore_path_unclicked","date_activated","date_deactivated","is_active","manual_override","manual_override_description"]

class ExploreChannelListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        exclude = ["icon_yap_path_clicked","icon_yap_path_unclicked","date_activated","date_deactivated","is_active","manual_override","manual_override_description"]

class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        exclude = ["is_active","is_blocked"]

class YapSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)
    hashtags = HashtagSerializer()
    channel = ChannelSerializer()
    user_tags = UserSerializer(partial=True)

    class Meta:
        model = Yap

class InternalReyapSerializer(serializers.ModelSerializer):
    yap = YapSerializer()
    reyapped_from = serializers.SerializerMethodField('reyapped_from')

    class Meta:
        model = Reyap
        exclude = ["reyap_reyap","reyap_flag","is_active","manual_override","manual_override_description"]


class ReyapSerializer(serializers.ModelSerializer):
    yap = YapSerializer()
    reyapped_from = serializers.SerializerMethodField('reyapped_from')
    reyap_reyap = InternalReyapSerializer()

    class Meta:
        model = Reyap


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)
    yap = YapSerializer()
    reyap = ReyapSerializer()

    class Meta:
        model = Like
        exclude = ["is_active","manual_override","manual_override_description"]

class ListenSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)
    yap = YapSerializer()
    reyap = ReyapSerializer()

    class Meta:
        model = Listen
        exclude = ["is_active","manual_override","manual_override_description"]

class FollowerRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)
    user_requested = UserSerializer(partial=True)

    class Meta:
        model = FollowerRequest
        exclude = ["is_active","manual_override","manual_override_description"]


class ListOfFollowersSerializer(serializers.ModelSerializer):
    user = ListUserSerializer(partial=True) #not return all info in this
    user_requested = UserSerializer(partial=True)
    profile_user_following = serializers.SerializerMethodField("get_user_following_info")

    class Meta:
        model = FollowerRequest


class ListOfFollowingSerializer(serializers.ModelSerializer):
    user = ListUserSerializer(partial=True) #not return all info in this
    user_requested = UserSerializer(partial=True)
    profile_user_following = serializers.SerializerMethodField("get_user_following_info")

    class Meta:
        model = FollowerRequest


class ListOfFollowingAndFollowersSerializer(serializers.ModelSerializer):
    user = ListUserSerializer(partial=True) #not return all info in this
    user_requested = ListUserSerializer(partial=True)
    relationship_type = serializers.SerializerMethodField("get_relationship_type")

    class Meta:
        model = FollowerRequest

