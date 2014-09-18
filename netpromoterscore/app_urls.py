from django.conf.urls import patterns, url
from .views import NetPromoterScoreView

urlpatterns = patterns('',
    url(r'$', NetPromoterScoreView.as_view(), name='net-promoter-score'),
)