from stats.models import *
import datetime

def get_stat_method(name_method, type_stats):
    """

    :param name_method: String. Name of the method required
    :param type_stats: String. Name of the stats group
    :return:
    """
    global stat_method
    if type_stats == "usership":
        stat_method = getattr(UserManager, name_method)
    elif type_stats == "countries":
        stat_method = getattr(CountryManager, name_method)
    elif type_stats == "hashtags":
        stat_method = getattr(HashtagManager, name_method)
    elif type_stats == "listens":
        stat_method = getattr(ListenManager, name_method)
    elif type_stats == "yaps":
        stat_method = getattr(YapManager, name_method)
    elif type_stats == "likes":
        stat_method = getattr(LikeManager, name_method)
    elif type_stats == "reyaps":
        stat_method = getattr(ReyapManager, name_method)
    return stat_method


def get_time(date, time):
    l_date = date.split('-')
    l_time = time.split(':')
    return datetime.datetime(int(l_date[0]), int(l_date[1]), int(l_date[2]), int(l_time[0]), int(l_time[1]))