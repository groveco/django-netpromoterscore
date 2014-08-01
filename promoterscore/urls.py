from django.conf.urls import patterns, url
from promoterscore.views import PromoterScoreApiView, SurveyApiView

urlpatterns = patterns('',
                       url(r'survey/$', SurveyApiView.as_view({'get': 'retrieve'}), name='promoter-score-get-survey'),
                       url(r'$', PromoterScoreApiView.as_view({'post': 'create'}), name='promoter-score'),

)