from yap.models import *
from django.contrib.gis.db import models
from django.db.models import Sum, Count, Avg
import operator
import datetime



"""


Time_start == Datetime.datetime
Time_end == Datetime.datetime

No datetime.timedelta

"""


class UserManager(models.Manager):

    """
    UserManager for stats
    """
    def users_count(self,
                    type_search="now",
                    time_start=None,
                    time_end=None,
                    accuracy=10):
        """
        Count users
        :param type_search: If Now or on an interval
        :param time_start: Date begin if interval
        :param time_end: Date end if interval
        :return: Int = Count users or Dictionary with count depending on start and end time
        """
        print time_start
        users = User.objects.using('ye_1_db_1').all()

        if type_search == "graph":
            data = []
            delta = datetime.timedelta(minutes=time_start)/accuracy
            # Not time_end => From Start date to now
            if not time_end:
                now = datetime.datetime.now()
            else:
                now = time_end
            i = 0
            while i < accuracy:
                i += 1
                time = now - delta * i
                data.append(users.filter(date_joined_lte=time).count())
            return data
        return users.filter(date_joined__lte=time_start).count()

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
        return User.objects.using('ye_1_db_1').filter(is_active=True, date_joined__lte=time_start).count()

    def birthday_month_users(self,
                             type_search="now",
                             time_start=None,
                             time_end=None):
        if type_search == "graph":
            return
        users = User.objects.using('ye_1_db_1').all()
        return users.filter(profile__date_of_birth=datetime.date.today()).count()

    def new_users_count(self,
                        type_search="now",
                        time_start=None,
                        time_end=None):
        """
        Count New users from time_start to time_end.
        :param type_search: If Now or on an interval
        :param time_start: Date begin interval.
        :param time_end: Date end if interval. if time_end == empty: time_end = Now
        :return: Int = Count New users
        """

        #time = time_end - time_start
        users = User.objects.using('ye_1_db_1').all()
        return users.filter(date_joined__gte=time_start).count()

    def to_push_notify(self,
                       type_search="now",
                       time_start=None,
                       time_end=None):
        """
        Get users that accept Push Notifications
        :param type_search:
        :param time_start:
        :param time_end:
        :return: list of users push notify
        """
        data = []
        for u in self.all():
            last = u.sessions.order_by('date_created').last()
            if last and (last.session_device_token == "<>" or not last.session_device_token or not last.is_active):
                continue
            data.append(u)
        return data


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
                     hashtags=None,
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
        hashtags = self.all()
        return sorted(set(hashtags),key=attrgetter('hashtag_name'))[:amount]


