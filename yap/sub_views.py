from stats.models import YapManager, UserManager, ListenManager, HashtagManager, CountryManager, ReyapManager
from yap.models import Yap, Listen, Hashtag, Reyap, Like
from users.models import UserInfo
user_manager = UserManager()

def get_home_data(**kwargs):
    data = []
    data.append({"Yap Count": YapManager.yap_count(**kwargs)})
    data.append({"Total Number of Active Users": UserManager.active_users_count(**kwargs)})
    data.append({"Total Number of Listens": ListenManager.listen_count(**kwargs)})
    data.append({"Average Time Listened": ListenManager.average_time_listened(**kwargs)})
    data.append({"Trending Hashtags": HashtagManager.top_hashtags(amount=5, **kwargs)})

    return data


def get_users_data(**kwargs):
    data = []
    data.append({"users_count": UserManager.users_count(**kwargs)})
    data.append({"active_users_count": UserManager.active_users_count(**kwargs)})
    data.append({"new_users_count": UserManager.new_users_count(**kwargs)})
    #data.append({"Birthdays Today": UserInfo.stats.birthday_month_users(**kwargs)})
    return data


def get_yaps_data(**kwargs):
    data = []
    data.append({"yap_count": YapManager.yap_count(**kwargs)})
    data.append({"active_yap_count": YapManager.active_yap_count(**kwargs)})
    data.append({"total_time_yapped": YapManager.total_time_yapped(**kwargs)})
    data.append({"total_active_time_yapped": YapManager.total_active_time_yapped(**kwargs)})
    data.append({"average_time_yapped": YapManager.average_time_yapped(**kwargs)})
    data.append({"average_active_time_yapped": YapManager.average_active_time_yapped(**kwargs)})
    data.append({"average_yap_per_user": YapManager.average_yap_per_user(**kwargs)})

    return data


def get_reyaps_data(**kwargs):
    data = []
    data.append({"reyap_count": Reyap.stats.reyap_count(**kwargs)})
    data.append({"active_reyap_count": Reyap.stats.active_reyap_count(**kwargs)})
    data.append({"new_reyap_count": Reyap.stats.new_reyap_count(**kwargs)})

    return data

def get_listens_data(**kwargs):
    data = []
    data.append({"listen_count": ListenManager.listen_count(**kwargs)})
    data.append({"active_listen_count": ListenManager.active_listen_count(**kwargs)})
    data.append({"total_time_listened": ListenManager.total_time_listened(**kwargs)})
    data.append({"total_active_time_listened": ListenManager.total_active_time_listened(**kwargs)})
    data.append({"average_time_listened": ListenManager.average_time_listened(**kwargs)})
    data.append({"average_active_time_listened": ListenManager.average_active_time_listened(**kwargs)})
    data.append({"average_time_listened_per_user": ListenManager.average_time_listened_per_user(**kwargs)})
    # data.append({"": })
    # data.append({"": })
    # data.append({"": })

    return data


def get_country_data(**kwargs):
    data = []
    data.append({"Top Countries": CountryManager.top_countries()})
    return data


def get_hashtags_data(**kwargs):
    data = []
#    data.append({"": })
    return data


def get_likes_data(**kwargs):
    data = []
    #data.append({"": })
    return data