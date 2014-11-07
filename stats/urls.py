from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^usership/$', 'stats.views.stats_usership'),
    url(r'^more_data/$', 'stats.views.more_data'),
    url(r'^yaps/$', 'stats.views.stats_yaps'),
    url(r'^yaps/more_data/$', 'stats.views.more_data_yaps'),
    url(r'spec_stats/', 'stats.views.spec_stats'),
    )