from django.conf.urls import patterns, url
from promoterscore.views import PromoterScoreApiView

urlpatterns = patterns('',
                       url(r'^api/promoter-score/$', PromoterScoreApiView.as_view({'post': 'create'}), name='promoter-score'),
                       url(r'^api/promoter-score/get_survey', PromoterScoreApiView.as_view({'get': 'retrieve'}), name='promoter-score-get-survey'),

)