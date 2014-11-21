from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^more_data/$', 'stats.views.more_data'),
    url(r'^usership/$', 'stats.views.stats_usership'),
    url(r'^yaps/$', 'stats.views.stats_yaps'),
    url(r'^reyaps/$', 'stats.views.stats_reyaps'),
    url(r'^listens/$', 'stats.views.stats_listens'),
    # url(r'^countries/$', 'stats.views.stats_countries'),
    # url(r'^hashtags/$', 'stats.views.stats_hashtags'),
    # url(r'^databases/$', 'stats.views.stats_databases'),
    url(r'^yaps/more_data/$', 'stats.views.more_data_yaps'),
    url(r'spec_stats/', 'stats.views.spec_stats'),
    url(r'custom_graph/', 'stats.views.custom_graph'),
    )