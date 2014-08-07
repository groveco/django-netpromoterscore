from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'$', 'promoterscore.views.get_net_promoter_score', name='net-promoter-score'),
)