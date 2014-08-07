from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'survey/$', 'netpromoterscore.views.retrieve_survey', name='retrieve_survey'),
                       url(r'create-promoter-score/$', 'netpromoterscore.views.create_promoter_score', name='create_promoter_score'),
)
