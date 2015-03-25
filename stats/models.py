from yap.models import Yap, Country, Like, Listen, Reyap, Hashtag
from django.contrib.gis.db import models
from django.db.models import Sum, Count, Avg
from django.contrib.auth.models import User
from operator import attrgetter
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
    @staticmethod
    def users_count(type_search="now",
                    time_start=None,
                    time_end=None,
                    accuracy=10):
        """
        Count users
        :param type_search: If Now or on an interval
        :param time_start: Date begin if interval
        :param time_end: Date end if interval
        :return: Normal = Count users or Dictionary with count depending on start and end time
                 Graph Case = List of couple (date, data). Example: data = [(datetime.now, '12'), (datetime.now - 2, '14')
        """
        users = User.objects.using('ye_1_db_1').all()

        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                data.append((time, users.filter(date_joined__lte=time).count()))
            return data
        return users.filter(date_joined__lte=time_start).count()


    @staticmethod
    def active_users_count(type_search="now",
                           time_start=None,
                           time_end=None,
                           accuracy=10):
        """
        Count Active users
        :param type_search: If Now or on an interval
        :param time_start: Date begin if interval
        :param time_end: Date end if interval
        :return: Int = Count Active users
        """
        users = User.objects.using('ye_1_db_1').filter(is_active=True)

        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                data.append((time, users.filter(date_joined__lte=time).count()))
            return data
        return users.filter(date_joined__lte=time_start).count()


    @staticmethod
    def new_users_count(type_search="now",
                        time_start=None,
                        time_end=None,
                        accuracy=10):
        """
        Count New users from time_start to time_end.
        :param type_search: If Now or on an interval
        :param time_start: Date begin interval.
        :param time_end: Date end if interval. if time_end == empty: time_end = Now
        :return: Int = Count New users
        """
        users = User.objects.using('ye_1_db_1').all()

        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                data.append((time, users.filter(date_joined__gte=time).count()))
            return data
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

    @staticmethod
    def birthday_month_users(self,
                             type_search="now",
                             time_start=None,
                             time_end=None):
        if type_search == "graph":
            return
        users = User.objects.using('ye_1_db_1').all()
        return users.filter(profile__date_of_birth=datetime.date.today()).count()


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

    @staticmethod
    def top_hashtags(type_search="now",
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
        hashtags = Hashtag.objects.all()
        return sorted(set(hashtags), key=attrgetter('hashtag_name'))[:amount]


class ListenManager(models.Manager):

    @staticmethod
    def listen_count(type_search="now",
                     time_start=None,
                     time_end=None,
                     accuracy=10):
        listens = Listen.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                data.append((time, listens.filter(date_created__lte=time).count()))
            return data
        return listens.filter(date_created__lte=time_start).count()

    @staticmethod
    def active_listen_count(type_search="now",
                            time_start=None,
                            time_end=None,
                            accuracy=10):
        listens = Listen.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                data.append((time, listens.filter(date_created__lte=time, is_active=True).count()))
            return data
        return Listen.objects.filter(date_created__lte=time_start, is_active=True).count()


    @staticmethod
    def total_time_listened(type_search="now",
                            time_start=None,
                            time_end=None,
                            accuracy=10):
        listens = Listen.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                l = listens.filter(date_created__lte=time)
                if l:
                    data.append((time, l.aggregate(Sum('time_listened'))['time_listened__sum']))
                else:
                    data.append((time, 0))
            return data
        listens = listens.filter(date_created__lte=time_start)
        if listens:
            return round(listens.aggregate(Sum('time_listened'))['time_listened__sum'], 3)
        return 0


    @staticmethod
    def total_active_time_listened(type_search="now",
                                   time_start=None,
                                   time_end=None,
                                   accuracy=10):
        listens = Listen.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                l = listens.filter(date_created__lte=time)
                if l:
                    data.append((time, l.aggregate(Sum('time_listened'))['time_listened__sum']))
                else:
                    data.append((time, 0))
            return data
        listens = listens.filter(is_active=True, date_created__lte=time_start)
        if listens:
            return round(listens.aggregate(Sum('time_listened'))['time_listened__sum'], 3)
        return 0


    @staticmethod
    def average_time_listened(type_search="now",
                              time_start=None,
                              time_end=None,
                              accuracy=10):
        listens = Listen.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                l = listens.filter(date_created__lte=time)
                if l:
                    data.append((time, l.aggregate(Avg('time_listened'))['time_listened__avg']))
                else:
                    data.append((time, 0))
            return data
        listens = listens.filter(date_created__lte=time_start)
        if listens:
            return round(listens.aggregate(Avg('time_listened'))['time_listened__avg'], 3)
        return 0

    @staticmethod
    def average_active_time_listened(type_search="now",
                                     time_start=None,
                                     time_end=None,
                                     accuracy=10):
        listens = Listen.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                l = listens.filter(is_active=True, date_created__lte=time)
                if l:
                    data.append((time, l.aggregate(Avg('time_listened'))['time_listened__avg']))
                else:
                    data.append((time, 0))
            return data
        listens = listens.filter(is_active=True, date_created__lte=time_start)
        if listens:
            return round(listens.aggregate(Avg('time_listened'))['time_listened__avg'], 3)
        return 0

    @staticmethod
    def average_listens_per_user(type_search="now",
                                 time_start=None,
                                 time_end=None,
                                 listens=None,
                                 users=None,
                                 accuracy=10):
        """
        :param type_search:
        :param time_start:
        :param time_end:
        :param listens: Number of Listens
        :param users: Number of users
        :return: Return average listens per user
        """
        listens = Listen.objects.all()
        users = User.objects.using('ye_1_db_1').all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                l = listens.filter(date_created__lte=time)
                u = users.filter(date_joined__lte=time)
                if l and u:
                    data.append((time, l.aggregate(Avg('time_listened'))['time_listened__avg']))
                else:
                    data.append((time, 0))
            return data
        listens = listens.filter(date_created__lte=time_start)
        users = User.objects.using('ye_1_db_1').filter(date_joined_lte=time_start).count()
        if listens and users:
            return round(listens / users, 3)
        return 0


    @staticmethod
    def average_active_listened_per_user(type_search="now",
                                         time_start=None,
                                         time_end=None,
                                         listens=None,
                                         users=None,
                                         accuracy=10):
        listens = Listen.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                l = listens.filter(is_active=True, date_created__lte=time)
                if l:
                    data.append((time, l.aggregate(Avg('time_listened'))['time_listened__avg']))
                else:
                    data.append((time, 0))
            return data
        listens = listens.filter(is_active=True, date_created__lte=time_start)
        users = User.objects.using('ye_1_db_1').filter(date_joined_lte=time_start).count()
        if listens and users:
            return round(listens / users, 3)


    @staticmethod
    def average_time_listened_per_user(type_search="now",
                                       time_start=None,
                                       time_end=None,
                                       users=None,
                                       accuracy=10):
        users = User.objects.using('ye_1_db_1').all().count()
        return round(ListenManager.average_time_listened(type_search=type_search,
                                                          time_start=time_start,
                                                          time_end=time_end)/users, 3)


    @staticmethod
    def average_active_time_listened_per_active_user(type_search="now",
                                                     time_start=None,
                                                     time_end=None,
                                                     users=None,
                                                     accuracy=10):
        users = User.objects.using('ye_1_db_1').all().count()
        return round(ListenManager.average_active_time_listened(type_search=type_search,
                                                          time_start=time_start,
                                                          time_end=time_end)/users, 3)


class YapManager(models.Manager):

    @staticmethod
    def yap_count(type_search="now",
                  time_start=None,
                  time_end=None,
                  accuracy=10):
        yaps = Yap.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                data.append((time, yaps.filter(date_created__lte=time).count()))
            return data
        return yaps.filter(date_created__lte=time_start).count()

    @staticmethod
    def active_yap_count(type_search="now",
                         time_start=None,
                         time_end=None,
                         accuracy=10):
        yaps = Yap.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                data.append((time, yaps.filter(is_active=True, date_created__lte=time).count()))
            return data
        return yaps.filter(is_active=True, date_created__lte=time_start).count()

    @staticmethod
    def total_time_yapped(type_search="now",
                          time_start=None,
                          time_end=None,
                          accuracy=10):
        yaps = Yap.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                y = yaps.filter(date_created__lte=time)
                if y:
                    data.append((time, y.aggregate(Sum('length'))['length__sum']))
                else:
                    data.append((time, 0))
            return data
        if yaps:
            return yaps.filter(date_created__lte=time_start).aggregate(Sum('length'))['length__sum']
        return 0

    @staticmethod
    def total_active_time_yapped(type_search="now",
                                 time_start=None,
                                 time_end=None,
                                 accuracy=10):
        yaps = Yap.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                y = yaps.filter(is_active=True, date_created__lte=time)
                if y:
                    data.append((time, y.aggregate(Sum('length'))['length__sum']))
                else:
                    data.append((time, 0))
            return data
        if yaps.filter(date_created__lte=time_start, is_active=True):
            return yaps.filter(date_created__lte=time_start, is_active=True).aggregate(Sum('length'))['length__sum']
        return 0

    @staticmethod
    def average_time_yapped(type_search="now",
                            time_start=None,
                            time_end=None,
                            accuracy=10):
        yaps = Yap.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                y = yaps.filter(date_created__lte=time)
                if y:
                    data.append((time, round(y.aggregate(Avg('length'))['length__avg']), 3))
                else:
                    data.append((time, 0))
            return data
        if yaps.filter(date_created__lte=time_start):
            return round(yaps.filter(date_created__lte=time_start).aggregate(Avg('length'))['length__avg'], 3)
        return 0

    @staticmethod
    def average_active_time_yapped(type_search="now",
                                   time_start=None,
                                   time_end=None,
                                   accuracy=10):
        yaps = Yap.objects.all()
        if type_search == "graph":
            data = []
            # Not time_end => From Start date to now
            if not time_end:
                time_end = datetime.datetime.now()
            delta = (time_start - time_end)/accuracy
            i = 0
            while i < accuracy:
                i += 1
                time = time_start - delta * i
                y = yaps.filter(date_created__lte=time, is_active=True)
                if y:
                    data.append((time, round(y.aggregate(Avg('length'))['length__avg'], 3)))
                else:
                    data.append((time, 0))
            return data
        if yaps.filter(date_created__lte=time_start, is_active=True):
            return round(yaps.aggregate(Avg('length'))['length__avg'], 3)
        return 0

    @staticmethod
    def average_yap_per_user(type_search="now",
                             time_start=None,
                             time_end=None,
                             accuracy=10):
        count_users = User.objects.using('ye_1_db_1').filter(date_joined__lte=time_start).count()
        if count_users:
            return round(YapManager.yap_count(type_search=type_search,
                                              time_start=time_start,
                                              time_end=time_end) / count_users, 3)
        return 0


class LikeManager(models.Manager):
    def like_count(type_search="now",
                   time_start=None,
                   time_end=None,
                   accuracy=10):
        return Like.objects.count()

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
        return Like.objects.count()

    def active_reyap_count(self,
                           type_search="now",
                           time_start=None,
                           time_end=None):
        if time_start:
            return Like.objects.filter(is_active=True, date_created__lte=time_start).count()
        return Like.objects.filter(is_active=True).count()

    def new_reyap_count(self,
                        type_search="now",
                        time_start=None,
                        time_end=None):
        if time_start:
            return Like.objects.filter(date_created__gte=time_start).count()
        return Like.objects.count()