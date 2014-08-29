from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'user_details/$', 'listings.views.user_details'),
    url(r'users/$', 'listings.views.list_users'),
    url(r'countries/$', 'listings.views.list_countries'),
    url(r'hashtags/$', 'listings.views.list_hashtags'),
    url(r'yaps/$', 'listings.views.list_yaps'),
    )