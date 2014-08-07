from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'survey/$', 'promoterscore.views.retrieve_survey', name='retrieve_survey'),
                       url(r'create-promoter-score/$', 'promoterscore.views.create_promoter_score', name='create_promoter_score'),
)
