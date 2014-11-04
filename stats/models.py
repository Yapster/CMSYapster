from yap.models import *
from django.contrib.gis.db import models
from django.db.models import Sum, Count, Avg
import operator


class UserManager(models.Manager):
    """
    UserManager for stats
    """
    def users_count(self,
                    type_search="now",
                    time_start=None,
                    time_end=None):
        """
        Count users
        :param type_search: If Now or on an interval
        :param time_start: Date begin if interval
        :param time_end: Date end if interval
        :return: Int = Count users
        """
        return self.using('ye_1_db_1').count()

    def active_users_count(self,
                           type_search="now",
                           time_start=None,
                           time_end=None):
        """
        Count Active users
        :param type_search: If Now or on an interval
        :param time_start: Date begin if interval
        :param time_end: Date end if interval
        :return: Int = Count Active users
        """
        return self.using('ye_1_db_1').filter(is_active=True).count()

    def birthday_today_users(self,
                             users=User.objects.using('ye_1_db_1').all()):
        return users.filter(profile__date_of_birth__month=datetime.date.today().month)

    def new_users_count(self,
                        type_search="now",
                        time_start=None,
                        time_end=None):
        """
        Count New users
        :param type_search: If Now or on an interval
        :param time_start: Date begin if interval
        :param time_end: Date end if interval
        :return: Int = Count New users
        """

        time = time_end - time_start
        return self.using('ye_1_db_1').filter(date_joined__gte=time)


class CountryManager(models.Manager):
    def top_countries(self,
                      type_search="now",
                      time_start=None,
                      time_end=None,
                      countries=Country.objects.all(),
                      users=User.objects.using('ye_1_db_1').all(),
                      amount=5):
        """
        Get list of top countries
        :param type_search: If Now or on an interval
        :param time_start: Date begin if interval
        :param time_end: Date end if interval
        :param countries: Query of All Countries or specific countries
        :param users: Query of All users or specific users
        :param amount: Amount of users needed
        :return:
        """
        d_countries = {}

        for country in countries:
            d_countries[country.country_name] = users.filter(profile__user_country_id=country.country_id).count()
        return sorted(d_countries.iteritems(), key=operator.itemgetter(1), reverse=True)[:amount]


class HashtagManager(models.Manager):
    def top_hashtags(self,
                     type_search="now",
                     time_start=None,
                     time_end=None,
                     hashtags=Hashtag.objects.all(),
                     amount=5):
        """
        Get list of top hashtags
        :param type_search:
        :param time_start:
        :param time_end:
        :param hashtags:
        :param amount: Amount of hashtags needed
        :return:
        """
        return sorted(set(hashtags),key=attrgetter('hashtag_name'))[:amount]


class ListenManager(models.Manager):
    def listen_count(self,
                     type_search="now",
                     time_start=None,
                     time_end=None):
        return self.count()

    def active_listen_count(self,
                            type_search="now",
                            time_start=None,
                            time_end=None):
        return self.filter(is_active=True).count()

    def total_time_listened(self,
                            type_search="now",
                            time_start=None,
                            time_end=None):
        return self.aggregate(Sum('time_listened'))

    def total_active_time_listened(self,
                                   type_search="now",
                                   time_start=None,
                                   time_end=None):
        return self.filter(is_active=True).aggregate(Sum('time_listened'))

    def average_time_listened(self,
                              type_search="now",
                              time_start=None,
                              time_end=None):
        return self.aggregate(Avg('time_listened'))

    def average_active_time_listened(self,
                                     type_search="now",
                                     time_start=None,
                                     time_end=None):
        return self.filter(is_active=True).aggregate(Avg('time_listened'))

    def average_listens_per_user(self,
                                 type_search="now",
                                 time_start=None,
                                 time_end=None,
                                 listens=Listen.objects.all(),
                                 users=User.using('ye_1_db_1').objects.all().count()):
        """
        :param type_search:
        :param time_start:
        :param time_end:
        :param listens: Number of Listens
        :param users: Number of users
        :return: Return average listens per user
        """
        return round(listens / users, 3)

    def average_active_listened_per_user(self,
                                         type_search="now",
                                         time_start=None,
                                         time_end=None,
                                         listens=Listen.objects.filter(is_active=True),
                                         users=User.using('ye_1_db_1').objects.all().count()):
        return round(listens/users, 3)

    def average_time_listened_per_user(self,
                                       type_search="now",
                                       time_start=None,
                                       time_end=None,
                                       users=User.using('ye_1_db_1').objects.all().count()):
        return round(self.average_time_listened(type_search=type_search,
                                                time_start=time_start,
                                                time_end=time_end)/users, 3)

    def average_active_time_listened_per_active_user(self,
                                                     type_search="now",
                                                     time_start=None,
                                                     time_end=None,
                                                     users=User.using('ye_1_db_1').objects.filter(is_active=True).count()):
        return round(self.average_time_listened(type_search=type_search,
                                                time_start=time_start,
                                                time_end=time_end)/users, 3)


class YapManager(models.Manager):
    def yap_count(self,
                  type_search="now",
                  time_start=None,
                  time_end=None):
        return self.count()

    def active_yap_count(self,
                         type_search="now",
                         time_start=None,
                         time_end=None):
        return self.filter(is_active=True).count()

    def total_time_yapped(self,
                          type_search="now",
                          time_start=None,
                          time_end=None,
                          yaps=Yap.objects.all(),
                          ):
        return yaps.aggregate(Sum('length'))

    def total_active_time_yapped(self,
                                 type_search="now",
                                 time_start=None,
                                 time_end=None,
                                 yaps=Yap.objects.filter(is_active=True)):
        return yaps.aggregate(Sum('length'))

    def average_time_yapped(self,
                            type_search="now",
                            time_start=None,
                            time_end=None,
                            yaps=Yap.objects.all()):
        return yaps.aggregate(Sum('length'))

    def average_active_time_yapped(self,
                                   type_search="now",
                                   time_start=None,
                                   time_end=None,
                                   yaps=Yap.objects.filter(is_active=True)):
        return yaps.aggregate(Sum('length'))

    def average_yap_per_user(self,
                             type_search="now",
                             time_start=None,
                             time_end=None,
                             yaps=Yap.objects.all(),
                             users=User.using('ye_1_db_1').objects.all().count()):

        return round(self.yap_count(type_search=type_search,
                                    time_start=time_start,
                                    time_end=time_end) / users)


class LikeManager(models.Manager):
    def like_count(self,
                   type_search="now",
                   time_start=None,
                   time_end=None):
        return self.count()

    def active_like_count(self,
                          type_search="now",
                          time_start=None,
                          time_end=None):
        return self.filter(is_active=True).count()


class ReyapManager(models.Manager):
    def reyap_count(self,
                   type_search="now",
                   time_start=None,
                   time_end=None):
        return self.count()

    def active_reyap_count(self,
                          type_search="now",
                          time_start=None,
                          time_end=None):
        return self.filter(is_active=True).count()