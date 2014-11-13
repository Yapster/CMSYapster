from stats.models import YapManager, UserManager, ListenManager, HashtagManager, CountryManager, ReyapManager
from yap.models import Yap, Listen, Hashtag, Reyap, Like
from users.models import UserInfo
user_manager = UserManager()

def get_home_data():
    data = []
    data.append({"Yap Count": Yap.stats.yap_count()})
    data.append({"Total Number of Active Users": UserInfo.stats.active_users_count()})
    data.append({"Total Number of Listens": Listen.stats.listen_count()})
    data.append({"Average Time Listened": Listen.stats.average_time_listened()})
    data.append({"Trending Hashtags": Hashtag.stats.top_hashtags(amount=5)})

    return data


def get_users_data(**kwargs):
    data = []
    data.append({"Total Number of Users": UserInfo.stats.users_count(**kwargs)})
    data.append({"Total Number of Active Users": UserInfo.stats.active_users_count(**kwargs)})
    data.append({"Total New Users": UserInfo.stats.new_users_count(**kwargs)})
    #data.append({"Birthdays Today": UserInfo.stats.birthday_month_users(**kwargs)})
    return data


def get_yaps_data(**kwargs):
    data = []
    data.append({"yap_count": Yap.stats.yap_count(**kwargs)})
    data.append({"active_yap_count": Yap.stats.active_yap_count(**kwargs)})
    data.append({"total_time_yapped": Yap.stats.total_time_yapped(**kwargs)})
    data.append({"total_active_time_yapped": Yap.stats.total_active_time_yapped(**kwargs)})
    data.append({"average_time_yapped": Yap.stats.average_time_yapped(**kwargs)})
    data.append({"average_active_time_yapped": Yap.stats.average_active_time_yapped(**kwargs)})
    data.append({"average_yap_per_user": Yap.stats.average_yap_per_user(**kwargs)})

    return data


def get_reyaps_data(**kwargs):
    data = []
    data.append({"Total Number of Reyaps": Reyap.stats.reyap_count(**kwargs)})
    data.append({"Total Number of active Reyaps": Reyap.stats.active_reyap_count(**kwargs)})
    data.append({"Total Number of active Reyaps": Reyap.stats.new_reyap_count(**kwargs)})

    return data

def get_listens_data(**kwargs):
    data = []
    data.append({"Total Number of Listens": Listen.stats.listen_count(**kwargs)})
    data.append({"Total Number of Active Listens": Listen.stats.active_listen_count(**kwargs)})
    data.append({"Total Listened Time": Listen.stats.total_time_listened(**kwargs)})
    data.append({"Total Active Time Listened": Listen.stats.total_active_time_listened(**kwargs)})
    data.append({"Average Time Listened": Listen.stats.average_time_listened(**kwargs)})
    data.append({"Average Active Time Listened": Listen.stats.average_active_time_listened(**kwargs)})
    data.append({"Average Time Listened Per User": Listen.stats.average_time_listened_per_user(**kwargs)})
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