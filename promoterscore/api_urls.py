from django.conf.urls import patterns, url
from promoterscore.views import PromoterScoreApiView, SurveyApiView

# Would not seperate URLs in different files

urlpatterns = patterns('',
                       url(r'survey/$', SurveyApiView.as_view({'get': 'retrieve'}), name='promoter-score-get-survey'),
                       # This should be named and not root
                       url(r'$', PromoterScoreApiView.as_view({'post': 'create'}), name='promoter-score'),
)