class ListenManager(models.Manager):
    def listen_count(self,
                     type_search="now",
                     time_start=None,
                     time_end=None):
        if time_start:
            return self.filter(date_created__lte=time_start).count()
        return self.count()

    def active_listen_count(self,
                            type_search="now",
                            time_start=None,
                            time_end=None):
        if time_start:
            return self.filter(date_created__lte=time_start, is_active=True).count()
        return self.filter(is_active=True).count()

    def total_time_listened(self,
                            type_search="now",
                            time_start=None,
                            time_end=None):
        if time_start:
            return round(self.filter(date_created__lte=time_start).aggregate(Sum('time_listened'))['time_listened__sum'], 3)
        return round(self.aggregate(Sum('time_listened'))['time_listened__sum'], 3)

    def total_active_time_listened(self,
                                   type_search="now",
                                   time_start=None,
                                   time_end=None):
        if time_start:
            return round(self.filter(is_active=True, date_created__lte=time_start).aggregate(Sum('time_listened'))['time_listened__sum'], 3)
        return round(self.filter(is_active=True).aggregate(Sum('time_listened'))['time_listened__sum'], 3)

    def average_time_listened(self,
                              type_search="now",
                              time_start=None,
                              time_end=None):
        if time_start:
            return round(self.filter(date_created__lte=time_start).aggregate(Avg('time_listened'))['time_listened__avg'], 3)
        return round(self.aggregate(Avg('time_listened'))['time_listened__avg'], 3)

    def average_active_time_listened(self,
                                     type_search="now",
                                     time_start=None,
                                     time_end=None):
        if time_start:
            return round(self.filter(is_active=True, date_created__lte=time_start).aggregate(Avg('time_listened'))['time_listened__avg'], 3)
        return round(self.filter(is_active=True).aggregate(Avg('time_listened'))['time_listened__avg'], 3)

    def average_listens_per_user(self,
                                 type_search="now",
                                 time_start=None,
                                 time_end=None,
                                 listens=None,
                                 users=None):
        """
        :param type_search:
        :param time_start:
        :param time_end:
        :param listens: Number of Listens
        :param users: Number of users
        :return: Return average listens per user
        """
        if time_start:
            listens = self.filter(date_created__lte=time_start)
            users = User.objects.using('ye_1_db_1').filter(date_joined_lte=time_start).count()
        else:
            listens = self.all()
            users = User.objects.using('ye_1_db_1').all().count()
        return round(listens / users, 3)

    def average_active_listened_per_user(self,
                                         type_search="now",
                                         time_start=None,
                                         time_end=None,
                                         listens=None,
                                         users=None):
        listens = self.all()
        users= User.objects.using('ye_1_db_1').all().count()
        return round(listens/users, 3)

    def average_time_listened_per_user(self,
                                       type_search="now",
                                       time_start=None,
                                       time_end=None,
                                       users=None):
        users = User.objects.using('ye_1_db_1').all().count()
        return round(self.average_time_listened(type_search=type_search,
                                                time_start=time_start,
                                                time_end=time_end)/users, 3)

    def average_active_time_listened_per_active_user(self,
                                                     type_search="now",
                                                     time_start=None,
                                                     time_end=None,
                                                     users=None):
        users = User.objects.using('ye_1_db_1').all().count()
        return round(self.average_time_listened(type_search=type_search,
                                                time_start=time_start,
                                                time_end=time_end)/users, 3)


class YapManager(models.Manager):
    def yap_count(self,
                  type_search="now",
                  time_start=None,
                  time_end=None):

        if type_search == "full":
            data ={}
            return
        return self.filter(date_created__lte=time_start).count()

    def active_yap_count(self,
                         type_search="now",
                         time_start=None,
                         time_end=None):
        return self.filter(is_active=True, date_created__lte=time_start).count()

    def total_time_yapped(self,
                          type_search="now",
                          time_start=None,
                          time_end=None,
                          yaps=None,
                          ):
        yaps = self.filter(date_created__lte=time_start)
        if yaps:
            return yaps.aggregate(Sum('length'))['length__sum']
        return 0

    def total_active_time_yapped(self,
                                 type_search="now",
                                 time_start=None,
                                 time_end=None,
                                 yaps=None):
        yaps = self.filter(date_created__lte=time_start, is_active=True)
        if yaps:
            return yaps.aggregate(Sum('length'))['length__sum']
        return 0

    def average_time_yapped(self,
                            type_search="now",
                            time_start=None,
                            time_end=None,
                            yaps=None):
        yaps = self.filter(date_created__lte=time_start)
        if yaps:
            return yaps.aggregate(Sum('length'))['length__sum']
        return 0

    def average_active_time_yapped(self,
                                   type_search="now",
                                   time_start=None,
                                   time_end=None,
                                   yaps=None):
        yaps = self.filter(date_created__lte=time_start, is_active=True)
        if yaps:
            return yaps.aggregate(Sum('length'))['length__sum']
        return 0

    def average_yap_per_user(self,
                             type_search="now",
                             time_start=None,
                             time_end=None,
                             yaps=None,
                             users=None):
        count_users = User.objects.using('ye_1_db_1').filter(date_joined__lte=time_start).count()
        if count_users:
            return round(self.yap_count(type_search=type_search,
                                        time_start=time_start,
                                        time_end=time_end) / count_users)
        return 0


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
        if time_start:
            return self.filter(date_created__lte=time_start).count()
        return self.count()

    def active_reyap_count(self,
                           type_search="now",
                           time_start=None,
                           time_end=None):
        if time_start:
            return self.filter(is_active=True, date_created__lte=time_start).count()
        return self.filter(is_active=True).count()

    def new_reyap_count(self,
                        type_search="now",
                        time_start=None,
                        time_end=None):
        if time_start:
            return self.filter(date_created__gte=time_start).count()
        return self.count()