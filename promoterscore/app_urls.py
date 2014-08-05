from django.conf.urls import patterns, url
from promoterscore.views import NetPromoterScoreView

urlpatterns = patterns('',
                       url(r'$', NetPromoterScoreView.as_view({'get': 'get'}), name='promoter-score'),
)